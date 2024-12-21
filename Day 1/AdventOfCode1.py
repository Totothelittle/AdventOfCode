import numpy as np

def parseInput(filename):
    with open(filename, 'r') as f:
        first_list, second_list = zip(*(
            map(int, line.split()) for line in f if line.strip()
        ))
    print("Hello world")

if __name__ == "__main__":
    filename = "Day1.in"
    parseInput(filename)