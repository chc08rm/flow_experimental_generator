#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 20:37:34 2025

@author: raminder
"""
import questionary
import pandas as pd
def integerise(value):
    while type(value)!=int:
        try:
            int(value)
            return
        except ValueError:
            value=questionary.text("please enter an integer value:").ask()
def floaterise(value):
    while type(value)!=float:
        try:
            float(value)
            break
        except ValueError:
            value=questionary.text("please enter an numerical value:").ask()
df = pd.DataFrame(columns=["flow_rate", "mixer_stage", "restime_stage"])
pumps=questionary.select("how many pumps are you using?", choices=["1","2","3","4","5"]).ask()
n_pumps=int(pumps)
if n_pumps==1:
    reactor="fixed bed"
elif n_pumps!=1:
    for i in range(1,n_pumps):
        reactor=questionary.select(f"what sort of mixer is being used to connect pumps {i} and {i+1} ?", choices=["T-mixer","chip","CSTR","fixed-bed"]).ask()
# if n_pumps==1:
#     reactor="fixed bed"
# elif n_pumps!=1:
for i in range(n_pumps):
    flow_rate=questionary.text(f"what flow rate is pump {i+1} set to (in mL/min)? ").ask()
    floaterise(flow_rate)
    if i==(n_pumps-1):
        mixer=questionary.select(f"what sort of mixer is being used to connect pumps {i+1} and the output ?", choices=["T-mixer","chip","CSTR","fixed-bed"]).ask()
    elif i!=(n_pumps-1):
        mixer=questionary.select(f"what sort of mixer is being used to connect pumps {i+1} and {i+2} ?", choices=["T-mixer","chip","CSTR","fixed-bed"]).ask() 
    restime=questionary.text("what residence time is the combined stream held for (in seconds)? ").ask()
    integerise(restime)
    df.loc[len(df)]={"flow_rate":flow_rate,"mixer_stage":mixer, "restime_stage":restime}
print(df)