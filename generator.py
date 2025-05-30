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
            value=questionary.text("Please enter a whole number, e.g. 0, -78, 60").ask()  # Error message
def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix
def question_list():
    questionary.print("Let's start with some basic pump parameters.", style="bold italic fg:pink")
    filename=questionary.text("This script writes a CSV file containing the reaction parameters for databasing and ML purposes. What would you like to call it?").ask()
    pumps=questionary.select("how many pumps are you using?", choices=["2","3","4","5"]).ask()
    pumps=int(pumps)
    pump_list=[]
    for n in range(pumps):
        questionary.print(f"Parameters for pump {n+1}:", style="bold italic fg:pink")
        pump_params=questionary.form(
            reagent_id=questionary.text(f"Enter the SMILES string for the reagent pump {n+1} delivers:"),
            reagent_eq=questionary.text("How many molar equivalents is the pump delivering? (use 1 for the limiting reagent)", validate=validate_float),
            solvent=questionary.text("Enter the SMILES string for the solvent used"),
            concentration=questionary.text("what is the reagent concentration in M?", validate=validate_float),
            flow_rate=questionary.text("what flow rate is this reagent being delivered at (in mL min-1)?", validate=validate_float)
            ).ask()
        pump_list.append(pump_params)
    pump_list=pd.DataFrame(pump_list)
    a=pump_list["reagent_id"].tolist()
    a.insert(0,"intermediate")
    mixer_list=[{"mixer_loc":pd.NA,"mixer_type":pd.NA,"t_diam":pd.NA,"res_time":pd.NA,"t_ext":pd.NA,"t_int":pd.NA}]
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
                    res_time=questionary.text("Please enter a valid number: ").ask()
            t_ext=questionary.text("What is the bath/block temperature at this stage (in °C)?").ask()
            integerise(t_ext)
            t_int=questionary.confirm("Did you have inline temperature data for this part of the reactor?").ask()
            if t_int == True:
                t_int=questionary.text("What is the inline temperature at this stage (in °C)?").ask()
                integerise(t_ext)
            else:
                t_int=pd.NA
            mixer_params={"mixer_loc":mixer_loc, "mixer_type":mixer_type, "t_diam":t_diam, "res_time":res_time, "t_ext":t_ext, "t_int":t_int}
            mixer_list.append(mixer_params)
    mixer_list=pd.DataFrame(mixer_list)
    questionary.print("And finally for the collection, workup conditions and yield.", style="bold italic fg:pink")
    aux_params=questionary.form(
        collection_into=questionary.text("What did you collect into? e.g. NH₄Cl, an inerted vial, etc."),
        collection_mode=questionary.select("What mode of collection did you use?", choices=["""Steady state — wait for at least 3   residence times of material to be passed through the reactor before collecting""", """Collecting all — collect all of the injectable quantity of limiting reagent after excess reagent lines have been primed""","Unknown"]),
        product_1_smiles=questionary.text("Please enter the SMILES string for the major product obtained. If you don't know what it was (e.g. a complex mixture was formed), leave this blank."),
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
    return reaction     
def temperature(reaction):
    t_list=[]
    for n in range(0, reaction.shape[0]):
        if pd.isnull(reaction.iloc[n]['t_int']):
            t_list.append(f"at a bath T of {reaction.iloc[n]['t_ext']}°C")
        else:
            t_list.append(f"at a bath T of {reaction.iloc[n]['t_ext']}°C, with an in-line T of {reaction.iloc[n]['t_int']}°C")
    t_list[0]=" "
    return t_list
def prep_gen(reaction, t_list):
    # Initialize a list to collect all description parts
    description_parts = []
    
    # Initial reaction description
    reaction_desc = (
        f"In a flow reactor were combined {reaction.iloc[0]['reagent_id']} "
        f"({reaction.iloc[0]['reagent_eq']} eq., {reaction.iloc[0]['concentration']}M in "
        f"{reaction.iloc[0]['solvent']}) dosed in at a flow rate of {reaction.iloc[0]['flow_rate']} mL min⁻¹ "
        f"and {reaction.iloc[1]['reagent_id']} ({reaction.iloc[1]['reagent_eq']} eq., "
        f"{reaction.iloc[1]['concentration']}M in {reaction.iloc[1]['solvent']}) dosed in at a flow rate of "
        f"{reaction.iloc[1]['flow_rate']} mL min⁻¹"
    )
    description_parts.append(reaction_desc)
    
    # Mixer parameters
    mixer_desc = ""
    if reaction.shape[0] == 2:
        if reaction.iloc[1]['mixer_type'] == "T-mixer":
            mixer_desc = (
                f"to a {reaction.iloc[1]['mixer_type']}(φ={reaction.iloc[1]['t_diam']} µm). "
                f"The resulting mixture was held for a residence time of {reaction.iloc[1]['res_time']} s, "
                f"{t_list[1]}, prior to being collected into {reaction.iloc[0]['collection_into']}."
            )
        elif reaction.iloc[1]['mixer_type'] == "CSTR":
            mixer_desc = (
                f"to a {reaction.iloc[1]['mixer_type']}. The resulting mixture was held for an MRT of "
                f"{reaction.iloc[1]['res_time']} s {t_list[1]}, prior to being collected into "
                f"{reaction.iloc[0]['collection_into']}."
            )
        else:
            mixer_desc = (
                f"to a {reaction.iloc[1]['mixer_type']}. The resulting mixture was held for a residence time of "
                f"{reaction.iloc[1]['res_time']} s {t_list[1]}, prior to being collected into "
                f"{reaction.iloc[0]['collection_into']}."
            )
    elif reaction.shape[0] > 2:
        base = "to a "
        if reaction.iloc[1]['mixer_type'] == "T-mixer":
            base += f"{reaction.iloc[1]['mixer_type']}(φ={reaction.iloc[1]['t_diam']} µm). "
        else:
            base += f"{reaction.iloc[1]['mixer_type']}. "
        
        base += (
            f"The resulting mixture was held for {'a residence time' if reaction.iloc[1]['mixer_type'] != 'CSTR' else 'an MRT'} "
            f"of {reaction.iloc[1]['res_time']} s {t_list[1]}, prior to being"
        )
        mixer_desc = base
    
    description_parts.append(mixer_desc)
    
    # Additional reagents loop
    loop_descriptions = []
    for n in range(2, reaction.shape[0]):
        reagent_desc = (
            f"combined with {reaction.iloc[n]['reagent_id']} ({reaction.iloc[n]['reagent_eq']} eq., "
            f"{reaction.iloc[n]['concentration']}M in {reaction.iloc[n]['solvent']}) dosed in at a flow rate of "
            f"{reaction.iloc[n]['flow_rate']} mL min⁻¹"
        )
        loop_descriptions.append(reagent_desc)
        
        mixer_part = ""
        if reaction.iloc[n]['mixer_type'] == "T-mixer":
            mixer_part = (
                f"to a {reaction.iloc[n]['mixer_type']}(φ={reaction.iloc[n]['t_diam']} µm). "
                f"The resulting mixture was held for a residence time of {reaction.iloc[n]['res_time']} s {t_list[n]}, "
                "prior to being"
            )
        elif reaction.iloc[n]['mixer_type'] == "CSTR":
            mixer_part = (
                f"to a {reaction.iloc[n]['mixer_type']}. The resulting mixture was held for an MRT of "
                f"{reaction.iloc[n]['res_time']} s {t_list[n]}, prior to being"
            )
        else:
            mixer_part = (
                f"to a {reaction.iloc[n]['mixer_type']}. The resulting mixture was held for a residence time of "
                f"{reaction.iloc[n]['res_time']} s {t_list[n]}, prior to being"
            )
        loop_descriptions.append(mixer_part)
    
        if n == reaction.index[-1]:
            loop_descriptions.append(f"collected into {reaction.iloc[0]['collection_into']}.")
    
    description_parts.extend(loop_descriptions)
    
    # Collection mode
    collection_desc = ""
    if reaction.iloc[0]["collection_mode"] == "STEADY_STATE":
        collection_desc = "Steady state collection was performed by infusing at least 3 residence times of all feed solutions through the reactor. Yields are reported on this basis."
    elif reaction.iloc[0]["collection_mode"] == "COLLECT_ALL_PRIME":
        prime_parts = ["All of the output following injection of the limiting reagent was collected"]
        for n in range(0, reaction.shape[0]):
            if reaction.iloc[n]['reagent_eq'] > 1:
                prime_parts.append(f"The {reaction.iloc[n]['reagent_id']}, ")
        prime_parts.append("pump(s) were initiated and run for at least 20 s prior to initiation of the limiting reagent pump.")
        collection_desc = " ".join(prime_parts)
    
    description_parts.append(collection_desc)
    
    # Yield description
    yield_desc = "No major product was identified."
    if float(reaction.iloc[0]["product_1_yield"]) > 0:
        yield_desc = (
            f"{reaction.iloc[0]['product_1_smiles']} was obtained in {reaction.iloc[0]['product_1_yield']}% yield "
            f"by {reaction.iloc[0]['product_1_yieldtype']} measurement."
        )
    description_parts.append(yield_desc)
    
    # Combine all parts into a single string
    final_description = " ".join(description_parts)
    return final_description
start=questionary.confirm("I can take a pre-defined CSV file in a valid format and print an experimental if you have one. Do you have a pre-saved CSV file?").ask()
if start == True:
    filename=questionary.path("Choose a valid file:", validate=lambda text: True if ".csv" in text else "Please choose a valid file type.").ask()
    reaction=pd.read_csv(f'{filename}')
    while 'reagent_id' not in reaction.columns:
        f_name=questionary.path("This CSV is not formatted correctly. Try another file.", validate=lambda text: True if ".csv" in text           else "Please choose a valid file type.").ask()
        reaction=pd.read_csv(f"{f_name}")
if start == False:
    reaction=question_list()
#"`-._,-'"`-._,-'"`-._,-'"`-._,-'
#Here's the output
#"`-._,-'"`-._,-'"`-._,-'"`-._,-'
t_list=temperature(reaction)
print(prep_gen(reaction, t_list))
with open('output.txt', "w", encoding="utf-8") as f:
    f.write(prep_gen(reaction,t_list))
