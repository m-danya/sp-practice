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
    "set number of first traces to process (default: process all of them)", required=False)

args = parser.parse_args()
path = args.i
if args.f:
    args.f = int(args.f)
if path[-1] != '/':
    path += '/'

element_names = {}

def gui_tree_dfs(tree):
    ans = {
        'count': 0,
        'clickable_elements': 0,
    }
    if tree is None:
        return ans
    ans['count'] = 1
    ans['clickable_elements'] = int(tree['clickable'])
    if tree['class'] in element_names:
        element_names[tree['class']] += 1
    else:
        element_names[tree['class']] = 1

    if 'children' not in tree:
        return ans
    for child in tree['children']:
        child_ans = gui_tree_dfs(child)
        ans['count'] += child_ans['count']
        ans['clickable_elements'] += child_ans['clickable_elements']
    return ans

gui_rows = []
traces_rows = []

for application in tqdm(glob.glob(path + "*")[:args.f]):
    for trace in glob.glob(application + "/trace*"):
        with open(trace + "/gestures.json") as json_file:
            gestures = json.load(json_file)
        taps = 0
        swipes = 0
        for screen in gestures:
            if len(gestures[screen]) > 1:
                swipes += 1
            else:
                taps += 1
        traces_rows.append({'taps': taps, 'swipes': swipes})
        for view in glob.glob(trace + "/view_hierarchies/*.json"):
            with open(view) as json_file:
                current_json = json.load(json_file)
            if not current_json:
                continue
            stats = gui_tree_dfs(current_json['activity']['root'])
            stats['activity_name'] = current_json['activity_name']
            gui_rows.append(stats)

if not traces_rows:
    print('No traces found!')
    exit()
if not gui_rows:
    print('No gui trees found!')
    exit()

df_gui = pd.DataFrame(gui_rows)
df_traces = pd.DataFrame(traces_rows)

print('\n')
print('#' * 30, end='\n\n')
print('GUI STATISTICS')
print()
print('Mean number of elements in the GUI screen tree = %.3f' % df_gui['count'].mean())
print('Mean number of clickable elements in the GUI screen tree = %.3f' % df_gui['clickable_elements'].mean())
print()
print('Top-10 elements:')
print()
for k, v in sorted(element_names.items(), key=lambda item: -item[1])[:10]:
    print(f'{k}: {v} times')
print()
print('#' * 30, end='\n\n')
print('TRACES STATISTICS')
print()
print('Mean number of taps per trace = %.3f' % df_traces['taps'].mean())
print('Mean number of swipes per trace = %.3f' % df_traces['swipes'].mean())
print()

