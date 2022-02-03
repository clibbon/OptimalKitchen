from pytest import fixture

from kitchenoptimiser import io
from kitchenoptimiser.io import Place, Thing
from kitchenoptimiser.volumeoperators import VolumeOperator

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

@fixture
def operator():
    operator = VolumeOperator(ALL_THINGS, ALL_PLACES, FIXED_POSITIONS, .1)

    return operator


@fixture
def places():
    places = [Place("top_shelf", 50, 100, 20, 0, False, .1),
              Place("mid_shelf", 50, 100, 20, 0, False, .1),
              Place("bot_shelf", 50, 100, 20, 0, False, .3)]

    return places


@fixture
def things():
    things = [Thing("vase", False, False, 50, 20, 30, True, .1),
              ]
    return things


def test_create(places, things):
    fixed = {'vase': "top_shelf"}
    volume_operator = VolumeOperator(all_things=things,
                                     all_places=places,
                                     fixed_assignments=fixed,
                                     swap_chance=.5)
    gene = volume_operator.create_gene()

    assert len(gene) == 3


def test_mutate(operator):
    test_individual = operator.create_gene()
    init_dict = operator.get_thing_place_dict(test_individual, include_fixed=False)
    operator.mutate(test_individual)
    mutated_dict = operator.get_thing_place_dict(test_individual, include_fixed=False)
    assert init_dict != mutated_dict


def test_mate(operator):
    test_individual_1 = operator.create_gene()
    test_individual_2 = operator.create_gene()

    child_1, child_2 = operator.mate(test_individual_1, test_individual_2)

    child_1_dict = operator.get_thing_place_dict(child_1, include_fixed=False)
    child_2_dict = operator.get_thing_place_dict(child_2, include_fixed=False)
    ind_1_dict = operator.get_thing_place_dict(test_individual_1, include_fixed=False)
    ind_2_dict = operator.get_thing_place_dict(test_individual_2, include_fixed=False)

    assert child_2_dict != child_1_dict, "Both children are the same!"
    assert child_1_dict != ind_1_dict, "Child 1 is the same as parent 1"
    assert child_1_dict != ind_2_dict, "Child 1 is the same as parent 2"
    assert child_2_dict != ind_1_dict, "Child 2 is the same as parent 1"
    assert child_2_dict != ind_2_dict, "Child 2 is the same as parent 2"
