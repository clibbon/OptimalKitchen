import random
from abc import ABC, abstractmethod

import numpy as np


class Operator(ABC):
    """Parent class defining operations"""

    @abstractmethod
    def create_gene(self):
        """Creates a gene in the form of a dictionary of thing:location"""
        pass

    @abstractmethod
    def mutate(self, individual) -> None:
        """In place mutation of an individual"""
        pass

    @abstractmethod
    def mate(self, ind_1, ind_2) -> tuple[dict, dict]:
        pass


class SetOperator(Operator):

    def __init__(self, all_things, all_locations, fixed_assignments, swap_chance):
        self.all_things = all_things
        self.all_locations = all_locations
        self.fixed_assignments = fixed_assignments

        # Precalculate a few things
        self.size_possiblethings_dict = {}  # TODO Fill out
        self.smallest_thing = get_smallest_thing(all_things)

        self.assignable_things = set(all_things.keys()).difference(set(fixed_assignments.keys()))
        self.assignable_locations = set(all_locations.keys()).difference(set(fixed_assignments.values()))

        self.swap_chance = swap_chance

    def create_gene(self):
        empty_locations = list(self.assignable_locations)
        random.shuffle(empty_locations)

        gene = dict(self.fixed_assignments)
        self.assign_things(gene, empty_locations, set(self.assignable_things))

        return gene

    def mutate(self, individual) -> tuple:
        locations_to_update = []
        unassigned_things = self.assignable_things.difference(set(individual.keys()))

        for location, things in individual.items():

            if location not in self.assignable_locations:
                continue

            if np.random.rand() < self.swap_chance:
                locations_to_update.append(location)
                individual[location] = set()
                unassigned_things.update(things)

        random.shuffle(locations_to_update)  # Need to introduce some randomness

        self.assign_things(individual, locations_to_update, unassigned_things)

        del individual.fitness.values  # part of the process to update individuals inplace
        return individual,

    def mate(self, ind_1, ind_2) -> tuple[dict, dict]:
        pass

    def assign_things(self, gene: dict, locations, things) -> None:
        for location in locations:
            available_space = 1.  # Starts off empty

            while available_space >= self.smallest_thing:
                available_sizes = self.size_possiblethings_dict.keys()
                largest_size = max(size for size in available_sizes if size <= available_space)

                candidate_things = things.intersection(self.size_possiblethings_dict[largest_size])

                if len(candidate_things) == 0:
                    if location not in gene:
                        gene[location] = set()
                    break  # No candidate things left

                selected_thing = random.choice(list(candidate_things))
                gene[location].add(selected_thing)
                available_space -= selected_thing.size
                things.remove(selected_thing)


def get_smallest_thing(things) -> float:
    pass
