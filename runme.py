from os import listdir
import read_xml

from append_entry_to_list import append_entry
from write_into_csv import create_csv_files

year_to_analyse = 2016
SCENARIO_ID = 32        
# path to results
path_results = "Resultfiles/"
name_results_files = "AnalysedResult_{}.xml".format(year_to_analyse)

def main():
    # check and load results
    scenarios = listdir(path_results)
    for scen in scenarios:
        if len(listdir(path_results + scen)) > 0:
            print("Results exist in: " + path_results + scen)
            # Processing results
            print("Processing Results")

            # Extract data from Result file
            region_list, year, system_cost, emission, generation, slack, curtailment, emission_region_dict, electricity_generation_dict,\
                input_energy_dict, output_energy_dict, storage_level_dict, energy_flow_dict, added_capacity_dict, fopex_dict, vopex_dict, loss_dict\
                = read_xml.get_dict(file=path_results + scen + "/" + name_results_files, scenario=SCENARIO_ID, year=year_to_analyse)
            
            
            scalars_list = []
            timeseries_list = []            
            append_entry(region_list, year, system_cost, emission, generation, slack, curtailment, emission_region_dict, electricity_generation_dict,\
                input_energy_dict, output_energy_dict, storage_level_dict, energy_flow_dict, added_capacity_dict, fopex_dict, vopex_dict, loss_dict, scalars_list, timeseries_list)

            

            create_csv_files(region_list, year, scalars_list, timeseries_list)


        else:
            print("No results in: " + path_results + scen)

if __name__ == "__main__":
    main()


