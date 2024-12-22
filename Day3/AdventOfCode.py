import numpy as np
import re

def parse_input(filename):
    occurences = []
    with open(filename, 'r') as file:
        for line in file:
            occurences.extend(re.findall("mul\(.?.?.?,.?.?.?\)|don't\(\)|do\(\)", line))
    
    return occurences

def uncorrupt_command(occurences):
    res = 0
    do_mult = True
    for occ in occurences:
        if "don't" in occ:
            do_mult = False
            mult = 0
        elif "do" in occ:
            do_mult = True
            mult = 0
        else:
            values = occ.split(",")
            if do_mult:
                mult = 1
                for value in values:
                    mult *= int(re.sub("\D", "", value)) 
            else:
                mult = 0
        
        res += mult
    return res

if __name__ == "__main__":
    day = 3

    small_filename = f"Advent of Code 2024/Day{day}/Test.in"
    big_filename = f"Advent of Code 2024/Day{day}/Input.in"
    gold_filename = f"Advent of Code 2024/Day{day}/GoldInput.in"
    
    occ = parse_input(big_filename)
    res = uncorrupt_command(occ)
    print(res)

    #res2 = uncorrupt_command(l, 1)
    #print(res2)