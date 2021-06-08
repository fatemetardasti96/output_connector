import os
import xml.etree.ElementTree as ET
from decimal import Decimal
import math

from date_adjust import hour_iterator
from parameter_extractor import input_tech_techtype_extractor
from added_capacity import added_capacity


def zero_appender(timeserie, start_timeindex, year):
    calender_dict = hour_iterator(year,1,1,0,0,year+1,1,1,0,0)
    time_index = calender_dict[start_timeindex]
    zero_timeserie = [0 for i in range(len(calender_dict))]
    zero_timeserie[time_index:time_index+len(timeserie)] = timeserie
    return zero_timeserie
    
def generate_electricity(tech_code):
    input_energy, output_energy, technology, technology_type = input_tech_techtype_extractor(tech_code)
    if technology == 'storage':
        return False
    return True

def get_dict(**kwargs):
    scenario = kwargs["scenario"]
    year = kwargs["year"]
    if os.path.isfile(kwargs["file"]):
        print(kwargs["file"])
        print("File exists {}, now parsing!".format(kwargs["file"]))
        # parse from xml, working with xml trees return a xml_root
        tree = ET.parse(kwargs["file"])
        root = tree.getroot()

        # dictionary to safe information from xml sheet
        component_dict = {}
        link_dict = {}
        glob_internal_dict = {}
        type_dict = {"converter","storage","primary_energy","region_internal"}
    
        #get list of all regions
        region_list = sorted([region.get("code") for region in root.iter("region")])
        # get regions
        for this_region in root.iter("region"):
            region = this_region.get("code")
            component_dict[region] = {}
            for types in type_dict:
                component_dict[region][types] = {}
                for installed_conv in this_region.iter(types):
                    component = installed_conv.get("code")
                    component_dict[region][types][component] = installed_conv
        

        #get emission
        total_emission = 0
        emission_region_dict = {}
        for this_region in root.iter("region"):
            emission = [Decimal(emission.text[:-1])/10**12 for emission in this_region.findall(".//region_internal/data[@code='annual_co2_emissions']")]
            emission_region_dict[this_region.get("code")] = str(emission[0]) if not math.isnan(emission[0]) else 0
            if not math.isnan(emission[0]):
                total_emission += emission[0]
        


        #get generation
        total_generation = 0
        RENEWABLES = {"BIOMASS_TURBINE", "BIOMASS_FURNANCE_CHP", "BIOMASS_FURNANCE", "BIO_CH4_TURBINE", "ROR", "WIND_ONS", "WIND_OFF", "PV1", "PV2", "GEO"}
        for renewable in RENEWABLES:
            for this_region in root.iter("region"):
                try:
                    string_timeseries = [elem.text for elem in this_region.findall(".//converter[@code='{}']/data[@code='used_capacity']".format(renewable))]
                    decimal_timeseries = [Decimal(timeserie) for timeserie in string_timeseries[0].split(",") if bool(timeserie)]
                    total_generation += sum(decimal_timeseries)
                except:
                    # print("{} doesn"t exist in {}".format(renewable, this_region.get("code")))
                    continue
        
        #get electricity generation
        electricity_generation_dict = {}
        for this_region in root.iter("region"):
            region = this_region.get("code")
            electricity_generation_dict[region] = {}
            for conv in this_region.iter("converter"):
                technology_code = conv.get("code")
                if generate_electricity(technology_code):
                    for data in conv.iter():
                        if data.get("code") == "used_capacity":
                            string_electricity_generation = data.text
                            splitted_electricity_generation = [abs(Decimal(gen)) for gen in string_electricity_generation.split(",") if bool(gen)]
                            start_timeindex = data.get("start")
                            if start_timeindex.split("-")[0] == "1970":
                                start_timeindex = "{}-1-1_0:0".format(year)
                            electricity_generation_dict[region][technology_code] = zero_appender(splitted_electricity_generation, start_timeindex, year)
                            # print(len(electricity_generation_dict[region][technology_code]), region, technology_code)

        

        #get input energy
        input_energy_dict = {}
        output_energy_dict = {}
        for this_region in root.iter("region"):
            region = this_region.get("code")
            input_energy_dict[region] = {}
            output_energy_dict[region] = {}
            for technology_code in ["PH_TURBINE", "BAT1POWER"]:
                for conv in this_region.iter("converter"):
                    tech = conv.get("code")
                    if technology_code == tech:
                        for data in conv.iter():
                            if data.get("code") == "used_capacity":
                                string_energy = data.text
                                if len(string_energy):
                                    splitted_input_energy = []
                                    splitted_output_energy = []
                                    for energy in string_energy.split(","):
                                        if (bool(energy) and Decimal(energy)<=0):
                                            splitted_input_energy.append(abs(Decimal(energy)))
                                        elif bool(energy):
                                            splitted_input_energy.append(0)
                                        
                                    for energy in string_energy.split(","):
                                        if (bool(energy) and Decimal(energy)>=0):
                                            splitted_output_energy.append(abs(Decimal(energy)))
                                        elif bool(energy):
                                            splitted_output_energy.append(0)
                                    
                                    start_timeindex = data.get("start")
                                    if start_timeindex.split("-")[0] == "1970":
                                        start_timeindex = "{}-1-1_0:0".format(year)
                                    input_energy_dict[region][technology_code] = zero_appender(splitted_input_energy, start_timeindex, year)
                                    output_energy_dict[region][technology_code] = zero_appender(splitted_output_energy, start_timeindex, year)

        #input energy for hydrogen storage charger: H2_ELECTROLYSER, H2_ELECTROLYSER_FC
        for this_region in root.iter("region"):
            region = this_region.get("code")
            for technology_code in ["H2_ELECTROLYSER", "H2_ELECTROLYSER_FC"]:
                for conv in this_region.iter("converter"):
                    tech = conv.get("code")
                    if technology_code == tech:
                        for data in conv.iter():
                            if data.get("code") == "used_capacity":
                                string_energy = data.text
                                if len(string_energy):
                                    splitted_input_energy = []
                                    for energy in string_energy.split(","):
                                        if bool(energy):
                                            splitted_input_energy.append(abs(Decimal(energy)))                                        
                                                                            
                                    start_timeindex = data.get("start")
                                    if start_timeindex.split("-")[0] == "1970":
                                        start_timeindex = "{}-1-1_0:0".format(year)
                                    input_energy_dict[region][technology_code] = zero_appender(splitted_input_energy, start_timeindex, year)

        #output energy for hydrogen storage discharger: CCH2_TURBINE, FUEL_CELL
        for this_region in root.iter("region"):
            region = this_region.get("code")
            for technology_code in ["CCH2_TURBINE", "FUEL_CELL"]:
                for conv in this_region.iter("converter"):
                    tech = conv.get("code")
                    if technology_code == tech:
                        for data in conv.iter():
                            if data.get("code") == "used_capacity":
                                string_energy = data.text
                                if len(string_energy):
                                    splitted_output_energy = []
                                        
                                    for energy in string_energy.split(","):
                                        if bool(energy):
                                            splitted_output_energy.append(abs(Decimal(energy)))
                                    
                                    start_timeindex = data.get("start")
                                    if start_timeindex.split("-")[0] == "1970":
                                        start_timeindex = "{}-1-1_0:0".format(year)
                                    output_energy_dict[region][technology_code] = zero_appender(splitted_output_energy, start_timeindex, year)
                    
        #storage level
        storage_level = {}
        for this_region in root.iter("region"):
            region = this_region.get("code")
            storage_level[region] = {}
            for storage in this_region.iter("storage"):
                technology_code = storage.get("code")
                for data in storage.iter():
                    if data.get("code") == "charged_energy":
                        string_storage_level = data.text
                        splitted_storage_level = [str(Decimal(str_level)) for str_level in string_storage_level.split(",") if bool(str_level)]
                        storage_level[region][technology_code] = splitted_storage_level
                    
                        start_timeindex = data.get("start")
                        if start_timeindex.split("-")[0] == "1970":
                            start_timeindex = "{}-1-1_0:0".format(year)
                        storage_level[region][technology_code] = zero_appender(splitted_storage_level, start_timeindex, year)
                        
        

        total_slack = 0
        total_curtailment = 0
        for this_region in root.iter("region"):
            string_slack = [load.text for load in this_region.findall(".//region_internal/data[@code='remaining_residual_load']")]
            decimal_slack = [Decimal(slack_value) for slack_value in string_slack[0].split(",") if bool(slack_value)]
            positive_slack = [val for val in decimal_slack if val>=0]
            negative_slack = [val for val in decimal_slack if val<0]
            total_slack += sum(positive_slack)
            total_curtailment += sum(negative_slack)
        # print("slack ",total_slack)
        # print("curtailment", total_curtailment)



        # get links
        for this_link in root.iter("link"):
            link = this_link.get("code")
            link_dict[link] = {}
            for tr_conv in this_link.iter("tr-converter"):
                link_name = tr_conv.get("code")
                link_dict[link][link_name] = tr_conv
        
        energy_flow_dict = {}
        for this_link in root.iter("link"):
            link = this_link.get("code")
            for data in this_link.iter():
                if data.get("code") == "delivered_energy":
                    energy_flow_string = data.text
                    energy_flow_decimal = [Decimal(energy_flow) for energy_flow in energy_flow_string.split(",") if bool(energy_flow)]
            
                    direct_energy_flow = [i if i>0 else 0 for i in energy_flow_decimal]
                    reversed_link = "{}_{}".format(link.split("_")[1], link.split("_")[0])
                    reversed_energy_flow= [abs(i) if i<0 else 0 for i in energy_flow_decimal]

                    start_timeindex = data.get("start")
                    if start_timeindex.split("-")[0] == "1970":
                        start_timeindex = "{}-1-1_0:0".format(year)
                    energy_flow_dict[link] = zero_appender(direct_energy_flow, start_timeindex, year)
                    energy_flow_dict[reversed_link] = zero_appender(reversed_energy_flow, start_timeindex, year)


        #added capacity
        added_capacity_dict = added_capacity(scenario, year)


        #fixed cost, variable costs
        fopex_dict = {}
        vopex_dict = {}
        capex_dict = {}
        opex_types = ["converter", "storage"]
        for this_region in root.iter("region"):
            region = this_region.get("code")
            for opex_type in opex_types:
                for elem in this_region.iter(opex_type):
                    converter_storage = elem.get("code")
                    if converter_storage not in fopex_dict.keys():
                        fopex_dict[converter_storage] = []
                        vopex_dict[converter_storage] = []
                        capex_dict[converter_storage] = []
                    for data in elem.iter():
                        if data.get("code") == "fopex":
                            fopex = Decimal(data.text.split(",")[0])
                            fopex_dict[converter_storage].append(fopex)

                        if data.get("code") == "vopex":
                            vopex_list = [Decimal(i) for i in data.text.split(",") if bool(i)]
                            vopex_dict[converter_storage].append(sum(vopex_list))

                        if data.get("code") == "capex":
                            capex = Decimal(data.text.split(",")[0])
                            capex_dict[converter_storage].append(capex)
        
        for tech in fopex_dict.keys():
            fopex_dict[tech] = str(sum(fopex_dict[tech]))
        for tech in vopex_dict.keys():
            vopex_dict[tech] = str(sum(vopex_dict[tech]))
        
        #losses
        loss_dict = {}
        for this_region in root.iter("region"):
            region = this_region.get("code")
            for storage in this_region.iter("storage"):
                tech = storage.get("code")
                if tech not in loss_dict.keys():
                    loss_dict[tech] = []
                for data in storage.iter():
                    if data.get("code") == "energy_lost_by_transfer":
                        storage_loss = [Decimal(i) for i in data.text.split(",") if bool(i)]
                        loss_dict[tech].append(sum(storage_loss))
        

        loss_dict["transmission"] = []
        for this_link in root.iter("link"):                
            link_loss = [elem.text for elem in this_link.findall(".//tr-converter/data[@code='losses_']")]
            link_loss_decimal = [abs(Decimal(i)) for i in link_loss[0].split(",") if bool(i)]
            loss_dict["transmission"].append(sum(link_loss_decimal))


        for tech in loss_dict.keys():
            loss_dict[tech] = str(sum(loss_dict[tech]))


        # get global internal information
        for glob_internals in root.iter("model_internal"):
            if glob_internals.get("fitness"):
                system_cost = glob_internals.attrib["fitness"]
            if not math.isnan(float(system_cost)):
                system_cost = Decimal(system_cost)
            else:
                system_cost = Decimal(glob_internals.attrib["fopex"]) + Decimal(glob_internals.attrib["capex"]) + Decimal(glob_internals.attrib["vopex"])
            internal_item = glob_internals.get("code")
            glob_internal_dict[internal_item] = glob_internals

        # Extract analysed year
        analysis_year = glob_internal_dict["annual_electricity_price_EUR/GWh"].attrib["start"][0:4]

        big_dict = [region_list, analysis_year, str(system_cost), str(total_emission), str(total_generation),\
            str(total_slack), str(total_curtailment), emission_region_dict, electricity_generation_dict, input_energy_dict, output_energy_dict, storage_level,\
            energy_flow_dict,added_capacity_dict, fopex_dict, vopex_dict, capex_dict, loss_dict]
        
        return big_dict


