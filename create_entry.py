import json

def scalars_entry(region, input_energy, output_energy, parameter_name, tech, tech_type, val, unit, source):
    return {
        "region": json.dumps(region) if type(region)==list else json.dumps([region]),
        "input_energy_vector":	input_energy,
        "output_energy_vector":	output_energy,
        "parameter_name": parameter_name,
        "technology": tech,
        "technology_type": tech_type,
        "value": val,
        "unit":	unit,
        "tags":	"",
        "method": json.dumps({"value": "aggregated"}),
        "source": source
    }


def timeseries_entry(region, input_energy, output_energy, parameter_name, tech, tech_type, year, series, unit, source, comment):
    timeindex_start = "{}-01-01 00:00:00".format(year)
    ##TODO what is timeindex_stop?
    timeindex_stop = "{}-12-31 00:00:00".format(year)
    ##TODO adjust time interval
    interval = "1h"
    return {
        "region": json.dumps(region) if type(region)==list else json.dumps([region]),
        "input_energy_vector":	input_energy,
        "output_energy_vector":	output_energy,
        "parameter_name": parameter_name,
        "technology": tech,
        "technology_type": tech_type,
        "timeindex_start": timeindex_start,
        "timeindex_stop": timeindex_stop,
        "timeindex_resolution":	interval,
        "series": series,
        "unit":	unit,
        "tags":	"",
        "method": json.dumps({"value": "timeseries"}),
        "source": source,
        "comment": comment
    }


