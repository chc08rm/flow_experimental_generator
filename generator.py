#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 20:37:34 2025

@author: raminder
"""
import questionary
import pandas as pd
import argparse
import os
def question_list():
    def validate_float(value):
        try:
            input_text=float(value)  # Try converting to float
            return True  # Accept if successful
        except ValueError:
            return "Please enter a valid number (e.g., 3.14, -5, 1e3)."  # Error message
    def validate_integer(value):
        try:
            input_text=int(value)  # Try converting to float
            return True  # Accept if successful
        except ValueError:
            return "Please enter a whole number, e.g. 0, -78, 60"  # Error message
    def integerise(value):
        while type(value)!=int:
            try:
                value=int(value)
            except ValueError:
                value=questionary.text("Please enter a whole number, e.g. 0, -78, 60").ask()  # Error message
    def ordinal(n: int):#for more sylish questions
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
        return str(n) + suffix
    def list_to_adduct(value, connector):
        #convert to a string. for a well formatted mixer location, this is trivial.
        value=str(value)
        value=value.replace("['","") 
        value=value.replace("']","") 
        #If I want to use this to make a human-readable string, I specify "and" as an argument. 
        if connector!="and":
            value=value.replace(",",".")
        else:
            value=value.replace(","," and")
        value=value.replace("'","")
        return value
    def adduct_to_list(value):
        #makes "cartesian coordinates" from a mixer location.
       value=[n.replace('product of reaction between ',"") for n in value]
       value=[n.replace(' and ',".") for n in value]
       return value
    questionary.print("Let's start with some basic pump parameters.", style="bold italic fg:pink")
    filename=questionary.text("This script writes a CSV file containing the reaction parameters for databasing and ML purposes. What would you like to call it?").ask()
    pumps=questionary.select("how many pumps are you using?", choices=["2","3","4","5"]).ask()
    pumps=int(pumps)
    pump_list=[]
    lim_rate=None
    for n in range(pumps):
        questionary.print(f"Parameters for pump {n+1}:", style="bold italic fg:pink")
        reagent_id=questionary.text(f"Enter the SMILES string for the reagent pump {n+1} delivers:").ask()
        lim_reagent=questionary.confirm("Is this the limiting reagent?").skip_if(lim_rate).ask()
        if lim_reagent==True:
            reagent_eq=1
        else:
            reagent_eq=float(questionary.text("How many molar equivalents is the pump delivering?", validate=validate_float).ask())
        solvent=questionary.autocomplete("Enter the SMILES string for the solvent used", choices=["C1CCOC1","CCCCCC","CC#N","C(Cl)Cl"], meta_information={"C1CCOC1":"THF","CCCCCC":"Hexane","CC#N":"MeCN","C(Cl)Cl":"DCM"}, match_middle=True).ask()
        concentration=float(questionary.text("what is the reagent concentration in M?", validate=validate_float).ask())
        if lim_reagent==True:
            flow_rate=questionary.text("what flow rate is this reagent being delivered at (in mL min-1)?", validate=validate_float).ask()
            lim_rate=float(flow_rate)
            lim_conc=float(concentration)
        else:
            try:
                flow_rate=((lim_conc*lim_rate)/concentration)*(reagent_eq)
                flow_rate=round(flow_rate,3)
                print(f"The flow rate is assumed to be {flow_rate} mL min-1.")
            except:
                flow_rate=float(questionary.text("what flow rate is this reagent being delivered at (in mL min-1)?", validate=validate_float).ask())
        pump_params={'reagent_id':reagent_id,'reagent_eq':reagent_eq,'solvent':solvent,'concentration':concentration,'flow_rate':flow_rate,'lim_reagent':lim_reagent}  
        pump_list.append(pump_params)
    pump_list=pd.DataFrame(pump_list)
    a=pump_list["reagent_id"].tolist()
    mixer_list=[{"mixer_loc":pd.NA,"mixer_type":pd.NA,"t_diam":pd.NA,"res_time":pd.NA,"t_ext":pd.NA,"t_int":pd.NA, "pressure_regulator":pd.NA, "pressure_psi":pd.NA}]
    questionary.print("And now for the mixing elements.", style="bold italic fg:pink")
    pressure_regulator=questionary.confirm("Was a back pressure regulator attached to the reactor output?").ask()
    mixer_list[0]["pressure_regulator"]=pressure_regulator
    if pressure_regulator:
        pressure_psi=questionary.text("What pressure (in psi) was the regulator set to?", validate=validate_integer).ask()
        mixer_list[0]["pressure_psi"]=int(pressure_psi)
    for n in range(1,pump_list.shape[0]):
            mixer_loc=questionary.checkbox(f"what inputs does the {ordinal(n)} mixer combine?", choices=a, validate=lambda num:  True if len(num)==2 else "Only 2 streams may be combined at a given mixing junction" ).ask()
            a.append(f"product of reaction between {list_to_adduct(mixer_loc,'and')}")
            mixer_type=questionary.select("what type of mixer is being used?", choices=["T-mixer","chip","CSTR","fixed-bed","static"]).ask()
            if mixer_type=="T-mixer":
                t_diam=questionary.select("what diameter is the T-piece (in uM)?", choices=["250","500","1600"]).ask()
            else:
                t_diam=pd.NA
            res_time=questionary.text("what residence time is the combined stream held for (in seconds)?").ask()
            #something is up with the async library, hence the explicit loop here. 
            while type(res_time)!=float:
                try:
                    res_time=float(res_time)
                except:
                    res_time=questionary.text("Please enter a valid number: ").ask()
            t_ext=questionary.text("What is the bath/block temperature at this stage (in °C)?", validate=validate_integer).ask()
            integerise(t_ext)
            t_int=questionary.confirm("Did you have inline temperature data for this part of the reactor?").ask()
            if t_int == True:
                t_int=questionary.text("What is the inline temperature at this stage (in °C)?", validate=validate_integer).ask()
                integerise(t_ext)
            else:
                t_int=pd.NA
            mixer_loc=adduct_to_list(mixer_loc)
            mixer_params={"mixer_loc":mixer_loc, "mixer_type":mixer_type, "t_diam":t_diam, "res_time":res_time, "t_ext":t_ext, "t_int":t_int}
            mixer_list.append(mixer_params)
    mixer_list=pd.DataFrame(mixer_list)
    questionary.print("And finally for the collection, workup conditions and yield.", style="bold italic fg:pink")
    aux_params=questionary.form(
        collection_into=questionary.text("What was your isolation procedure? Write this part as as you would a normal experimental."),
        run_time=questionary.text("How long did you collect for (in mins)? Leave at 0 if you didn't record a time.", default='0', validate=validate_float),
        collection_mode=questionary.select("What mode of collection did you use?", choices=["""Steady state — wait for at least 3   residence times of material to be passed through the reactor before collecting""", """Collecting all — collect all of the injectable quantity of limiting reagent after excess reagent lines have been primed""","Unknown"]),
        product_1_smiles=questionary.text("Please enter the SMILES string for the major product obtained. If you don't know what it was (e.g. a complex mixture was formed), leave this blank."),
        product_1_yield=questionary.text("What was your yield (or conversion)?", validate=validate_float),
        product_1_yieldtype=questionary.select("How was this yield determined?", choices=["Weight","LCMS", "1H NMR", "Titration"]),
        additional_info=questionary.autocomplete("Add in any additional comments here. You may also add your analytical data.", match_middle=True, choices=["Ultrasonication was used throughout the run to minimise fouling.", "Where appropriate, reagent solutions were pre-dried."])
    ).ask()
    # A bit of post processing
    if "Steady" in aux_params["collection_mode"]: 
        aux_params["collection_mode"]="STEADY_STATE"
    elif "Collecting" in aux_params["collection_mode"]:
        aux_params["collection_mode"]="COLLECT_ALL_PRIME"
    else:
        aux_params["collection_mode"]="UNSPECIFIED"
    if aux_params['run_time']!=None:
        (aux_params['run_time'])=float(aux_params['run_time'])
    aux_params=pd.DataFrame([aux_params])
    reaction=pd.concat([pump_list,mixer_list,aux_params], axis=1)
    return reaction,filename     
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
    def mole_maker(n):
        run_time=float(reaction.iloc[0]['run_time'])
        conc=float(reaction.iloc[n]['concentration'])
        flow_rate=float(reaction.iloc[n]['flow_rate'])
        mmoles=round(conc*run_time*flow_rate, 2)
        return mmoles
    # Initialize a list to collect all description parts
    description_parts = []
    
    # Initial reaction description
    reaction_desc = (
        f"In a flow reactor were combined {reaction.iloc[0]['reagent_id']} "
        f"({mole_maker(0)} mmol, {reaction.iloc[0]['reagent_eq']} eq., {reaction.iloc[0]['concentration']}M in "
        f"{reaction.iloc[0]['solvent']}) dosed in at a flow rate of {reaction.iloc[0]['flow_rate']} mL min⁻¹ "
        f"and {reaction.iloc[1]['reagent_id']} ({mole_maker(1)} mmol, {reaction.iloc[1]['reagent_eq']} eq., "
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
                f"{t_list[1]}. "
            )
        elif reaction.iloc[1]['mixer_type'] == "CSTR":
            mixer_desc = (
                f"to a {reaction.iloc[1]['mixer_type']}. The resulting mixture was held for an MRT of "
                f"{reaction.iloc[1]['res_time']} s {t_list[1]}. "
            )
        else:
            mixer_desc = (
                f"to a {reaction.iloc[1]['mixer_type']} mixer. The resulting mixture was held for a residence time of "
                f"{reaction.iloc[1]['res_time']} s {t_list[1]}. "
            )
        if reaction.iloc[0]['pressure_regulator']:
            mixer_desc+=f"""A back pressure regulator set to {reaction.iloc[0]['pressure_psi']} psi was attached to the reactor output line and the output was collected into {reaction.iloc[0]['collection_into']}."""
        else:
            mixer_desc+=f"prior to being collected into {reaction.iloc[0]['collection_into']}."
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
            f"combined with {reaction.iloc[n]['reagent_id']} ({mole_maker(n)} mmol, {reaction.iloc[n]['reagent_eq']} eq., "
            f"{reaction.iloc[n]['concentration']}M in {reaction.iloc[n]['solvent']}) dosed in at a flow rate of "
            f"{reaction.iloc[n]['flow_rate']} mL min⁻¹"
        )
        loop_descriptions.append(reagent_desc)
        
        mixer_part = ""
        if reaction.iloc[n]['mixer_type'] == "T-mixer":
            mixer_part = (
                f"to a {reaction.iloc[n]['mixer_type']}(φ={reaction.iloc[n]['t_diam']} µm). "
                f"The resulting mixture was held for a residence time of {reaction.iloc[n]['res_time']} s {t_list[n]}, "  
            )
        elif reaction.iloc[n]['mixer_type'] == "CSTR":
            mixer_part = (
                f"to a {reaction.iloc[n]['mixer_type']}. The resulting mixture was held for an MRT of "
                f"{reaction.iloc[n]['res_time']} s {t_list[n]},"
            )
        else:
            mixer_part = (
                f"to a {reaction.iloc[n]['mixer_type']} mixer. The resulting mixture was held for a residence time of "
                f"{reaction.iloc[n]['res_time']} s {t_list[n]},"
            )
        mixer_part+="prior to being"
        loop_descriptions.append(mixer_part)
    
        if n == reaction.index[-1]:
            if reaction.iloc[0]['pressure_regulator']:
                 loop_descriptions.append(f"passed through a back pressure regulator set to {reaction.iloc[0]['pressure_psi']} psi. The output was collected into {reaction.iloc[0]['collection_into']}.")
            else:
                loop_descriptions.append(f"collected into {reaction.iloc[0]['collection_into']}.")          
    description_parts.extend(loop_descriptions)
    
    # Collection mode
    collection_desc = ""
    if reaction.iloc[0]["collection_mode"] == "STEADY_STATE":
        collection_desc += "Steady state collection was performed by infusing at least 3 residence times of all feed solutions through the reactor. Yields are reported on this basis."
    elif reaction.iloc[0]["collection_mode"] == "COLLECT_ALL_PRIME":
        prime_parts = [f"All of the output was collected following initiation of the {reaction.loc[reaction['lim_reagent'] == True, 'reagent_id'].squeeze()} pump. The"]
        for n in range(0, reaction.shape[0]):
            if reaction.iloc[n]['reagent_eq'] > 1:
                prime_parts.append(f"{reaction.iloc[n]['reagent_id']}, ")
        prime_parts.append(f"pump(s) were initiated and run for at least 20 s prior to initiation of the {reaction.loc[reaction['lim_reagent'] == True, 'reagent_id'].squeeze()} pump.")
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
    additional_info=""
    if reaction.iloc[0]["additional_info"] is not None:
        additional_info=reaction.iloc[0]["additional_info"]
    description_parts.append(additional_info)
    # Combine all parts into a single string
    final_description = " ".join(description_parts)
    return final_description
def dir_scanner_out(value):#value is a path.
    # Make a list of csvs in the working directory.
    with os.scandir(value) as file_list:
        csv_list=[os.path.abspath(entry)
                  for entry in file_list 
                  if '.csv' in entry.name.lower()
                  and '.txt' not in entry.name.lower()
                  and entry.is_file()
                  ]
    # Make a dictionary into which the ELN reference is the key and the prep/experimental is the value
    directory_output={}
    for csv in csv_list:
        df=pd.read_csv(csv)
        if 'reagent_id' in df.columns: #can the CSV be accepted by prep_gen?
            #populate the dictrionary and use it to output to text files.
            directory_output.update({csv:f'{prep_gen(df)}'})
    for filename, prep in directory_output.items():
        with open(f"{filename.replace('.csv','')}.txt", "w", encoding="utf-8") as filename:
            filename.write(f'{prep}')
    return directory_output #and here's the dictionary if you want it.
#"`-._,-'"`-._,-'"`-._,-'"`-._,-'
#end definitions
#"`-._,-'"`-._,-'"`-._,-'"`-._,-'
parser = argparse.ArgumentParser(description='Program with interactive/non-interactive modes')
parser.add_argument('-n', '--non-interactive', 
                    nargs='?',         # Capture 0 or 1 arguments
                    const=os.getcwd(),        # Default value when flag is used without argument
                    default=None,      # Value when flag is not used
                    metavar='DIRECTORY',  # Display name for argument in help
                    help='Enable non-interactive mode. Optionally specify directory (default: "./")')

args = parser.parse_args()

if args.non_interactive is not None:
    # Non-interactive mode
    directory = os.path.abspath(args.non_interactive)
    print(f"Running in non-interactive mode with directory: {directory}")
    dir_scanner_out(directory)
    print("Done!")
else:
    # Interactive mode
    start=questionary.confirm("I can take a pre-defined CSV file in a valid format and print an experimental if you have one. Do you have a pre-saved CSV file?").ask()
    if start:
        filename=questionary.path("Choose a valid file:", validate=lambda text: True if ".csv" in text else "Please choose a valid file type.").ask()
        reaction=pd.read_csv(f'{filename}')
        while 'reagent_id' not in reaction.columns:
            f_name=questionary.path("This CSV is not formatted correctly. Try another file.", validate=lambda text: True if ".csv" in text           else "Please choose a valid file type.").ask()
            reaction=pd.read_csv(f"{f_name}")
        print(prep_gen(reaction))
    if start == False:
        reaction=question_list()
        print(prep_gen(reaction[0]))
        reaction[0].to_csv(f"{os.getcwd()}/{reaction[1]}.csv")
        with open(f'{os.getcwd()}/{reaction[1]}.txt', "w", encoding="utf-8") as f:
            f.write(prep_gen(reaction[0]))
