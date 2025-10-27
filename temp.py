#!/usr/bin/env python3

import pandas as pd 
import matplotlib.pyplot as plt 
df = pd.read_json("./data/divij.json")

# Converting the ts column to datetime object
df["ts"] = pd.to_datetime(df["ts"])

from utils.plot_sources.analysis_plots.artist_corelation_plot import  get_probability_matrix 
print(get_probability_matrix(df))
