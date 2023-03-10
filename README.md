# HPDM-STD205

This is for HPDM to ASHRAE standard 205 conversion. Learn more about ASHRAE Standard 205: https://data.ashrae.org/standard205/<br />
This is a trial version.<br />
"Out_cool.xls" or "Out_heat.xls" is the output file ("Out.xls") generated by ORNL Heat Pump Design Model (HPDM). HPDM and its tutorial can be accessed from [HPDM official website](https://hpdmflex.ornl.gov/hpdm/wizard/welcome.php/).<br />
## Install
`pip install HPDMSTD205`
## Required packages
This API requires the following packages:<br />
1. [pandas](https://github.com/pandas-dev/pandas/)<br />
2. [json](https://github.com/nlohmann/json/)<br />
3. [pint](https://github.com/hgrecco/pint/)<br />
## How to run examples
1. Copy "readHPDM.py" and "unit_dic.json" to the example "RS" folder (e.g., RS0004);
2. Substitute "RS0004_sample_control.json" with master file name;
3. Substitute "std205_out.json" with wantted output name.<br />
`STD205API("RS0004_sample_control.json").write("std205_out.json")`
