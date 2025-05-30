#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 27 14:12:20 2025

@author: raminder
"""
import pandas as pd
def prep_gen(reaction):
    def temperature(reaction):
        t_list=[]
        for n in range(0, reaction.shape[0]):
            if pd.isnull(reaction.iloc[n]['t_int']):
                t_list.append(f"at a bath T of {reaction.iloc[n]['t_ext']}°C")
            else:
                t_list.append(f"at a bath T of {reaction.iloc[n]['t_ext']}°C, with an in-line T of {reaction.iloc[n]['t_int']}°C")
        t_list[0]=" "
        return t_list
    t_list=temperature(reaction)
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
def dir_scanner_out(value):#value is a path.
    import os #Import's here because you won't always need it. in the execution of generator.
    f_list=[]
    with os.scandir(value) as it:
        for entry in it:
            if '.csv' in entry.name.lower() and entry.is_file():
                f_list.append(entry.name)
    return f_list

for x in (dir_scanner_out('./')):
    x=pd.read_csv(x)
    if 'reagent_id' in x.columns:
        print(prep_gen(x))


    

    