from pytest import fixture
from kitchenoptimiser.io import Place, Thing
from kitchenoptimiser.VolumeOperators import VolumeOperator


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
                                     swap_chance=.1)
    gene = volume_operator.create_gene()

    assert len(gene) == 3
