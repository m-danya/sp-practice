#! /usr/bin/python3

import argparse
from pathlib import Path
import pandas as pd
from tqdm import tqdm
import json
from collections import defaultdict


def get_gui_stats(tree_json, element_names):
    '''
    Obtains gui statistics from given json

            Parameters:
                    tree_json (object): gui tree
                    element_names (defaultdict): can be empty. will be
                            updated with encountered elements

            Returns:
                    stats (object): obtained statistics
    '''
    stats = get_subtree_stats(tree_json['activity']['root'], element_names)
    stats['activity_name'] = tree_json['activity_name']
    return stats


def get_traces_stats(gestures_json):
    '''
    Obtains traces statistics from given json

            Parameters:
                    gestures_json (object): gui tree

            Returns:
                    stats (object): obtained statistics
    '''
    taps, swipes = 0, 0
    for screen in gestures_json:
        if len(gestures_json[screen]) > 1:
            swipes += 1
        else:
            taps += 1
    return {
        'taps': taps,
        'swipes': swipes,
        'length': len(gestures_json)
    }


def get_bounds_area(bounds):
    '''Calculates the area of the given rectangle'''
    dx = bounds[2] - bounds[0]
    dy = bounds[3] - bounds[1]
    if (dx * dy < 0):
        # Incorrect, but somehow appears
        return 0
    return dx * dy


def get_subtree_stats(tree, element_names):
    '''
    Calculates given subtree stats and merges it with subtree children's stats.
    (Depth-first search)

            Parameters:
                    tree (object): subtree to observe
                    element_names (defaultdict): can be empty. will be
                            updated with encountered elements

            Returns:
                    collected_data (object): obtained statistics
    '''
    collected_data = {
        'count': 0,
        'clickable_elements': 0,
        'clickable_areas': [],
    }
    if tree is None:
        return collected_data
    collected_data['count'] = 1
    collected_data['clickable_elements'] = int(tree['clickable'])
    if tree['clickable'] and 'bounds' in tree.keys():
        area = get_bounds_area(tree['bounds'])
        if area > 0 and area < 1500 * 500:  # reasonable bounds only
            collected_data['clickable_areas'].append(area)
    element_names[tree['class']] += 1

    for child in tree.get('children', []):  # default = [] instead of None
        child_ans = get_subtree_stats(child, element_names)
        collected_data['count'] += child_ans['count']
        collected_data['clickable_elements'] += child_ans['clickable_elements']
        collected_data['clickable_areas'].extend(child_ans['clickable_areas'])
    return collected_data


def print_statistics(df_gui, df_traces, element_names):
    '''
    Just print given stats.

            Parameters:
                    df_gui (object): gui_trees stats
                    df_traces (object): traces stats
                    element_names (dict): frequency of occurrence of elements
    '''
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
    print('Mean trace length = %.3f' %
          df_traces['length'].mean())
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        help="set input traces directory path (D must directly \
                            contain folders with package names)",
                        required=True,
                        type=Path)
    parser.add_argument("-n",
                        help="set number of first traces to process (default: \
                            process all of them)",
                        required=False,
                        type=int)

    args = parser.parse_args()
    path = args.i

    element_names = defaultdict(int)

    gui_rows, traces_rows = [], []

    application_folders = [x for x in path.iterdir() if x.is_dir()][:args.n]
    # args.n == None is working fine

    for application in tqdm(application_folders):
        for trace in [x for x in application.iterdir() if x.is_dir()]:
            if not (trace / "gestures.json").is_file():
                # gestures doesn't exist => bad directory, skip
                continue
            with open(trace / "gestures.json") as json_file:
                gestures = json.load(json_file)
            traces_rows.append(get_traces_stats(gestures))
            for view in (trace / "view_hierarchies").glob("*.json"):
                if view.name.startswith('.'):
                    # ignore hidden files
                    continue
                with open(view) as json_file:
                    current_json = json.load(json_file)
                if not current_json:
                    # skip empty jsons
                    continue
                gui_rows.append(get_gui_stats(current_json, element_names))

    if not traces_rows:
        print('No traces found!')
        exit()
    if not gui_rows:
        print('No gui trees found!')
        exit()

    df_gui = pd.DataFrame(gui_rows)
    df_traces = pd.DataFrame(traces_rows)

    df_gui.to_csv('research/df_gui.csv')
    df_traces.to_csv('research/df_traces.csv')

    print_statistics(df_gui, df_traces, element_names)


if __name__ == '__main__':
    main()
