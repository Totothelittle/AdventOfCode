import numpy as np
import re

def parse_input(filename):
    lines = []
    with open(filename, 'r') as file:
        dict_values = {}
        for line in file:
            if '|' in line:
                values = line.strip().split('|')
                if values[0] in dict_values:
                    dict_values[values[0]].append(values[1])
                else:
                    dict_values[values[0]] = [values[1]]
            else:
                lines.append(line.strip().split(','))
           
    return lines, dict_values

def check_update(updates, checklist):
    res  = 0
    res2 = 0
    for update in updates:
        res_check = 1
        fix_update = []
        for i_item, item in enumerate(update):
            if item in checklist:
                for checker in checklist[item]:
                    if checker in update and i_item > update.index(checker):
                        res_check = 0
                        fix_update = rebuild_update(update, checklist)
                        break
                        
        if res_check == 1:
            res  += int(update[int(len(update)/2)])
        else:
            res2 += int(fix_update[int(len(fix_update)/2)])
        
    return res, res2

def rebuild_update(update, checklist):
    fix_update = []
    for val in update:
        if not fix_update:
            fix_update.append(val)
        else:
            index_to_place = -1
            for i_fix, fix in enumerate(fix_update):
                if val in checklist and fix in checklist[val]:
                    index_to_place = i_fix
                    break
            if index_to_place < 0:
                fix_update.append(val)
            else:
                fix_update.insert(index_to_place, val)
    
    return fix_update


if __name__ == "__main__":
    day = 5

    small_filename = f"Advent of Code 2024/Day{day}/Test.in"
    big_filename = f"Advent of Code 2024/Day{day}/Input.in"
    gold_filename = f"Advent of Code 2024/Day{day}/GoldInput.in"
    
    updates, checklist = parse_input(big_filename)
    res, res2 = check_update(updates, checklist)
    print(res)
    print(res2)