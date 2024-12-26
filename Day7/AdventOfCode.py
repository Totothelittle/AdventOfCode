import numpy as np
from itertools import product
import re

def parse_input(filename):
    with open(filename, 'r') as file:
        list_values = []
        for line in file:
            list_values.append((int(line.strip().split(":")[0]), list(map(int, line.strip().split(":")[1].split(" ")[1:]))))
           
    return list_values

def find_op_combinations(list_values, concatenation=False):
    final_res  = 0

    type_operations = ["+", "*"]
    if concatenation:
        type_operations.append("||")

    for item in list_values:
        key = item[0]
        values = item[1]

        operations = ['+', '*']
        if concatenation:
            operations.append('||')
        combinations = list(product(operations, repeat=len(values)-1))

        possibilities = check_operations(key, values, combinations)
        if possibilities > 0:
            final_res += key
        
    return final_res

def check_operations(key, values, combinations):
    possibility = 0

    for comb in combinations:

        res = values[0]
        for i_op, op in enumerate(comb):
            if op == "+":
                res += values[i_op + 1]
            elif op == "*":
                res *= values[i_op + 1]
            else:
                res = int(str(res) + str(values[i_op + 1]))

        if res == key:
            possibility = 1

    return possibility

if __name__ == "__main__":
    day = 7

    small_filename = f"Advent of Code 2024/Day{day}/Test.in"
    big_filename = f"Advent of Code 2024/Day{day}/Input.in"
    gold_filename = f"Advent of Code 2024/Day{day}/GoldInput.in"
    
    values = parse_input(big_filename)
    res = find_op_combinations(values)
    print(res)
    
    res2 = find_op_combinations(values, True)
    print(res2)
