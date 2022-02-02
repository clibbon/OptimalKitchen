import random

from operations import Operator
from .io import Thing, Place


class FillablePlace:
    """A 2D place with height. Why not a 3D place? We're packing in 2D, but with a height constraint. Packs greedily,
    not optimally."""
    def __init__(self, place: Place, initial_contents: list[Thing] = None):
        if initial_contents is None:
            initial_contents = []

        self.contents = []

        self.name = place.name
        self.width = place.width
        self.depth = place.depth
        self.height = place.height

        for thing in initial_contents:
            self.add(thing)

    def is_empty(self):
        return len(self.contents) == 0

    def can_fit(self, thing: Thing) -> bool:
        if thing.height > self.height:
            return False

        if thing.is_solid:
            return self.can_fit_solid(thing)
        else:
            return self.can_fit_liquid(thing)

    def can_fit_solid(self, thing: Thing) -> bool:
        dimension1 = max(thing.width, thing.depth)
        dimension2 = min(thing.width, thing.depth)

        available_width, available_depth = self.get_available_square()
        available_dim1 = max(available_depth, available_width)
        available_dim2 = min(available_width, available_depth)
        return (dimension1 <= available_dim1) and (dimension2 <= available_dim2)

    def can_fit_liquid(self, thing: Thing) -> bool:
        available_width, available_depth = self.get_available_square()
        available_area = available_depth * available_width

        thing_area = thing.width * thing.depth
        return thing_area <= available_area

    def get_available_square(self):
        available_depth = self.depth
        available_width = self.width
        for inner_thing in self.contents:
            max_dimension = max(inner_thing.width, inner_thing.depth)
            min_dimension = min(inner_thing.width, inner_thing.depth)

            if available_width > available_depth:
                available_width -= max_dimension
                available_depth -= min_dimension
            else:
                available_depth -= max_dimension
                available_width -= min_dimension

        return available_width, available_depth

    def add(self, thing: Thing) -> None:
        if not self.can_fit(thing):
            raise AssertionError("Initial contents too large for bin")
        self.contents.append(thing)

    def remove(self, thing: Thing) -> None:
        self.contents.remove(thing)

    def pop(self) -> Thing:
        """Pop a random thing out"""
        if not self.is_empty():
            raise AssertionError("Place is already empty")

        random_idx = random.choice(range(len(self.contents)))
        return self.contents.pop(random_idx)


def get_thing_place_dict(places: list[FillablePlace]):
    thing_place_dict = {}
    for place in places:
        for thing in place.contents:
            thing_place_dict[thing.name] = place.name
    return thing_place_dict



class VolumeOperator(Operator):
    """An operator designed to work with things and places which have full dimensions (width, height, depth)"""

    def __init__(self, all_things: list[Thing], all_places: list[Place], fixed_assignments: dict, swap_chance):
        self.all_things = all_things
        self.all_places = all_places
        self.fixed_assignments = fixed_assignments

        self.assignable_things = list(thing for thing in all_things if thing.name not in fixed_assignments.keys())
        self.assignable_places = list(place for place in all_places if place not in fixed_assignments.values())

        self.swap_chance = swap_chance

    def create_gene(self):
        places = [FillablePlace(place) for place in self.assignable_places]

        pack_random(self. assignable_things, places)
        return places

    def mutate(self, individual) -> None:
        unassigned_things = []
        for place in individual.places:
            if random.random() < self.swap_chance:
                unassigned_things.append(place.pop())

        del individual.fitness  # Part of DEAP
        pack_random(unassigned_things, individual.places)

    def mate(self, ind_1, ind_2):
        things_to_swap = [thing for thing in self.assignable_things if random.random() < self.swap_chance]

        ind_1_thing_place_dict = get_thing_place_dict(ind_1.places)
        ind_2_thing_place_dict = get_thing_place_dict(ind_2.places)
        places_1 = sorted(ind_1.places, key=lambda x: x.name)
        places_2 = sorted(ind_2.places, key=lambda x: x.name)
        for place_1, place_2 in zip(places_1, pl)

def pack_random(things, places):
    """Randomly puut things in places. Modifies places"""
    for thing in things:
        random.shuffle(places)
        for place in places:
            if place.can_fit(thing):
                place.add(thing)
                break
