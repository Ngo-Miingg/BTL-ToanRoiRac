import networkx as nx
import matplotlib.pyplot as plt

# Tạo đồ thị
G = nx.Graph()

# Thêm các cạnh vào đồ thị theo ví dụ đã cho
edges = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]
G.add_edges_from(edges)

# Hàm để thực hiện DFS
def dfs_edges(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next_node in set(graph[start]) - visited:
        yield (start, next_node)
        yield from dfs_edges(graph, next_node, visited)

# Tạo cây DFS từ đỉnh 1
dfs_tree_edges = list(dfs_edges(G, 1))

# Vẽ đồ thị gốc và cây DFS
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# Vẽ đồ thị gốc
nx.draw(G, with_labels=True, node_size=500, font_size=12, font_weight='bold', ax=ax1, node_color='skyblue')
ax1.set_title("Đồ Thị Gốc")

# Vẽ cây DFS
T = nx.Graph(dfs_tree_edges)
nx.draw(T, with_labels=True, node_size=500, font_size=12, font_weight='bold', ax=ax2, node_color='lightgreen')
ax2.set_title("Cây DFS")

# Hiển thị đồ thị
plt.tight_layout()
plt.show()