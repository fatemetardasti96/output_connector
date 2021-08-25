import xml.etree.ElementTree as ET
from decimal import Decimal
import json
import requests

from build_in_functions import iterate_mapping
from parameter_extractor import input_tech_techtype_extractor




def added_capacity(SCENARIO_ID, filepath, year):
    #request database from url
    db_name = 'https://modex.rl-institut.de/scenario/id/{}?source=modex&mapping=regions'.format(SCENARIO_ID)
    r = requests.get(db_name)
    databas = r.json()

    db_name_concrete = 'https://modex.rl-institut.de/scenario/id/{}?source=modex&mapping=concrete'.format(SCENARIO_ID)
    r = requests.get(db_name_concrete)
    databas_concrete = r.json()

    # installed_capacity = iterate_mapping(data, "scalars[? parameter_name == 'installed capacity' && year == `{}`]".format(year))

    tree = ET.parse(filepath)
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


    for this_link in root.iter("link"):
        region = this_link.get("code")
        capacity_dict[region] = {}
        for data in this_link.iter():
            if data.get("code") == "capacity":
                string_capacity = data.text
                capacity = [capacity for capacity in string_capacity.split(",") if bool(capacity)]
                capacity_dict[region]['transmission'] = capacity[0]



    added_capacity_dict = {}
    for region in capacity_dict:
        added_capacity_dict[region] = {}
        for tech_code in capacity_dict[region]:
            input_energy, output_energy, tech, tech_type = input_tech_techtype_extractor(tech_code)
            if tech == "storage":
                input_energy = 'electricity'
            
            capacity_value = capacity_dict[region][tech_code]
            try:
                if tech_code == 'transmission':
                    regionA, regionB = region.split('_')[0], region.split('_')[-1]
                    installed_capacity_value = iterate_mapping(databas_concrete, "oed_scalars[? parameter_name == 'installed capacity' && region==['{}', '{}'] \
                    && technology == 'transmission' && (technology_type=='hvac' || technology_type=='DC') && year==`{}`].value".format(regionA, regionB, year))[0]    
                    
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
                
            added_capacity_dict[region][tech_code] = str(round(added_capacity, 6)+0)


    return capacity_dict, added_capacity_dict