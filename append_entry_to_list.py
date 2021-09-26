from create_entry import scalars_entry, timeseries_entry       
from parameter_extractor import input_tech_techtype_extractor

SOURCE = "GENESYS-2"


def append_entry(region_list, year, system_cost, emission, generation, slack, curtailment, emission_region_dict, electricity_generation_dict,\
                input_energy_dict, output_energy_dict, storage_level_dict, energy_flow_dict, capacity_dict, added_capacity_dict, fopex_dict,\
                vopex_dict, total_vopex, capex_dict, loss_dict, scalars_list, timeseries_list):

    scalars_list.append(scalars_entry(region_list,"ALL","ALL","system cost", "ALL", "ALL", system_cost, "€", SOURCE))
    scalars_list.append(scalars_entry(region_list,"ALL","CO2","emissions", "ALL", "ALL", emission, "Gt", SOURCE))
    scalars_list.append(scalars_entry(region_list,"ALL","ALL","renewable generation", "ALL", "ALL", generation, "GWh", SOURCE))    

    for region in slack.keys():
        scalars_list.append(scalars_entry(region, "ALL", "ALL", "slack", "ALL", "ALL", slack[region], "GWh", SOURCE))
    for region in curtailment.keys():
        scalars_list.append(scalars_entry(region, "ALL", "ALL", "curtailment", "ALL", "ALL", curtailment[region], "GWh", SOURCE))

    for region in emission_region_dict.keys():
        scalars_list.append(scalars_entry(region, "ALL", "CO2", "emissions", "ALL", "ALL", emission_region_dict[region], "Gt", SOURCE))

    for region in electricity_generation_dict:
        for tech_code in electricity_generation_dict[region]:
            input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code)
            scalars_list.append(scalars_entry(region, input_energy, output_energy, "electricity generation", technology, technology_type,\
                    str(sum(electricity_generation_dict[region][tech_code])), "GWh", SOURCE))

            timeseries_list.append(timeseries_entry(region, input_energy, "electricity", "electricity generation", technology, technology_type, year,\
                    [float(i)*1000 for i in electricity_generation_dict[region][tech_code]], "MWh", SOURCE, " "))


    for region in input_energy_dict:
        for tech_code in input_energy_dict[region]:
            input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code) 
            scalars_list.append(scalars_entry(region, input_energy, output_energy, "input energy", technology, technology_type, str(sum(input_energy_dict[region][tech_code])), "GWh", SOURCE))

            timeseries_list.append(timeseries_entry(region, input_energy, output_energy, "input energy", technology, technology_type, year,\
                    [float(i)*1000 for i in input_energy_dict[region][tech_code]], "MWh", SOURCE, " "))


    for region in output_energy_dict:
        for tech_code in output_energy_dict[region]:
            input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code)     
            scalars_list.append(scalars_entry(region, input_energy, output_energy, "output energy", technology, technology_type, str(sum(output_energy_dict[region][tech_code])), "GWh", SOURCE))

            timeseries_list.append(timeseries_entry(region, input_energy, output_energy, "output energy", technology, technology_type, year,\
                    [float(i)*1000 for i in output_energy_dict[region][tech_code]], "MWh", SOURCE, " "))

    for link in energy_flow_dict:
        regA, regB = link.split("_")
        scalars_list.append(scalars_entry([regA, regB], "electricity", "electricity", "energy flow", "transmission", "hvac", str(sum(energy_flow_dict[link])), "GWh", SOURCE))

        timeseries_list.append(timeseries_entry([regA, regB], "electricity", "electricity", "energy flow", "transmission", "hvac", year,\
                    [float(i)*1000 for i in energy_flow_dict[link]], "MWh", SOURCE, " "))


    for region in added_capacity_dict:
        for tech_code in added_capacity_dict[region]:
            input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code)        
            scalars_list.append(scalars_entry(region, input_energy, output_energy, "added capacity", technology, technology_type, added_capacity_dict[region][tech_code], "GW", SOURCE))

    for region in capacity_dict:
        for tech_code in capacity_dict[region]:
            input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code)        
            scalars_list.append(scalars_entry(region, input_energy, output_energy, "capacity", technology, technology_type, capacity_dict[region][tech_code], "GW", SOURCE))


    # for tech_code in fopex_dict.keys():
        # input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code)        
        # scalars_list.append(scalars_entry(region_list, input_energy, output_energy, "fixed cost", technology, technology_type, fopex_dict[tech_code], "€", SOURCE))

    # for tech_code in vopex_dict.keys():
        # input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code) 
        # scalars_list.append(scalars_entry(region_list, input_energy, output_energy, "variable cost", technology, technology_type, vopex_dict[tech_code], "€", SOURCE))

    # for region in vopex_dict:
    #     for tech_code in vopex_dict[region]:
    #         input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor_for_primary_energy(tech_code)     
    #         scalars_list.append(scalars_entry(region, input_energy, output_energy, "variable cost", technology, technology_type, str(vopex_dict[region][tech_code]), "€", SOURCE))

    scalars_list.append(scalars_entry(region_list, "ALL", "ALL", "variable cost", "ALL", "ALL", str(total_vopex), "€", SOURCE))


    for tech_code in capex_dict.keys():
        input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code)        
        scalars_list.append(scalars_entry(region_list, input_energy, output_energy, "investment cost", technology, technology_type, capex_dict[tech_code], "€", SOURCE))

    for tech_code in loss_dict.keys():
        input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code)        
        scalars_list.append(scalars_entry(region_list, input_energy, output_energy, "losses", technology, technology_type, loss_dict[tech_code], "GWh", SOURCE))

    for region in storage_level_dict:
        for tech_code in storage_level_dict[region]:
            input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code) 
            timeseries_list.append(timeseries_entry(region, input_energy, output_energy, "storage level", technology, technology_type, year,\
                [float(i) for i in storage_level_dict[region][tech_code]], "MWh", SOURCE, " "))