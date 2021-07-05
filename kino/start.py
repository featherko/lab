import matplotlib.pyplot as plt
import networkx as nx
plt.rcParams["figure.figsize"] = (13,13)

actors = [
    ("Эван Рэйчел Вуд"),
    ("Энтони Хопкинс"),

]
actors_per_films = [("Эван Рэйчел Вуд", "Энтони Хопкинс", 1),
                    ("Эван Рэйчел Вуд", "Брэдд Питт", 2),
                    ("Леонардо ди Каприо", "Брэдд Питт", 5),
                    ("Брэдд Питт", "Анджелина Джоли", 7),
                    ]
G = nx.Graph()
G.add_nodes_from(actors)

G.add_weighted_edges_from(actors_per_films)

pos = nx.spring_layout(G, seed=7)
weights = [item[-1] for item in actors_per_films]

plt.figure(1)
nx.draw_networkx_nodes(G, pos, node_size=1200)
nx.draw_networkx_edges(G, pos, width=weights)

nx.draw_networkx_labels(G, pos, font_size=15, font_family="sans-serif")

ax = plt.gca()
ax.margins(0.4)
plt.axis("off")
plt.show()



"""
https://api.kinopoisk.dev/movie?field=typeNumber&search=4&sortField=rating.imdb&sortType=-1&limit=100&token=ZQQ8GMN-TN54SGK-NB3MKEC-ZKB8V06"""