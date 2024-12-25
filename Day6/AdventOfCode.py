import numpy as np
import re

def parse_input(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
           
    return lines

def guard_patrol(guard_map):
    res  = 0
    directions = {">" : (0, 1), "<" : (0, -1), "v" : (1, 0), "^": (-1, 0)}

    # Get start index
    for i_line, line in enumerate(guard_map):
        if "^" in line:
            guard_index = (i_line, line.index("^"))
            break

    # Moving phase
    while( 0 <= guard_index[0] < len(guard_map) and 0 <= guard_index[1] < len(guard_map[0])):
        guard = guard_map[guard_index[0]][guard_index[1]]
        next_index = (guard_index[0] + directions[guard][0],
                      guard_index[1] + directions[guard][1])
        
        if 0 > next_index[0] or next_index[0] >= len(guard_map) or 0 > next_index[1] or next_index[1] >= len(guard_map[0]):
            guard_map[guard_index[0]] = update_line(guard_index, 'X', guard_map)
            guard_index = next_index
        else:
            if guard_map[next_index[0]][next_index[1]] != "#":
                guard_map[next_index[0]]  = update_line(next_index, guard, guard_map)
                guard_map[guard_index[0]] = update_line(guard_index, 'X', guard_map)
                guard_index = next_index
            else:
                guard_map[guard_index[0]] = update_line(guard_index, change_direction(guard), guard_map)
     
    # Counting phase
    for line in guard_map:
        res += line.count('X')

    return res

def guard_loop(guard_map):
    directions = {">" : (0, 1), "<" : (0, -1), "v" : (1, 0), "^": (-1, 0)}
    edges = {">" : "-", "<" : "-", "v" : "|", "^": "|"}
    blocks = []

    # Get start index
    for i_line, line in enumerate(guard_map):
        if "^" in line:
            guard_index = (i_line, line.index("^"))
            break

    # Get all blockages
    for i_line, line in enumerate(guard_map):
        for i_col, value in enumerate(line):
            if value == "#":
                blocks.append((i_line, i_col))

    # Moving phase
    direction_updated = False
    crossed = False
    vertices = []
    loop_found = 0
    while( 0 <= guard_index[0] < len(guard_map) and 0 <= guard_index[1] < len(guard_map[0])):
        guard = guard_map[guard_index[0]][guard_index[1]]
        next_index = (guard_index[0] + directions[guard][0],
                      guard_index[1] + directions[guard][1])
        
        if 0 > next_index[0] or next_index[0] >= len(guard_map) or 0 > next_index[1] or next_index[1] >= len(guard_map[0]):
            guard_map[guard_index[0]] = update_line(guard_index, edges[guard], guard_map)
            guard_index = next_index
        else:
            if guard_map[next_index[0]][next_index[1]] != "#":
                # Try loop
                if not direction_updated and vertices:
                    loop_found += find_loops(guard, guard_index, guard_map, vertices)

                # Normal graph
                if not direction_updated and not crossed:
                    guard_map[guard_index[0]] = update_line(guard_index, edges[guard], guard_map)
                else:
                    guard_map[guard_index[0]] = update_line(guard_index, "+", guard_map)
                    if direction_updated:
                        vertices.append(guard_index)
                    direction_updated = False
                    crossed = False

                if guard_map[next_index[0]][next_index[1]] == "-" or guard_map[next_index[0]][next_index[1]] == "|":
                    crossed = True
                guard_map[next_index[0]]  = update_line(next_index, guard, guard_map)

                guard_index = next_index

            else:
                guard_map[guard_index[0]] = update_line(guard_index, change_direction(guard), guard_map)
                direction_updated = True
     
    return loop_found

def find_loops(guard, guard_index, guard_map, vertices):
    loop_found = 0
    block_found = 0

    # Get map and vertices already existing in array
    guard_map_array = np.array([list(line) for line in guard_map])
    visited = vertices.copy()
    guard_position = guard_index
    try_guard = guard

    # Create new potential vertice
    visited.append(guard_index)

    while block_found >= 0 and loop_found == 0:
        # Update guard direction
        try_guard = change_direction(try_guard)

        # Re-initialise block found
        block_found = -1

        # Target line to check
        if try_guard == ">":
            line_check = guard_map_array[guard_position[0], guard_position[1]+1:]
        elif try_guard == "v":
            line_check = guard_map_array[guard_position[0]+1:, guard_position[1]]
        elif try_guard == "<":
            line_check = np.flip(guard_map_array[guard_position[0], :guard_position[1]])
        else:
            line_check = np.flip(guard_map_array[:guard_position[0], guard_position[1]])

        # Search next block
        if '#' in line_check:
            block_found = list(line_check).index('#')
            
            # Create a new vertex
            if block_found > 0:
                if try_guard == ">":
                    new_vertex = (guard_position[0], guard_position[1] + block_found)
                elif try_guard == "v":
                    new_vertex = (guard_position[0] + block_found, guard_position[1])
                elif try_guard == "<":
                    new_vertex = (guard_position[0], guard_position[1] - block_found)
                else:
                    new_vertex = (guard_position[0] - block_found, guard_position[1])
                
                # Update guard position
                guard_position = new_vertex

                # Check if a loop can be formed at this block
                if new_vertex in visited:
                    loop_found = 1
                else:
                    visited.append(new_vertex)
                    

    return loop_found

def change_direction(guard):
    if guard == ">":
        return "v"
    elif guard == "v":
        return "<"
    elif guard == "<":
        return "^"
    else:
        return ">"
    
def update_line(index, char, guard_map):
    line = list(guard_map[index[0]])
    line[index[1]] = char

    return "".join(line)
    
if __name__ == "__main__":
    day = 6

    small_filename = f"Advent of Code 2024/Day{day}/Test.in"
    big_filename = f"Advent of Code 2024/Day{day}/Input.in"
    gold_filename = f"Advent of Code 2024/Day{day}/GoldInput.in"
    
    guard_map = parse_input(big_filename)
    guard_map_loop = guard_map.copy()
    res = guard_patrol(guard_map)
    print(res)

    res2 = guard_loop(guard_map_loop)
    print(res2)
