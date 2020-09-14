# create directed graph of ancestors
    # iterate over the ancestor list
        # create child keys with a set of parent values
        # if child is already in the graph add parent to the set

# search through the graph and return the earliest 
# ancestor of the starting node
    # get parent of starting node
    # if starting node has no parents return -1
    
    # if starting node has parents
        # check if parents have parents
        # if yes recursively get the parents

def get_ancestor(graph, node):
    parents = graph[node]
    print('\n')
    print(f'node: {node}')
    print(f'parents: {parents}')
    print('length ', len(parents))

    if len(parents) == 1:
        ancestor = parents.pop()
        print(f'ancestor: {ancestor}')
        return ancestor
    elif len(parents) > 1:
        left_p = list(parents)[0]
        right_p = list(parents)[1]
        if left_p in graph:
            print('call left')
            get_ancestor(graph, left_p)
        if right_p in graph:
            print('call right')
            get_ancestor(graph, right_p)

def earliest_ancestor(ancestors, starting_node):
    print(f'start: {starting_node}')
    graph = {}
    for v in ancestors:
        if v[1] not in graph:
            graph[v[1]] = set()
            graph[v[1]].add(v[0])
        else:
            graph[v[1]].add(v[0])

    if starting_node not in graph.keys():
        return -1
    else:
        ancestor = get_ancestor(graph, starting_node)
        print(ancestor)
        print(graph)
        return ancestor
