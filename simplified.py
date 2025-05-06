#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 20:37:34 2025

@author: raminder
"""

import questionary
questionary.select("what reactor design are you using?"
                   choice="tube, chip, CSTR, fixed-bed"
                   ).ask