#! /usr/bin/python3

import argparse
import glob
import pandas as pd
from tqdm import tqdm
import json

parser = argparse.ArgumentParser()
parser.add_argument("-i", help=\
    "set input traces directory path (D must directly contain folders with package names)", required=True)
parser.add_argument("-f", help=\
    "set number of first traces to process (default = inf)", required=False)

args = parser.parse_args()
path = args.i
if args.f:
    args.f = int(args.f)
if path[-1] != '/':
    path += '/'
df = pd.DataFrame()
dfs = []

def dfs_search(tree):
    ans = {
        'count': 1
        # TODO: taps / swipes count, ...
    }
    if tree is None:
        return {'count': 0}
    if 'children' not in tree:
        return ans
    for child in tree['children']:
        child_ans = dfs_search(child)
        ans['count'] += child_ans['count']
    return ans

for application in tqdm(glob.glob(path + "*")[:args.f]):
    for trace in glob.glob(application + "/trace*"):
        gestures_file = "trace/gestures.json"
        for view in glob.glob(trace + "/view_hierarchies/*.json"):
            # TODO: do not convert json to df, calculate values from dict and add them to THE ONLY main df as a row!
            df_temp = pd.read_json(view)
            if df_temp.empty:
                continue
            df_temp = df_temp.drop(['active_fragments', 'added_fragments'])
            df_temp = df_temp.drop(columns=['is_keyboard_deployed', 'request_id'])
            stats = dfs_search(df_temp['activity']['root'])
            for key in stats:
                df_temp[key] = [stats[key]]
            df_temp
            dfs.append(df_temp)

df = pd.concat(dfs, ignore_index=True)

print(df)
print('\n')
print('#' * 30, end='\n\n')
print('Mean number of elements in the GUI screen tree = ', df['count'].mean())
print()