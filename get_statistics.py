#! /usr/bin/python3

import argparse
import glob
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("-i", help=\
    "set input traces directory path (D must directly contain folders with package names)", required=True)
args = parser.parse_args()
path = args.i

if path[-1] != '/':
    path += '/'

df = pd.DataFrame()
dfs = []

for application in glob.glob(path + "*")[:30]:
    for trace in glob.glob(application + "/trace*"):
        gestures_file = "trace/gestures.json"
        for view in glob.glob(trace + "/view_hierarchies/*.json"):
            df_temp = pd.read_json(view)
            dfs.append(df_temp)

df = pd.concat(dfs, ignore_index=True)

# TODO: explore 'activity' column -- GUI elements tree to obtain statistics

print(df)