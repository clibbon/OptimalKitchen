import networkx as nx
from collections import defaultdict
from .processes import Process

class DistanceScorer:

    def __init__(self, layout: nx.Graph):
        self.distances = pre_calc_distances(layout)

    def score_process(self, process: Process):


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