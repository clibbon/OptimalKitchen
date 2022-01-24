from collections import defaultdict
from functools import reduce
import random
import numpy as np


def mutate_complex(gene, swap_chance, fixed_positions):
    """Randomly shuffles places of a few things in the gene"""

    locations_to_update = []
    assigned_things = reduce(lambda x, y: x.union(y), gene.values(), set())
    unassigned_things = ALL_THINGS.difference(assigned_things).difference(fixed_positions.values())

    for location, things in gene.items():

        if location in fixed_positions.keys():
            continue

        if np.random.rand() < swap_chance:
            locations_to_update.append(location)
            gene[location] = set()
            unassigned_things.update(things)

    # Need to introduce some randomness
    random.shuffle(locations_to_update)

    for location in locations_to_update:
        available_space = 1.  # Starts off empty

        while available_space >= SMALLEST_THING:
            available_sizes = size_possiblethings_dict.keys()
            largest_size = max(size for size in available_sizes if size <= available_space)

            candidate_things = unassigned_things.intersection(size_possiblethings_dict[largest_size])

            if len(candidate_things) == 0:
                break  # No candidate things left

            selected_thing = random.choice(list(candidate_things))
            gene[location].add(selected_thing)
            unassigned_things.remove(selected_thing)
            available_space -= selected_thing.size

    del gene.fitness.values
    return gene,


def get_child_complex(parent_1, parent_2):
    """Creates a child by selecting positions from either parent. In the case
    no valid positions (from either parent) are free then randomly assign a
    position"""
    unassigned_things = ALL_THINGS.difference(FIXED_POSITIONS.values())
    empty_locations = set()
    child = defaultdict(set)

    non_fixed_locations = ALL_LOCATIONS.difference(FIXED_POSITIONS.keys())

    for location in non_fixed_locations:
        if np.random.rand() > .5:
            # Try parent 1
            parent_1_things = parent_1[location]
            if parent_1_things.issubset(unassigned_things):
                child[location] = parent_1_things
                unassigned_things.difference_update(parent_1_things)
            else:
                empty_locations.add(location)

        else:
            # Parent 2
            parent_2_things = parent_2[location]
            if parent_2_things.issubset(unassigned_things):
                child[location] = parent_2_things
                unassigned_things.difference_update(parent_2_things)
            else:
                empty_locations.add(location)

    unassigned_locations = list(empty_locations)
    random.shuffle(unassigned_locations)

    for location in unassigned_locations:
        available_space = 1.  # Starts off empty

        while available_space >= SMALLEST_THING:
            available_sizes = size_possiblethings_dict.keys()
            largest_size = max(size for size in available_sizes if size <= available_space)

            candidate_things = unassigned_things.intersection(size_possiblethings_dict[largest_size])

            if len(candidate_things) == 0:
                child[location] = set()
                break  # No candidate things left

            selected_thing = random.choice(list(candidate_things))
            child[location].add(selected_thing)
            available_space -= selected_thing.size

    child.update(FIXED_POSITIONS)
    assert child.keys() == parent_1.keys(), f"PARENT 1\n{parent_1}\n\nPARENT 2\n{parent_2}\n\nCHILD\n{child}\n\nDIFFERENCE\n{set(child.keys()).symmetric_difference(set(parent_1.keys()))}"
    return child