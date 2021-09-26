import os
import read_xml
from pathlib import Path
from datetime import datetime

from append_entry_to_list import append_entry
from write_into_csv import create_csv_files

SCENARIO_ID = 58        
scenario_type = "Base-Scenario"
dirpath = "Resultfiles/v12/" + scenario_type

output_dirname = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
Path('genesys/'+output_dirname).mkdir()


def main():
    for filepath in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filepath)
        if os.path.isfile(filepath):
            print("Results exist in: " + filepath)
            print("Processing Results")
            
            # Extract data from Result file
            print("Start reading dictionaries")
            region_list, year, system_cost, emission, generation, slack, curtailment, emission_region_dict, electricity_generation_dict,\
                input_energy_dict, output_energy_dict, storage_level_dict, energy_flow_dict, capacity_dict, added_capacity_dict, fopex_dict,\
                    vopex_dict, total_vopex, capex_dict, loss_dict, total_load = read_xml.get_dict(file=filepath, scenario=SCENARIO_ID, scenario_type="base")
            
            print("sum of total load for ", year, " : ", sum(total_load.values()))

            scalars_list = []
            timeseries_list = []   
            
            print("write dictionaries into csv")
            append_entry(region_list, year, system_cost, emission, generation, slack, curtailment, emission_region_dict,\
                electricity_generation_dict, input_energy_dict, output_energy_dict, storage_level_dict, energy_flow_dict, capacity_dict,\
                added_capacity_dict, fopex_dict, vopex_dict, total_vopex, capex_dict, loss_dict, scalars_list, timeseries_list)            

            output_dir = "genesys/" + output_dirname + '/' + scenario_type +  '/' + year
            Path(output_dir).mkdir(parents=True, exist_ok=True)


            create_csv_files(region_list, year, scalars_list, timeseries_list, scenario_type, output_dir)


        else:
            print("No results in: " + filepath)

if __name__ == "__main__":
    main()


