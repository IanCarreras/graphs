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
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
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
    print('\ndft\n')
    visited.add(current_room)
    exits = player.current_room.get_exits()
    print(f'current_room: {current_room}')
    print(f'exits: {exits}')
    for exit in exits:
        graph[current_room][exit] = player.current_room.get_room_in_direction(exit).id

    while len(exits) > 1:
        print(f'\ncurrent_room: {current_room}')
        next_dir = None
        for dir in exits:
            print('\n')
            print(f'dir: {dir}')
            print(f'graph: {graph}')
            if graph[current_room][dir] not in visited:
                next_dir = dir
                break
                
        player.travel(next_dir)
        print(f'player moves: {dir}')
        traversal_path.append(next_dir)
        current_room = player.current_room.id
        print(f'line 74 current_room: {current_room}')
        visited.add(current_room)
        print(f'line 76 visited: {visited}')
        exits = player.current_room.get_exits()
        print(f'line 78 exits: {exits}')

        for exit in exits:
            graph[current_room][exit] = player.current_room.get_room_in_direction(exit).id
        print(f'line 82 graph: {graph}')
        print(f'traversal_path: {traversal_path}')

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
        print('\n')
        print(f'queue: {queue.queue}')
        current_obj = queue.dequeue()
        current_path = current_obj['path']
        current_room = current_obj['current_room']
        print(f'current_room: {current_room}')

        if current_room not in visited:
            print(f'{current_room} not visited by bfs')
            print(f'line 102 visited: {visited}')
            print(f'world_visited: {world_visited}')
            print('has current_room been visited: ', current_room in world_visited)
            if current_room not in world_visited:
                print(f'line 103 path: {path}')
                return path
            
            visited.add(current_room)
            print(f'{current_room} visited by bfs')
            print(f'line 110 visited: {visited}')
            neighbors = graph[current_room]
            print(f'neighbors: {neighbors}')
            neighbors_values = list(graph[current_room].values())
            neighbors_keys = list(graph[current_room].keys())
            print(f'neighbors_values: {neighbors_values}')
            print(f'neighbors_keys: {neighbors_keys}')
            if len(neighbors) == 1:
                path.append(neighbors_keys[0])
                new_room = neighbors_values[0]
                print(f'path: {path}')
                print(f'line 106 {current_room} neighbors: {graph[current_room]}')
            elif len(neighbors_values) > 1:
                for n in neighbors_values:
                    if n not in visited:
                        print(f'n: {n}')
                        index = neighbors_values.index(n)
                        path.append(neighbors_keys[index])
                        print(f'path: {path}')
                        new_room = n
                        return path

            for n in neighbors:
                new_path = list(current_path)
                new_path.append(n)


            print(f'line 134 new_room: {new_room}')
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

    print(graph)

    current_room = player.current_room.id

    status = dft(current_room, graph, visited)
    print(f'status: {status}')

    result = bfs(status[0], status[2], status[1])
    print(f'\nresult: {result}')

    for dir in result:
        player.travel(dir)
    traversal_path.extend(result)
    print(f'traversal_path: {traversal_path}')

    print('\n')
    print(f'line 151 current_room: {player.current_room.id}')

    status = dft(player.current_room.id, graph, visited)

    result = bfs(status[0], status[2], status[1])

    for dir in result:
        player.travel(dir)
    traversal_path.extend(result)
    print(f'\ntraversal_path: {traversal_path}')

    status = dft(player.current_room.id, graph, visited)

    result = bfs(status[0], status[2], status[1])

    for dir in result:
        player.travel(dir)
    traversal_path.extend(result)
    
    status = dft(player.current_room.id, graph, visited)

    result = bfs(status[0], status[2], status[1])

    for dir in result:
        player.travel(dir)
    traversal_path.extend(result)



traverse_world()

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
