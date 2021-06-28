import xml.etree.ElementTree as ET
from decimal import Decimal
import json
import requests

from build_in_functions import iterate_mapping
from parameter_extractor import input_tech_techtype_extractor




def added_capacity(SCENARIO_ID, year):
    #request database from url
    db_name = 'https://modex.rl-institut.de/scenario/id/{}?source=modex&mapping=regions'.format(SCENARIO_ID)
    r = requests.get(db_name)
    databas = r.json()

    # installed_capacity = iterate_mapping(data, "scalars[? parameter_name == 'installed capacity' && year == `{}`]".format(year))

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
            if tech == "storage":
                input_energy = 'electricity'
            
            capacity_value = capacity_dict[region][tech_code]
            try:
                installed_capacity_value = iterate_mapping(databas, "scalars[? parameter_name == 'installed capacity' && region=='{}' && input_energy_vector=='{}'\
                && technology == '{}' && technology_type=='{}' && year==`{}`].value".format(region, input_energy, tech, tech_type, year))[0]
            except:
                installed_capacity_value = 0
            
            if tech_code in ("PH_storage", "BAT1POWER", "FUEL_CELL", "CCH2_TURBINE"):
                try:
                    e2p_ratio = iterate_mapping(databas, "scalars[? parameter_name == 'E2P ratio' && region == '{}' && year == `{}` \
                    && technology == 'storage' && technology_type=='{}'].value".format(region, year, tech_type))[0]            
                except:
                    e2p_ratio = 1
                
                installed_capacity_value *= e2p_ratio
                added_capacity = float(capacity_value) - float(installed_capacity_value)
            else:
                added_capacity = float(capacity_value) - float(installed_capacity_value/1000.0)
                
            added_capacity_dict[region][tech_code] = str(added_capacity)


    return added_capacity_dict