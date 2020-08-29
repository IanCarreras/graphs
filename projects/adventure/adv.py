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

def traverse_world():   
    graph = {}
    visited = set()
    queue = Queue()
    stack = Stack()

    for i in range(len(world.rooms)):
        graph[i] = {}

    print(graph)

    for exit in player.current_room.get_exits():
        graph[player.current_room.id][exit] = player.current_room.get_room_in_direction(exit).id
    
    visited.add(player.current_room.id)
    print(graph)
    print(visited)



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
