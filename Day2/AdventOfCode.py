import numpy as np

def parse_input(filename):
    with open(filename, 'r') as file:
        lines = [list(map(int, line.split())) for line in file if line.strip()]
    
    return lines

def check_safety(lines_buffer, lvl_tolerance):
    nb_safe_report = 0
    i_line = 1
    for line in lines_buffer:
        diff_check, diff_abs = generate_diffs(line)

        if (all(diff_check) or not any(diff_check)) and all(diff_abs):
            nb_safe_report += 1
        else:
            if lvl_tolerance > 0:
                for i_item in range(len(line)):
                    line_to_fix = line.copy()
                    line_to_fix.pop(i_item)
                    diff_check, diff_abs = generate_diffs(line_to_fix)
                    if (all(diff_check) or not any(diff_check)) and all(diff_abs):
                        nb_safe_report += 1
                        break
        i_line += 1

    return nb_safe_report

def generate_diffs(line):
    diff = []
    for i_level in range(len(line)-1):
        diff.append(line[i_level] - line[i_level + 1])
    diff_check = [i_diff > 0 for i_diff in diff]
    diff_abs = [0 < abs(i_diff) <= 3 for i_diff in diff]

    return diff_check, diff_abs

if __name__ == "__main__":
    day = 2

    small_filename = f"Advent of Code 2024/Day{day}/Test.in"
    big_filename = f"Advent of Code 2024/Day{day}/Input.in"
    gold_filename = f"Advent of Code 2024/Day{day}/GoldInput.in"
    
    l = parse_input(big_filename)
    res = check_safety(l, 0)
    print(res)

    res2 = check_safety(l, 1)
    print(res2)