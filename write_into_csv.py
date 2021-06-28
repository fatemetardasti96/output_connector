import csv
import json
from datetime import datetime
from pathlib import Path
import shutil

dirname = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
Path('genesys/'+dirname).mkdir()

src = r'genesys/datapackage.json'
dst = 'genesys/'+dirname + '/datapackage.json'
shutil.copy(src, dst, follow_symlinks=True)

def list_into_csv(list_of_dict, identifiers, filename):    
    path = "genesys/" + dirname + '/' + filename
    with open(path, "w") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=identifiers)
        writer.writeheader()
        for i, scalar_dict in enumerate(list_of_dict):                      
            writer.writerow({key: scalar_dict[key] for key in identifiers})


def create_scenario_csv(values, identifiers, filename):    
    path = "genesys/" + dirname + '/' + filename
    with open(path, "w") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(identifiers)
        writer.writerow(values)


def create_csv_files(region_list, year, scalars_list, timeseries_list):
    scenario_id = 1
    scenario_name = "Basisszenario"
    scenario_identifiers = ["id",	"scenario",	"region", "year", "source", "comment"]
    scenario_filename = "oed_scenario_output.csv"
    scenario_list = [scenario_id, scenario_name,	json.dumps({"DE": region_list}), year, "open_MODEX", ""]
    create_scenario_csv(scenario_list, scenario_identifiers, scenario_filename)


    scalar_identifiers = ["id", "scenario_id", "region", "input_energy_vector", "output_energy_vector", "parameter_name", "technology",\
    "technology_type", "value",	"unit",	"tags" ,"method", "source", "comment", "year"]
    scalar_filename = "oed_scalar_output.csv"
    for i, scalar_dict in enumerate(scalars_list):
        scalar_dict["id"] = i+1
        scalar_dict["scenario_id"] = scenario_id
        scalar_dict["comment"] = ""
        scalar_dict["year"] = year
    list_into_csv(scalars_list, scalar_identifiers, scalar_filename)


    timeseries_identifiers = ["id", "scenario_id", "region", "input_energy_vector", "output_energy_vector", "parameter_name", "technology",\
    "technology_type", "timeindex_start", "timeindex_stop", "timeindex_resolution",	"series", "unit", "tags" ,"method", "source", "comment"]
    timeseries_filename = "oed_timeseries_output.csv"
    for i, timeseries_dict in enumerate(timeseries_list):
        timeseries_dict["id"] = i+1
        timeseries_dict["scenario_id"] = 1 
    list_into_csv(timeseries_list, timeseries_identifiers, timeseries_filename)