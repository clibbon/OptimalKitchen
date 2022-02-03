import pytest

from kitchenoptimiser.volumeoperators import VolumeOperator
from kitchenoptimiser.scorers import DistanceScorer, VisibilityScorer
from kitchenoptimiser import io

ALL_THINGS = io.read_things(r'../example/things.json')
ALL_PLACES = io.read_locations(r'../example/locations.json')
LAYOUT = io.read_layout(r'../example/layout.json')
PROCESS_DETAILS = io.read_process_details(r'../example/process_details2.json')
FIXED_POSITIONS = {
    '0_Fridge': '0_Fridge',
    '4_Hob': '4_Hob',
    '4_Oven': '4_Oven',
    '7_Sink': '7_Sink',
}


@pytest.fixture
def operator():
    operator = VolumeOperator(ALL_THINGS, ALL_PLACES, FIXED_POSITIONS, .1)

    return operator


def test_distance_scorer(operator):
    individual = operator.create_gene()
    scorer = DistanceScorer(LAYOUT, PROCESS_DETAILS)
    thing_place_dict = operator.get_thing_place_dict(individual, include_fixed=True)

    score = scorer.get_score(thing_place_dict)


def test_visibility_scorer(operator):
    individual = operator.create_gene()
    scorer = VisibilityScorer(ALL_PLACES, ALL_THINGS)
    thing_place_dict = operator.get_thing_place_dict(individual, include_fixed=True)

    score = scorer.get_score(thing_place_dict)
    print(score)
