# output_connector

Parameters to adjust in runme.py:

SCENARIO_ID is the scenario ID from input side and must be equal to the input ID that the output file is generated from. This is used for generating
added capacities.

dirpath could be adjusted based on input result version. Current version: v9

AnalysedResult.xml should have be saved in such a diectory structure:

```
-Resultfiles
|
|--v9
   |
   |--Base-Scenario
      |
      |--AnalysedResult_2016.xml
      |--AnalysedResult_2030.xml
      |--AnalysedResult_2050.xml
   |
   |--Variation-Scenario
```

## Create virtual environment

`python3 -m venv ./venv`


## Activate virtual environment

`source ./venv/bin/activate`

## Install requirements

`pip install -r requirements.txt`

## Run

`python runme.py`

