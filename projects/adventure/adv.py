from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from queue import Queue
from stack import Stack

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
print(f'length of world.rooms: {len(world.rooms)}')

# solution for test_cross
# traversal_path = ['n','n','s','s','e','e','w','w','w','w','e','e','s','s']

# solution for test_loop
# traversal_path = ['n','n','s','s','e','e','w','w','s','s','w','w','n','n','e','e']

def dft(current_room, graph, visited):
    visited.add(current_room)
    exits = player.current_room.get_exits()
    for exit in exits:
        graph[current_room][exit] = player.current_room.get_room_in_direction(exit).id

    while len(exits) > 1:
        next_dir = None
        for dir in exits:
            if graph[current_room][dir] not in visited:
                next_dir = dir
                break
        
        if next_dir is None:
            break

        player.travel(next_dir)
        traversal_path.append(next_dir)
        current_room = player.current_room.id
        visited.add(current_room)
        exits = player.current_room.get_exits()

        for exit in exits:
            graph[current_room][exit] = player.current_room.get_room_in_direction(exit).id

    return [graph, visited, current_room]

def bfs(graph, current_room, world_visited):
    print('\nbfs\n')
    queue = Queue()
    visited = set()
    path = []
    queue.enqueue({
        'current_room': current_room,
        'path': [current_room]
    })

    while queue.size() > 0:
        current_obj = queue.dequeue()
        current_path = current_obj['path']
        current_room = current_obj['current_room']

        if current_room not in visited:
            if current_room not in world_visited:
                return path[:-1]
            
            visited.add(current_room)
            neighbors = graph[current_room]
            neighbors_values = list(graph[current_room].values())
            neighbors_keys = list(graph[current_room].keys())
            if len(neighbors) == 1:
                path.append(neighbors_keys[0])
                new_room = neighbors_values[0]
            elif len(neighbors_values) > 1:
                for n in neighbors_values:
                    new_neighbors = list(graph[n].values())
                    for i in new_neighbors:
                        if i not in world_visited:
                            index = neighbors_values.index(n)
                            path.append(neighbors_keys[index])
                            new_room = n
                            return path[:-1]
                    
                for n in neighbors_values:
                    if n not in visited and n not in world_visited:
                        index = neighbors_values.index(n)
                        path.append(neighbors_keys[index])
                        new_room = n
                        return path[:-1]

            for n in neighbors:
                new_path = list(current_path)
                new_path.append(n)


            if new_room in world_visited:
                queue.enqueue({
                    'current_room': new_room,
                    'path': new_path
                })
    return 

def traverse_world():   
    graph = {}
    visited = set()

    for i in range(len(world.rooms)):
        graph[i] = {}

    current_room = player.current_room.id
    
    while len(visited) != len(graph):

        status = dft(current_room, graph, visited)

        if len(visited) == len(graph):
            break

        result = bfs(status[0], status[2], status[1])

        for dir in result:
            player.travel(dir)
        traversal_path.extend(result)


traverse_world()
print(f'traversal_path: {traversal_path}')

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
