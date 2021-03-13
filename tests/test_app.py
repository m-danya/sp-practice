import pytest
from pathlib import Path
import json
from collections import defaultdict


from get_statistics import get_gui_stats, get_traces_stats


def test_get_gui_stats(gui_jsons):
    element_names = defaultdict(int)
    stats = get_gui_stats(gui_jsons['data'], element_names)
    stats_expected = gui_jsons['expected']
    element_names_expected = stats_expected.pop('element_names')
    assert stats == stats_expected
    assert element_names == element_names_expected


def test_get_traces_stats(trace_json):
    stats = get_traces_stats(trace_json['data'])
    assert stats == trace_json['expected']


def get_jsons_list(type):
    files = (Path(__file__).parent / "jsons" / f"{type}").glob("*.json")
    return [x for x in files if 'expected' not in x.name]


@pytest.fixture(params=get_jsons_list('gui_trees'),
                ids=[str(s.name) for s in get_jsons_list('gui_trees')])
def gui_jsons(request):
    return get_data_and_expected(request.param)


@pytest.fixture(params=get_jsons_list('traces'),
                ids=[str(s.name) for s in get_jsons_list('traces')])
def trace_json(request):
    return get_data_and_expected(request.param)


def get_data_and_expected(path_to_json):
    with open(path_to_json) as json_file:
        json_data = json.load(json_file)
    # get _expected file path:
    path_to_json = path_to_json.parent / \
        (path_to_json.name.replace('.json', '_expected.json'))
    with open(path_to_json) as json_file:
        json_expected = json.load(json_file)
    return {
        "data": json_data,
        "expected": json_expected
    }
