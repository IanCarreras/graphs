from queue import Queue
from stack import Stack

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]

    def dft(self, starting_vertex):
        stack = Stack()
        stack.push(starting_vertex)
        visited = set()

        while stack.size() > 0:
            v = stack.stack[-1]
            stack.pop()
            if v not in visited:
                visited.add(v)
                neighbors = self.get_neighbors(v)
                for n in neighbors:
                    stack.push(n)
        
        return visited

    def bfs(self, starting_vertex, destination_vertex):
        q = Queue()
        visited = set()
        q.enqueue({
            'current_vertex': starting_vertex,
            'path': [starting_vertex]
        })

        while q.size() > 0:
            current_obj = q.dequeue()
            current_path = current_obj['path']
            current_vertex = current_obj['current_vertex']

            if current_vertex not in visited:
                if current_vertex is destination_vertex:
                    return current_path

                visited.add(current_vertex)
                neighbors = self.get_neighbors(current_vertex)
                for n in neighbors:
                    new_path = list(current_path)
                    new_path.append(n)

                q.enqueue({
                    'current_vertex': n,
                    'path': new_path
                })
        return None