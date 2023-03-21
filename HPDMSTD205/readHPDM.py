import pandas as pd
import cbor2
import json
import pint
import os
unit_file = {
  "F": "degF",
  "BTU/LBM": "Btu/pound",
  "Btu/lb": "Btu/pound",
  "LBM/HR": "pound/hr",
  "lb/h":"pound/hr",
  "W": "W",
  "PSIA": "psi",
  "psia": "psi",
  "R": "degR",
  "BTU/LBM/R": "Btu/pound/degR",
  "Btu/lb-R": "Btu/lbm/degR",
  "FT^3/LBM": "ft^3/pound",
  "ft3/lb": "ft^3/pound",
  "ft3": "ft^3",
  "RPM": "rpm",
  "INH2O": "inch_H2O_39F",
  "inH2O": "inch_H2O_39F",
  "WATER/DRY_AIR": "",
  "water/dryAir": "",
  "FT^3/HR": "ft^3/hr",
  "PSID": "psi",
  "BTU/H": "Btu/hr",
  "LBM": "lb",
  "LBM/FT^3": "lb/(ft^3)",
  "CFM": "cu_ft/min",
  "SCFM": "44.16*lb/min"
}
class STD205API:
    def __init__(self,control_file_name):
        #load control file
        my_file = open(control_file_name)#"RS0004_sample_control.json"
        con_data = json.load(my_file)
        my_file.close()
        lists = ["performance_map", "performance_map_cooling","performance_map_heating"]
        ureg = pint.UnitRegistry(system='SI')
        Q_ = ureg.Quantity
        self.std205out = con_data
        #search performance map/cooling map/heating map
        for u in range(len(lists)):
            if lists[u] in con_data["performance"].keys():
                #load HPDM
                my_file = open(con_data["performance"][lists[u]]["hpdm_out_file_name"], "r")
                data = my_file.read()
                my_file.close()
                #my_file = open("HPDMSTD205\unit_dic.json")
                unit_data = unit_file #json.load(my_file)
                #my_file.close()
                data_into_list = data.split("\n")
                n = len(data_into_list)
                k = 0
                while ((k<n) and (data_into_list[k].split("\t")[2]!="Output Variable List")):
                    k = k + 1
                i = k
                while ((i<n) and (data_into_list[i].split("\t")[0]!="Status")):
                    i = i + 1
                tk = [ [0]*(4) for r in range(i-k-2)]
                list_name_k = data_into_list[k]
                for j in range(i-k-2):
                    tk[j] = data_into_list[j+k+1].split("\t")
                dfk = pd.DataFrame(tk)
                dfk_f = pd.DataFrame(dfk.values[:,1:3]).transpose()
                dfk_f.columns = dfk_f.iloc[0]
                t = [ [0]*(22) for r in range(n-1-i-1)]
                list_name = data_into_list[i]
                for j in range(n-1-i-1):
                    t[j] = data_into_list[j+i+1].split("\t")
                df = pd.DataFrame(t)
                df.columns = list_name.split("\t")
                #load dic file
                data_j = con_data["performance"][lists[u]]
                jD_grid = data_j["grid_variables"]
                jD_look = data_j["lookup_variables"]
                title = []
                title_grid = []
                for k in jD_grid.keys():
                    title_grid.append(jD_grid[k]["hpdm_name"])
                    title.append(jD_grid[k]["hpdm_name"])
                for k in jD_look.keys():
                    title.append(jD_look[k]["hpdm_name"])
                df_focus = df[title].astype(float)
                df_focus = df_focus.sort_values(by=title_grid)
                for k in jD_grid.keys():
                    df_try = df_focus[jD_grid[k]["hpdm_name"]]
                list_fl = df_try.drop_duplicates().values.tolist()
                self.std205out["performance"][lists[u]]["grid_variables"] = {}
                for i in range(0,len(list_fl)):
                    name = jD_grid[k]["hpdm_name"].replace(":","-")
                    list_fl[i] = Q_(list_fl[i],unit_data[dfk_f[name][1]]).to_base_units().magnitude
                for k in jD_grid.keys():
                    self.std205out["performance"][lists[u]]["grid_variables"][k] = list_fl
                for k in jD_look.keys():
                    list_fl = df_focus[jD_look[k]["hpdm_name"]].values.tolist()
                self.std205out["performance"][lists[u]]["lookup_variables"] = {}
                for i in range(0,len(list_fl)):
                    name = jD_look[k]["hpdm_name"].replace(":","-")
                    list_fl[i] = Q_(list_fl[i],unit_data[dfk_f[name][1]]).to_base_units().magnitude
                for k in jD_look.keys():
                    self.std205out["performance"][lists[u]]["lookup_variables"][k] = df_focus[jD_look[k]["hpdm_name"]].values.tolist()
                self.std205out["performance"][lists[u]].pop("hpdm_out_file_name")
    def write(self,mode,output_name):
        if mode == "json":
            json_object = json.dumps(self.std205out, indent = 4) 
            with open(output_name, "w") as outfile:
                outfile.write(json_object)
        if mode == "cbor":
            data = cbor2.dumps(self.std205out)
            with open(output_name, "wb") as outfile:
                outfile.write(data)
