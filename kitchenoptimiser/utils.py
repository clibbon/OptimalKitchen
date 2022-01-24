"""Useful functions I'm sure I'll need again"""

import matplotlib.pyplot as plt
import networkx as nx


def draw_layout(layout: nx.Graph):
    fig, ax = plt.subplots(figsize=(12, 9))
    pos = nx.spring_layout(layout)
    nx.draw(layout, pos)
    nx.draw_networkx_labels(layout, pos, labels={n: n for n in layout})
    plt.show()


def draw_process(process: nx.Graph):
    fig, ax = plt.subplots(figsize=(12, 9))
    pos = nx.spring_layout(process)
    nx.draw(process, pos)
    nx.draw_networkx_labels(process, pos, labels={n: n for n in process})
    nx.draw_networkx_edge_labels(
        process,
        pos,
        edge_labels={edge[:2]: edge[2]['weight'] for edge in process.edges(data=True)})
    plt.show()


def parse(tree):
    """This is useful for when I forget the correct graph format."""
    new_tree = {}
    for k, v in tree.items():
        if type(v) in (float, int):
            new_tree[k] = {'weight': v}
        else:
            new_tree[k] = parse(v)
    return new_tree
