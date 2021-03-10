#! /usr/bin/python3

import argparse
from pathlib import Path
import pandas as pd
from tqdm import tqdm
import json
import glob

def gui_tree_dfs(tree, element_names):
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
        child_ans = gui_tree_dfs(child, element_names)
        ans['count'] += child_ans['count']
        ans['clickable_elements'] += child_ans['clickable_elements']
    return ans


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        help="set input traces directory path (D must directly contain folders with package names)",
                        required=True,
                        type=Path)
    parser.add_argument("-n",
                        help="set number of first traces to process (default: process all of them)",
                        required=False,
                        type=int)

    args = parser.parse_args()
    path = args.i

    element_names = {}

    gui_rows = []
    traces_rows = []

    for application in tqdm([x for x in path.iterdir() if x.is_dir()][:args.n]):
        # args.n == None is working fine
        for trace in [x for x in application.iterdir() if x.is_dir()]:
            with open(trace / "gestures.json") as json_file:
                gestures = json.load(json_file)
            taps, swipes = 0, 0
            for screen in gestures:
                if len(gestures[screen]) > 1:
                    swipes += 1
                else:
                    taps += 1
            traces_rows.append({'taps': taps, 'swipes': swipes})
            for view in (trace / "view_hierarchies").glob("*.json"):
                if view.name.startswith('.'):
                    # ignore hidden files
                    continue
                with open(view) as json_file:
                    current_json = json.load(json_file)
                if not current_json:
                    continue
                stats = gui_tree_dfs(
                    current_json['activity']['root'], element_names)
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
    print('Mean number of elements in the GUI screen tree = %.3f' %
          df_gui['count'].mean())
    print('Mean number of clickable elements in the GUI screen tree = %.3f' %
          df_gui['clickable_elements'].mean())
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
    print('Mean number of swipes per trace = %.3f' %
          df_traces['swipes'].mean())
    print()


if __name__ == '__main__':
    main()
