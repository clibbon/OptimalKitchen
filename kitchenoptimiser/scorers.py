from collections import defaultdict

import networkx as nx

from .io import Place, Thing


class DistanceScorer:

    def __init__(self, layout: nx.Graph, process_importances: dict, unassigned_distance_penalty=100):
        self.distances = pre_calc_distances(layout)
        self.process_importances = process_importances
        self.unassigned_penalty = unassigned_distance_penalty

    def _score_process(self, process: nx.Graph, thing_location_dict: dict[str:str]):
        """
        Score how easy a process is given a thing-location mapping
        :param process: a dictionary describing a process
        :param thing_location_dict: Map of thing names to place names
        :return: Score - high is difficult
        """

        avg_distance = 0
        dict_process = nx.to_dict_of_dicts(process)
        for thing, destination_things in dict_process.items():
            for destination_thing, edge_info in destination_things.items():

                if (thing in thing_location_dict) and (destination_thing in thing_location_dict):
                    source_location = thing_location_dict[thing]
                    destination_location = thing_location_dict[destination_thing]

                    avg_distance += edge_info['weight'] * self.distances[source_location][destination_location]
                else:
                    avg_distance += self.unassigned_penalty

        return avg_distance

    def get_score(self, thing_location_dict: dict):
        """To calculate fitness create a graph for each process with weights given as
        the frequency of use * distance between the nodes. Then find the total path
        length for that graph.
        """
        fitness = 0

        for process_name, details in self.process_importances.items():
            avg_distance = self._score_process(details['process'], thing_location_dict)
            fitness += avg_distance * details['frequency']
        return fitness


def pre_calc_distances(layout: nx.Graph, weight: str = 'weight'):
    """
    Calculates all pairwise distances
    :param layout:
    :param weight:
    :return:
    """
    shortest_paths = nx.algorithms.shortest_path(layout)
    shortest_lengths = defaultdict(dict)

    for start_node, finish_nodes in shortest_paths.items():
        for finish_node in finish_nodes:
            shortest_lengths[start_node][finish_node] = nx.classes.path_weight(layout,
                                                                               shortest_paths[start_node][finish_node],
                                                                               weight)
    return shortest_lengths


class VisibilityScorer:
    def __init__(self, location_info: dict[str: Place], thing_info: dict[str: Thing], not_surface_penalty=10,
                 no_sockets_penalty=5):
        self.location_info = location_info
        self.thing_info = thing_info
        self.not_surface_penalty = not_surface_penalty
        self.no_sockets_penalty = no_sockets_penalty

    def get_score(self, thing_location_dict):
        """Calculate the fitness based on the convenience of the location - does it
        have appropriate sockets/visibility etc."""

        fitness = 0

        for thing, location in thing_location_dict.items():
            if location not in self.location_info.keys():
                raise AssertionError(f"Location {location} has no info.")

            location_info = self.location_info[location]
            thing_info = self.thing_info[thing]
            surface_needs_met = (thing_info.needs_surface and location_info.is_surface) or (
                not thing_info.needs_surface)
            socket_needs_met = (thing_info.needs_socket and (location_info.sockets > 0))

            if not surface_needs_met:
                fitness -= self.not_surface_penalty
            if not socket_needs_met:
                fitness -= self.no_sockets_penalty

            if thing_info.visibility_need is not None:
                visibility_score = thing_info.visibility_need * location_info.visibility
                fitness += visibility_score

            return fitness
