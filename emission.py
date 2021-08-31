from decimal import Decimal
import math


def get_emission(root, scenario_type):
    if scenario_type == "base":
        total_emission = 0
        emission_region_dict = {}
        for this_region in root.iter("region"):
            emission = [Decimal(emission.text[:-1])/10**9 for emission in this_region.findall(".//region_internal/data[@code='annual_co2_emissions']")]
            emission_region_dict[this_region.get("code")] = str(emission[0]) if not math.isnan(emission[0]) else 0
            if not math.isnan(emission[0]):
                total_emission += emission[0]

        return emission_region_dict, total_emission

    elif scenario_type == "variation":
        # emission_region_dict = {}
        # total_emission_dict = {}
        # for year in range(2016, 2051):
        #     emission_region_dict[year] = {}
        #     total_emission_dict[year] = 0
        
        # for this_region in root.iter("region"):
        #     region = this_region.get("code")
        #     for data in this_region.iter("region_internal"):
        #         if data.get("code") == "annual_co2_emissions":
        #             string_emission = data.text
        #             splitted_emission = [Decimal(em)/(10**9) for em in string_emission.split(",") if bool(em)]
        #             for i, em in enumerate(splitted_emission):
        #                 emission_region_dict[2016+i][region] = em

        #     for year in emission_region_dict:
        #         total_emission_dict[year] = sum(list(emission_region_dict[year].values()))
        
        # return emission_region_dict, total_emission_dict
        pass


    else:
        raise("Undefined scenario type!")