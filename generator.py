#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 20:37:34 2025

@author: raminder
"""

import questionary
pumps=questionary.select("how many pumps are you using?", choices=["1","2","3","4","5"]).ask()
n_pumps=int(pumps)
if n_pumps==1:
    reactor="fixed bed"
elif n_pumps!=1:
    for i in range(1,n_pumps):
        reactor=questionary.select(f"what sort of mixer is being used to connect pumps {i} and {i+1} ?", choices=["T-mixer","chip","CSTR","fixed-bed"]).ask()