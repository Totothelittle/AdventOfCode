import numpy as np
import re

def parse_input(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append([char for char in line.strip()])
    
    return lines

def find_all_xmas(lines):
    res = 0

    #Find all 'X'
    x_indexes = []
    n_line = 0
    for line in lines:
        x_line_indexes = [(n_line, x_index) for x_index, x_value in enumerate(line) if x_value == 'X']
        x_indexes.extend(x_line_indexes)
        n_line += 1
    
    #Get all ways
    nb_ways = 0
    next_letters = "MAS"
    checklist = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for x in x_indexes:
        for i_check in checklist:
            check_way = 1
            for i_letter, letter in enumerate(next_letters):
                next_row = x[0] + i_check[0]*(i_letter+1)
                next_col = x[1] + i_check[1]*(i_letter+1)
                if  0 <= next_row < len(lines) and 0 <= next_col < len(lines[0]):
                    if lines[next_row][next_col] != letter:
                        check_way = 0
                        break
                else:
                    check_way = 0
                    break
            nb_ways += check_way
                
    return nb_ways

def find_all_x_mas(lines):
    #Find all 'A'
    a_indexes = []
    n_line = 0
    for line in lines:
        a_line_indexes = [(n_line, a_index) for a_index, a_value in enumerate(line) if a_value == 'A']
        a_indexes.extend(a_line_indexes)
        n_line += 1

    #Get all ways
    nb_ways = 0
    checklist = [(-1, -1), (-1, 1)]
    for a in a_indexes:
        check_way = 1
        for i_check in checklist:
            row_check_1 = a[0] + i_check[0]
            col_check_1 = a[1] + i_check[1]
            row_check_2 = a[0] - i_check[0]
            col_check_2 = a[1] - i_check[1]

            if  0 < a[0] < len(lines) - 1 and 0 < a[1] < len(lines[0]) - 1:
                if lines[row_check_1][col_check_1] == 'M':
                    if lines[row_check_2][col_check_2] != 'S':
                        check_way = 0
                        break
                elif lines[row_check_1][col_check_1] == 'S':
                    if lines[row_check_2][col_check_2] != 'M':
                        check_way = 0
                        break
                else:
                    check_way = 0
                    break
            else:
                check_way = 0
                break

        nb_ways += check_way

    return nb_ways

if __name__ == "__main__":
    day = 4

    small_filename = f"Advent of Code 2024/Day{day}/Test.in"
    big_filename = f"Advent of Code 2024/Day{day}/Input.in"
    gold_filename = f"Advent of Code 2024/Day{day}/GoldInput.in"
    
    lines = parse_input(big_filename)
    res = find_all_xmas(lines)
    print(res)

    res2 = find_all_x_mas(lines)
    print(res2)