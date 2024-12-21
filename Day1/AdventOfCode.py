import numpy as np

def parse_input(filename):
    with open(filename, 'r') as file:
        first_list, second_list = zip(*(
            map(int, line.split()) for line in file if line.strip()
        ))
    
    return first_list, second_list

def sort_lists(l1, l2): 
    l1, l2 = list(l1), list(l2)
    l1.sort()
    l2.sort()

    diff_list = [abs(i2 - i1) for i1, i2 in zip(l1, l2)]
    return sum(diff_list)

def find_similarities(l1, l2):
    
    return sum([value * l2.count(value) for value in l1])

if __name__ == "__main__":
    day = 1

    small_filename = f"Advent of Code 2024/Day{day}/Test.in"
    big_filename = f"Advent of Code 2024/Day{day}/Input.in"
    gold_filename = f"Advent of Code 2024/Day{day}/GoldInput.in"
    
    l1, l2 = parse_input(big_filename)
    res = sort_lists(l1, l2)
    res2 = find_similarities(l1, l2)
    print(res)
    print(res2)