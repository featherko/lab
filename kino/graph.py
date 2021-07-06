"""Work with Graphs."""
from itertools import combinations
from typing import List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
from pony.orm import db_session, select

from kino.db import Actors, Title, db_bind


@db_session
def build_edges() -> List[Tuple]:
    """Create list of tuples.

    Creating list of tuples, where [0], [1] element of each tuple are Two actor names(nodes) and
    [2] is amount of times they were playing together.
    """
    d = {}
    for t in select(t for t in Title):
        names = list(t.cast.name)
        names.sort()
        comb = combinations(names, 2)
        for pair in comb:
            if pair in d:
                d[pair] += 1
            else:
                d[pair] = 1

    return [(*k, v) for k, v in d.items()]


def degrees() -> list:
    """Get degree list.

    Prints out list of tuples with Node-name and its degree.
    """
    with db_session:
        q = select(a.name for a in Actors)[:]
    degree_list = G.degree(list(q))
    print(degree_list)
    return degree_list


def close_centr() -> None:
    """Calculate closeness centrality.

    Prints out dict with Node-name as key and its closeness centrality as value.
    """
    close = nx.algorithms.centrality.closeness_centrality(G)
    print(close)


def between_centr() -> None:
    """Calculate betweenness centrality.

    Prints out dict with Node-name as key and its betweenness centrality as value.
    """
    between = nx.algorithms.centrality.betweenness_centrality(G)
    print(between)


def hubs(lst: list) -> None:
    """Find out hubs.

    Prints out list of tuples, where T[0] node name T[1] node degree.
    """
    avg_edges = sum(n[1] for n in lst) / len(lst)
    hubs_fil = filter(lambda x: x[1] > avg_edges, lst)
    print(list(hubs_fil))


def build_graph() -> None:
    """Build graph."""
    plt.rcParams["figure.figsize"] = (40, 40)
    pos = nx.spring_layout(G, seed=7, k=5)
    weights = [item[-1] for item in edges]
    plt.figure(1)
    nx.draw_networkx_nodes(G, pos, node_size=30)
    nx.draw_networkx_edges(G, pos, width=weights)
    nx.draw_networkx_labels(G, pos, font_size=7, font_family="sans-serif")
    ax = plt.gca()
    ax.margins(1)
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    db_bind()
    edges = build_edges()
    edges.sort(key=lambda x: x[2], reverse=True)
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    dgr_lst = degrees()
    close_centr()
    between_centr()
    hubs(dgr_lst)
    # build_graph()
