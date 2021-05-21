import xml.etree.ElementTree as ET
from decimal import Decimal
import json
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from build_in_functions import iterate_mapping
from parameter_extractor import input_tech_techtype_extractor




def added_capacity(SCENARIO_ID, year):
    #request database from url
    db_name = 'https://modex.rl-institut.de/scenario/id/{}?source=modex&mapping=regions'.format(SCENARIO_ID)
    request = urllib.request.urlopen(db_name)
    data = json.load(request)

    installed_capacity = iterate_mapping(data, "scalars[? parameter_name == 'installed capacity' && year == `{}`]".format(year))

    tree = ET.parse("Resultfiles/Base-Scenario/AnalysedResult_{}.xml".format(year))
    root = tree.getroot()

    capacity_dict = {}
    for this_region in root.iter("region"):
        region = this_region.get("code")
        capacity_dict[region] = {}
        for types in ("converter", "storage"):
            for technology in this_region.iter(types):
                tech_code = technology.get("code")
                for data in technology.iter():
                    if data.get("code") == "capacity":                    
                        string_capacity = data.text
                        capacity = [capacity for capacity in string_capacity.split(",") if bool(capacity)]
                        capacity_dict[region][tech_code] = capacity[0]


    added_capacity_dict = {}
    for region in capacity_dict:
        added_capacity_dict[region] = {}
        for tech_code in capacity_dict[region]:
            input_energy, output_energy, tech, tech_type = input_tech_techtype_extractor(tech_code)
            capacity_value = capacity_dict[region][tech_code]
            try:
                installed_capacity_value = iterate_mapping(installed_capacity, "[? region=='{}' && input_energy_vector=='{}'\
                && technology == '{}' && technology_type=='{}' && year==`{}`].value".format(region, input_energy, tech, tech_type, year))[0]
            except:
                installed_capacity_value = 0

            added_capacity = Decimal(capacity_value) - Decimal(installed_capacity_value/1000.0)
            added_capacity_dict[region][tech_code] = str(added_capacity)


    return added_capacity_dict