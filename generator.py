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
def integerise(value):
    while type(value)!=int:
        try:
            value=int(value)
        except ValueError:
            value=input("Please enter a whole number, e.g. 0, -78, 60")  # Error message
def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix
filename=questionary.text("This script writes a CSV file containing the reaction parameters for databasing and ML purposes. What would you like to call it?").ask()
questionary.print("Let's start with some basic pump parameters.", style="bold italic fg:pink")
pumps=questionary.select("how many pumps are you using?", choices=["2","3","4","5"]).ask()
pumps=int(pumps)
pump_list=[]
for n in range(pumps):
    questionary.print(f"Parameters for pump {n+1}:", style="bold italic fg:pink")
    pump_params=questionary.form(
        reagent_id=questionary.text("Enter the SMILES string for the reagent pump delivers:"),
        reagent_eq=questionary.text("How many molar equivalents is the pump delivering? (use 1 for the limiting reagent)", validate=validate_float),
        solvent=questionary.text("Enter the SMILES string for the solvent used"),
        concentration=questionary.text("what is the reagent concentration in M?", validate=validate_float),
        flow_rate=questionary.text("what flow rate is this reagent being delivered at (in mL min-1)?", validate=validate_float)
        ).ask()
    pump_list.append(pump_params)
pump_list=pd.DataFrame(pump_list)
a=pump_list["reagent_id"].tolist()
a.insert(0,"intermediate")
mixer_list=[{"mixer_loc":"null","mixer_type":"null","t_diam":"null","res_time":"null","t_bath":"null","t_inline":"null"}]
questionary.print("And now for the mixing elements.", style="bold italic fg:pink")
for n in range(1,pump_list.shape[0]):
        mixer_loc=questionary.checkbox(f"what inputs does the {ordinal(n)} mixer combine? If one of them is an intermediate, choose the intermediate and intercepting reagent as options.", choices=a, validate=lambda num:  True if len(num)==2 else "Only 2 streams may be combined at a given mixing junction" ).ask()
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
        t_bath=questionary.text("What is the bath temperature at this stage (in °C)?").ask()
        integerise(t_bath)
        t_inline=questionary.confirm("Did you have inline temperature data for this part of the reactor?").ask()
        if t_inline == True:
            t_inline=questionary.text("What is the inline temperature at this stage (in °C)?").ask()
            integerise(t_bath)
        mixer_params={"mixer_loc":mixer_loc, "mixer_type":mixer_type, "t_diam":t_diam, "res_time":res_time, "t_bath":t_bath, "t_inline":t_inline}
        mixer_list.append(mixer_params)
mixer_list=pd.DataFrame(mixer_list)
questionary.print("And finally for the collection, workup conditions and yield.", style="bold italic fg:pink")
aux_params=questionary.form(
    collection_into=questionary.text("What did you collect into? e.g. NH₄Cl, an inerted vial, etc."),
    collection_mode=questionary.select("What mode of collection did you use?", choices=["""Steady state — wait for at least 3   residence times of material to be passed through the reactor before collecting""", """Collecting all — collect all of the injectable quantity of limiting reagent after excess reagent lines have been primed""","Unknown"]),
    product_1_smiles=questionary.text("Please enter the SMILES string for the major product obtained"),
    product_1_yield=questionary.text("What was your yield?", validate=validate_float),
    product_1_yieldtype=questionary.select("How was this yield determined?", choices=["Weight","LCMS", "1H NMR", "Titration"])
).ask()
if "Steady" in aux_params["collection_mode"]: 
    aux_params["collection_mode"]="STEADY_STATE"
elif "Collecting" in aux_params["collection_mode"]:
    aux_params["collection_mode"]="COLLECT_ALL_PRIME"
else:
    aux_params["collection_mode"]="UNSPECIFIED"
aux_params=pd.DataFrame([aux_params])
reaction=pd.concat([pump_list,mixer_list,aux_params], axis=1)
reaction.to_csv(f"{filename}.csv")
#Here's the output


        