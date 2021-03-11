import pytest
from pathlib import Path
import json
from collections import defaultdict


from get_statistics import get_gui_stats, get_traces_stats


def test_get_gui_stats(gui_jsons):
    element_names = defaultdict(int)
    stats = get_gui_stats(gui_jsons['data'], element_names)
    stats_ans = gui_jsons['ans']
    element_names_ans = stats_ans.pop('element_names')
    assert stats == stats_ans
    assert element_names == element_names_ans


def test_get_traces_stats(trace_json):
    stats = get_traces_stats(trace_json['data'])
    assert stats == trace_json['ans']


def get_jsons_list(type):
    files = (Path.cwd() / "tests" / "jsons").glob(f"{type}_*.json")
    return [x for x in files if 'ans' not in x.name]


@pytest.fixture(params=get_jsons_list('gui'),
                ids=[str(s.name) for s in get_jsons_list('gui')])
def gui_jsons(request):
    return get_data_and_ans(request.param)


@pytest.fixture(params=get_jsons_list('trace'),
                ids=[str(s.name) for s in get_jsons_list('trace')])
def trace_json(request):
    return get_data_and_ans(request.param)


def get_data_and_ans(path_to_json):
    with open(path_to_json) as json_file:
        json_data = json.load(json_file)
    # get _ans file path:
    path_to_json = path_to_json.parent / \
        (path_to_json.name.replace('.json', '_ans.json'))
    with open(path_to_json) as json_file:
        json_ans = json.load(json_file)
    return {
        "data": json_data,
        "ans": json_ans
    }
