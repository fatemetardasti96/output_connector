def input_tech_techtype_extractor(tech_code):
    code_dict = {
        "PV1": [
            "solar radiation",
            "electricity",
            "photovoltaics",
            "rooftop"
        ],
        "PV2": [
            "solar radiation",
            "electricity",
            "photovoltaics",
            "utility"
        ],
        "PH_TURBINE":[
            "electricity",
            "electricity",
            "storage",
            "pumped"
        ],
        "BIOMASS_TURBINE":[
            "biomass",
            "electricity",
            "generator",
            "steam"
        ], 
        "GAS_TURBINE_CHP":[
            "natural gas",
            "electricity",
            "chp",
            "gas"
        ], 
        "GAS_TURBINE":[
            "natural gas",
            "electricity",
            "generator",
            "gas"
        ], 
        "CH4_CCTURBINE":[
            "natural gas",
            "electricity",
            "generator",
            "combined cycle"
        ], 
        "BIOMASS_FURNANCE_CHP":[
            "waste",
            "electricity",
            "chp",
            "steam"
        ], 
        "BIOMASS_FURNANCE":[
            "waste",
            "electricity",
            "generator",
            "steam"
        ], 
        "GASN_TURBINE":[
            "natural gas",
            "electricity",
            "generator",
            "combustion engine"
        ], 
        "GASN_TURBINE_CHP":[
            "natural gas",
            "electricity",
            "chp",
            "combustion engine"
        ],
        "BIO_CH4_TURBINE":[
            "biogas",
            "electricity",
            "generator",
            "combustion engine"
        ], 
        "LIGNITE_CHP":[
            "lignite",
            "electricity",
            "chp",
            "steam"
        ], 
        "CH4_CCTURBINE_CHP":[
            "natural gas",
            "electricity",
            "chp",
            "combined cycle"
        ], 
        "ROR":[
            "water",
            "electricity",
            "hydro turbine",
            "run-of-river"
        ], 
        "HARDCOAL_OCTURBINE_CHP":[
            "hard coal",
            "electricity",
            "chp",
            "steam"
        ], 
        "HARDCOAL_OCTURBINE":[
            "hard coal",
            "electricity",
            "generator",
            "steam"
        ], 
        "WIND_ONS":[
            "air",
            "electricity",
            "wind turbine",
            "onshore"
        ], 
        "WIND_OFF":[
            "air",
            "electricity",
            "wind turbine",
            "offshore"
        ], 
        "LIGHT_OIL":[
            "light oil",
            "electricity",
            "generator",
            "gas"
        ],
        "LIGHT_OIL_CHP":[
            "light oil",
            "electricity",
            "chp",
            "gas"
        ],
        "BAT1POWER":[
            "electricity",
            "electricity",
            "storage",
            "battery"
        ],
        "LIGNITE_OCTURBINE":[
            "lignite",
            "electricity",
            "generator",
            "steam"
        ],
        "GEO":[
            "heat",
            "electricity",
            "geothermal",
            "unknown"
        ],
        "NUCLEAR_TURBINE":[
            "uranium",
            "electricity",
            "nuclear",
            "unknown"
        ],
        "PH_storage":[
            "hydro energy",
            "electricity",
            "storage",
            "pumped"
        ],
        "Battery_Energy_storage":[
            "Battery_Energy",
            "electricity",
            "storage",
            "battery"
        ],
        "transmission":[
            "electricity",
            "electricity",
            "transmission",
            "hvac"
        ],
        "H2_ELECTROLYSER":[
            "electricity",
            "H2",
            "storage",
            "hydrogen gas"
        ],
        "H2_ELECTROLYSER_FC":[
            "electricity",
            "H2_FC",
            "storage",
            "hydrogen fuelcell"
        ],
        "FUEL_CELL":[
            "H2_FC",
            "electricity",
            "storage",
            "hydrogen fuelcell"
        ],
        "CCH2_TURBINE":[
            "H2",
            "electricity",
            "storage",
            "hydrogen gas"
        ],
        "H2_storage_gasturbine":[
            "electricity",
            "electricity",
            "storage",
            "hydrogen gas"
        ],
        "H2_storage_fuel_cell":[
            "electricity",
            "electricity",
            "storage",
            "hydrogen fuelcell"
        ],
        "TRANSMISSION_IMPORT":[
            "electricity",
            "electricity",
            "transmission",
            "trade import"
        ]

    }
    return code_dict[tech_code]
