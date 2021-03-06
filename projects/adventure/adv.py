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
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited_graph = {}

# solution for test_cross
# traversal_path = ['n','n','s','s','e','e','w','w','w','w','e','e','s','s']

# solution for test_loop
# traversal_path = ['n','n','s','s','e','e','w','w','s','s','w','w','n','n','e','e']

def check_neighbors(current_room, next_room):
    if current_room == next_room:
        return 'same room'
    elif current_room.n_to == next_room:
        return 'n'
    elif current_room.s_to == next_room:
        return 's'
    elif current_room.w_to == next_room:
        return 'w'
    elif current_room.e_to == next_room:
        return 'e'

def bfs(current_room, next_room):
    queue = Queue()
    queue.enqueue([current_room])
    visited = set()
    while queue.size() > 0:
        path = queue.dequeue()
        current = path[-1]
        if current not in visited:
            if current == next_room:
                return path
            visited.add(current)
            for neighbor in current.get_exits():
                new_path = list(path)
                new_path.append(current.get_room_in_direction(neighbor))
                queue.enqueue(new_path)

# dfs
stack = Stack()
stack.push([player.current_room])
visited = set()
while stack.size() > 0:
    path = stack.pop()
    current = path[-1]
    player_position = check_neighbors(player.current_room, current)
    
    if current.id not in visited:
        if player_position != None and player_position != 'same room':
            player.travel(player_position)
            traversal_path.append(player_position)

        visited_graph[current.id] = {}
        visited.add(current.id)
        
        for exit in current.get_exits():
            visited_graph[player.current_room.id].update({exit: None})
        
        if player_position == 'same room':
            for next_room in player.current_room.get_exits():
                new_path = path + [player.current_room.get_room_in_direction(next_room)]
                stack.push(new_path)
        else:
            shortest = bfs(player.current_room, path[-1])
            position = []
            for room in shortest:
                direction = check_neighbors(player.current_room, room)
                if direction != 'same room':
                    position.append(direction)
                    player.travel(direction)
            traversal_path += position
            for next_room in player.current_room.get_exits():
                new_path = path + [player.current_room.get_room_in_direction(next_room)]
                stack.push(new_path)


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