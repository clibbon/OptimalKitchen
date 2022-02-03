import random

from .operations import Operator
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
        if self.is_empty():
            raise AssertionError("Place is already empty")

        random_idx = random.choice(range(len(self.contents)))
        return self.contents.pop(random_idx)


def get_place_things_dict(places: list[FillablePlace]):
    place_thing_dict = {place.name: set(thing.name for thing in place.contents)
                        for place in places}
    return place_thing_dict


def place_specifically(source, location_dict, things, strict=False):
    """Puts the provided things in the same place in target as they are in source. Ignores things that aren't in
    source"""
    for thing in things:
        if thing.name not in location_dict:
            continue

        for place in source:
            if place.name == location_dict[thing.name]:
                if place.can_fit(thing):
                    place.add(thing)
                elif strict:
                    raise AssertionError(f"Can't fit {thing} in {place}")
                break


def swap_places(child_1, child_2, ind_1_thing_place_dict, ind_2_thing_place_dict, things_to_swap):
    for thing in things_to_swap:
        for place in child_1:
            right_place = place.name == ind_2_thing_place_dict[thing]
            if right_place:
                if place.can_fit(thing):
                    place.add(thing)
                break

        for place in child_2:
            right_place = place.name == ind_1_thing_place_dict[thing]
            if right_place:
                if place.can_fit(thing):
                    place.add(thing)
                break


class VolumeOperator(Operator):
    """An operator designed to work with things and places which have full dimensions (width, height, depth)"""

    def __init__(self, all_things: dict[str, Thing], all_places: dict[str, Place], fixed_assignments: dict, swap_chance):
        self.all_things = all_things
        self.all_places = all_places
        self.fixed_assignments = fixed_assignments

        self.assignable_things = list(thing for thing in all_things.values()
                                      if thing.name not in fixed_assignments.keys())
        self.assignable_places = list(place for place in all_places.values()
                                      if place.name not in fixed_assignments.values())

        self.swap_chance = swap_chance

    def create_gene(self):
        places = [FillablePlace(place) for place in self.assignable_places]

        pack_random(self. assignable_things, places)
        return places

    def mutate(self, individual) -> None:
        unassigned_things = []
        for place in individual:
            should_swap = random.random() < self.swap_chance
            if should_swap and not place.is_empty():
                unassigned_things.append(place.pop())

        pack_random(unassigned_things, individual)

    def mate(self, ind_1, ind_2):
        things_to_swap = [thing for thing in self.assignable_things if random.random() < self.swap_chance]

        ind_1_thing_place_dict = self.get_thing_place_dict(ind_1, include_fixed=False)
        ind_2_thing_place_dict = self.get_thing_place_dict(ind_2, include_fixed=False)

        things_to_keep = [thing for thing in self.assignable_things if thing not in things_to_swap]

        child_1 = [FillablePlace(place) for place in self.assignable_places]
        child_2 = [FillablePlace(place) for place in self.assignable_places]

        place_specifically(child_1, ind_1_thing_place_dict, things_to_keep, strict=True)
        place_specifically(child_2, ind_2_thing_place_dict, things_to_keep, strict=True)

        # Now try to swap the things to swap
        place_specifically(child_1, ind_2_thing_place_dict, things_to_swap, strict=False)
        place_specifically(child_2, ind_1_thing_place_dict, things_to_swap, strict=False)

        return child_1, child_2

    def get_thing_place_dict(self, places: list[FillablePlace], include_fixed):
        thing_place_dict = {}
        for place in places:
            for thing in place.contents:
                thing_place_dict[thing.name] = place.name

        if include_fixed:
            thing_place_dict.update(self.fixed_assignments)

        return thing_place_dict


def pack_random(things, places):
    """Randomly put things in places. Modifies places"""
    for thing in things:
        random.shuffle(places)
        for place in places:
            if place.can_fit(thing):
                place.add(thing)
                break
