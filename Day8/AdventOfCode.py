import numpy as np
from itertools import combinations
import re

def parse_input(filename):
    with open(filename, 'r') as file:
        dict_values = {}
        for i_line, line in enumerate(file):
            for i_col, item in enumerate(line):
                if item != "." and item != "\n":
                    if item not in dict_values:
                        dict_values[item] = [(i_line, i_col)]
                    else:
                        dict_values[item].append((i_line, i_col))
        matrix_size = (i_line, i_col)
    return dict_values, matrix_size

def create_antinodes(antennas, matrix_size, long_waves = False):
    antinodes  = []

    for antenna_type, antenna_list in antennas.items():
        antenna_pairs = list(combinations(antenna_list, 2))
        for pair in antenna_pairs:
            distance = np.array(pair[1]) - np.array(pair[0])
            if not long_waves:
                antinode1 = np.array(pair[0]) - distance
                antinode2 = np.array(pair[1]) + distance

                if 0 <= antinode1[0] <= matrix_size[0] and 0 <= antinode1[1] <= matrix_size[1]:
                    antinodes.append(tuple(antinode1))
                if 0 <= antinode2[0] <= matrix_size[0] and 0 <= antinode2[1] <= matrix_size[1]:
                    antinodes.append(tuple(antinode2))
            else:
                out_of_bound_m = False
                out_of_bound_p = False
                iteration = 1
                while(not out_of_bound_m or not out_of_bound_p):
                    antinode1 = np.array(pair[0]) - iteration*distance
                    antinode2 = np.array(pair[1]) + iteration*distance

                    if 0 <= antinode1[0] <= matrix_size[0] and 0 <= antinode1[1] <= matrix_size[1]:
                        antinodes.append(tuple(antinode1))
                    else:
                        out_of_bound_m = True
                    if 0 <= antinode2[0] <= matrix_size[0] and 0 <= antinode2[1] <= matrix_size[1]:
                        antinodes.append(tuple(antinode2))
                    else:
                        out_of_bound_p = True
                    iteration += 1

                # Antennas are also antinodes
                antinodes.append(tuple(pair[0]))
                antinodes.append(tuple(pair[1]))
   
    return len(set(antinodes))

if __name__ == "__main__":
    day = 8

    small_filename = f"Advent of Code 2024/Day{day}/Test.in"
    big_filename = f"Advent of Code 2024/Day{day}/Input.in"
    gold_filename = f"Advent of Code 2024/Day{day}/GoldInput.in"
    
    antennas, matrix_size = parse_input(big_filename)
    res = create_antinodes(antennas, matrix_size)
    print(res)
    
    res2 = create_antinodes(antennas, matrix_size, True)
    print(res2)
