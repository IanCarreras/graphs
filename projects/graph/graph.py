"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # create empty queue and enqueue the starting vertex
        q = Queue()
        q.enqueue(starting_vertex)
        # create empty set to track visited vertices
        visited = set()

        # while queue is not empty
        while q.size() > 0:
            # get current vertex, dequeue from queue
            v = q.queue[0]
            q.dequeue()
            
            # check if the current vertex has not been visited
            if v not in visited:
                # print current vertex
                print(f'bft: {v}')
                # mark current vertex as visited
                visited.add(v)            
                # queue up all the current vertex's neighbors, to visit them next
                neighbors = self.get_neighbors(v)
                for n in neighbors:
                    q.enqueue(n)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # create empty stack and add the starting vertex
        stack = Stack()
        stack.push(starting_vertex)
        # create empty set to track visited vertices
        visited = set()

        # while stack is not empty
        while stack.size() > 0:
            # get current vertex, pop from stack
            v = stack.stack[-1]
            stack.pop()
            # check if the current vertex has not been visited
            if v not in visited:
                # print current vertex
                print(f'dft: {v}')
                # mark current vertex as visited
                visited.add(v)          
                # push all the current vertex's neighbors, to visit them next
                neighbors = self.get_neighbors(v)
                for n in neighbors:
                    stack.push(n)

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        pass  # TODO

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # create an empty queue and enqueue the path to starting vertex
        q = Queue()
        # create an empty set to track visited verticies
        visited = set()
        q.enqueue({
            'current_vertex': starting_vertex,
            'path': [starting_vertex]
        })

        # while the queue is not empty
        while q.size() > 0:
            # get current vertex path, dequeue from queue
            current_obj = q.dequeue()
            # set current vertex to the last element of the path
            current_path = current_obj['path']
            current_vertex = current_obj['current_vertex']

            # check if the current vertex has not been visited
            if current_vertex not in visited:

                # check if current vertex is destination
                if current_vertex is destination_vertex:
                    # if yes stop and return
                    return current_path

                # mark current vertex as visited
                visited.add(current_vertex)

                # queue up new paths with each neighbor
                neighbors = self.get_neighbors(current_vertex)
                for n in neighbors:
                    # take current path
                    # append neighbor
                    # queue up new path
                    new_path = list(current_path)
                    new_path.append(n)
                
                q.enqueue({
                    'current_vertex': n,
                    'path': new_path
                }) 
        return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        stack = Stack()
        visited = set()
        stack.push({
            'current_vertex': starting_vertex,
            'path': [starting_vertex]
        })

        while stack.size() > 0:
            current_obj = stack.pop()
            current_path = current_obj['path']
            current_vertex = current_obj['current_vertex']

            if current_vertex not in visited:
                if current_vertex == destination_vertex:
                    return current_path

                visited.add(current_vertex)

                for n in self.get_neighbors(current_vertex):
                    new_path = list(current_path)
                    new_path.append(n)
                    stack.push({
                        'current_vertex': n,
                        'path': new_path
                    })
        return None

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        pass  # TODO

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
