import matplotlib.pyplot as plt
import networkx as nx

def hierarchical_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _hierarchical_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchical_pos(G, node, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {node: (xcenter, vert_loc)}
    else:
        pos[node] = (xcenter, vert_loc)
    
    parsed.append(node)
    neighbors = list(G.neighbors(node))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        neighbors.remove(parent)  
    
    if len(neighbors) != 0:
        dx = width / 2 
        nextx = xcenter - width / 2 - dx / 2
        for neighbor in neighbors:
            nextx += dx
            pos = _hierarchical_pos(G, neighbor, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=node, parsed=parsed)
    
    return pos

def plot_tree(node):
    G = nx.Graph()
    labels = {}

    def add_edges(node, G):
        if node:
            node_id = id(node)
            labels[node_id] = node.value  # Store the label for the current node
            if node.left:
                left_id = id(node.left)
                G.add_edge(node_id, left_id)
                add_edges(node.left, G)
            if node.right:
                right_id = id(node.right)
                G.add_edge(node_id, right_id)
                add_edges(node.right, G)

    add_edges(node, G)
    
    pos = hierarchical_pos(G, id(node))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=3000, node_color="#ccc", font_size=14)
    plt.show()

def add_nodes_positions(G,node, x, y, node_count, left_count, right_count, pos, labels):
        if node is not None:
            G.add_node(node_count)
            pos[node_count] = (x, y)
            labels[node_count] = node.value
            
            # Add left child
            left_count = node_count + 1
            if node.left is not None:
                G.add_edge(node_count, left_count)
                left_count = add_nodes_positions(G,node.left, x - 1, y - 1,node_count, left_count,right_count,pos,labels)
            
            # Add right child
            right_count = left_count + 1
            if node.right is not None:
                G.add_edge(node_count, left_count)
                right_count = add_nodes_positions(G,node.right, x + 1, y - 1, node_count,left_count, right_count,pos,labels)
            
            return right_count
        return node_count

def show_tree(root_node):
    G = nx.Graph()
    
    pos = {}
    labels = {}
    layer = 0
    def add_nodes_positions(node, x, y, node_count):
        if node is not None:
            print(layer)
            # Add the node to the graph
            G.add_node(str(node_count))
            layer_inside = layer+0.25
            # Set the position and label for the node
            pos[str(node_count)] = (x, y)
            labels[str(node_count)] = node.value

            # Traverse the left subtree
            if node.left is not None:
                left_count = node_count + 1
                G.add_edge(str(node_count), str(left_count))
                new_x = (x-2)
                left_count = add_nodes_positions(node.left, x - 1, y - 1, left_count)
            
            # Traverse the right subtree
            if node.right is not None:
                right_count = left_count + 1
                G.add_edge(str(node_count), str(right_count))
                return add_nodes_positions(node.right, x + 1, y - 1, right_count)
            
            return node_count + 1
        return node_count
    # Draw the graph with specified positions
    add_nodes_positions(root_node, 0, 0, 1)
    
    # Draw the graph with specified positions
    nx.draw(G, pos, labels=labels, with_labels=True)
    plt.show()