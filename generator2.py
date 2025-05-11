#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 20:37:34 2025

@author: raminder
"""
import questionary
import pandas as pd
def validate_float(input_text):
    try:
        float(input_text)  # Try converting to float
        return True  # Accept if successful
    except ValueError:
        return "Please enter a valid number (e.g., 3.14, -5, 1e3)."  # Error message
t_sizes=["250", "500", "1600"]
#df = pd.DataFrame(columns=["flow_rate", "mixer_stage", "restime_stage"])
pumps=questionary.select("how many pumps are you using?", choices=["1","2","3","4","5"]).ask()
pumps=int(pumps)
pump_list=[]
for n in range(pumps):
    print(f"Parameters for pump {n+1}:")
    pump_params=questionary.form(
        reagent_id=questionary.text("enter the SMILES string for the reagent pump delivers:"),
        solvent=questionary.text("What solvent is this reagent in?"),
        concentration=questionary.text("what is its concentration in M?", validate=validate_float),
        flow_rate=questionary.text("what flow rate is this reagent being delivered at (in mL min-1)?", validate=validate_float)
        ).ask()
    pump_list.append(pump_params)
pump_list=pd.DataFrame(pump_list)
# print(pump_list)
a=pump_list["reagent_id"].tolist()
a.insert(0,"intermediate")
mixer_list=[]
for n in range(1,pump_list.shape[0]):
        mixer_loc=questionary.checkbox("what inputs does the mixer combine? If one of them is an intermediate, choose the intermediate and intercepting reagent as options.", choices=a, validate=lambda num:  True if len(num)==2 else "Only 2 streams may be combined at a mixing junction" ).ask()
        mixer_type=questionary.select("what type of mixer is being used?", choices=["T-mixer","chip","CSTR","fixed-bed","static"]).ask()
        if mixer_type=="T-mixer":
            t_diam=questionary.select("what diameter is the T-piece (in uM)?", choices=["250","500","1600"]).ask()
        else:
            t_diam=0
        res_time=questionary.text("what residence time is the combined stream held for (in seconds)?").ask()
        #something is up with the async library, hence the explicit loop here. 
        while type(res_time)!=float:
            try:
                res_time=float(res_time)
            except:
                res_time=input("Please enter a valid number: ")
        mixer_params={"mixer_loc":mixer_loc, "mixer_type":mixer_type, "t_diam":t_diam, "res_time":res_time}
        mixer_list.append(mixer_params)
mixer_list=pd.DataFrame(mixer_list)
# print(mixer_list)        
# pump_list.to_csv("pump_list.csv")
# mixer_list.to_csv("mixer_list.csv")