#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 7
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import itertools
import math
import re

INPUTFILE = "Advent of Code 2024/Day7/Input.in"

SAMPLE_CASES = [
    (
        """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
        """,
        3749
    ),
]

SAMPLE_CASES2 = [
    (
        """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
        """,
        11387
    ),
]


Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str, strip=True, blank_lines=False) -> Lines:
    return load_text(
        Path(infile).read_text(), strip=strip, blank_lines=blank_lines
    )

def load_text(text: str, strip=True, blank_lines=False) -> Lines:
    if strip:
        lines = [line.strip() for line in text.strip("\n").split("\n")]
    else:
        lines = text.strip("\n").split("\n")
    if blank_lines:
        return lines
    return [line for line in lines if line.strip()]

def parse_sections(lines: Lines) -> Sections:
    result = []
    sect = []
    for line in lines:
        if not line.strip():
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


# Solution

PLUS, MULTIPLY, CONCAT = "+", "*", "||"
OPERATORS = [PLUS, MULTIPLY]
OPERATORS2 = [PLUS, MULTIPLY, CONCAT]


def left_right_eval(operands, operators):
    assert len(operands) == len(operators) + 1
    result = operands[0]
    expr = [str(operands[0])]
    for val, op in zip(operands[1:], operators):
        expr.extend([op, str(val)])
        if op == PLUS:
            result += val
        elif op == MULTIPLY:
            result *= val
        elif op == CONCAT:
            result = int(f"{result}{val}")
    expression = ' '.join(expr)
    return result, expression


def resolve(value, operands) -> bool:
    n = len(operands) - 1
    # print(f"-- resolve({value}, {operands}")
    for operators in itertools.product(OPERATORS, repeat=n):
        result, expression = left_right_eval(operands, operators)
        if result == value:
            # print(f".. {result} <- {expression}")
            return True
    return False


def resolve2(value, operands) -> bool:
    n = len(operands) - 1
    # print(f"-- resolve2({value}, {operands}")
    for operators in itertools.product(OPERATORS2, repeat=n):
        result, expression = left_right_eval(operands, operators)
        if result == value:
            # print(f".. {result} <- {expression}")
            return True
    return False

def parse_input(lines: Lines) -> list[Any]:
    result = []
    for line in lines:
        if not line.strip():
            continue
        value, rest = line.strip().split(":")
        operands = list(map(int, rest.split()))
        result.append((int(value), operands))
    return result

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    result = 0
    cases = parse_input(lines)
    for value, operands in cases:
        if resolve2(value, operands):
            result += value
    return result

def solve(lines: Lines) -> int:
    """Solve the problem."""
    result = 0
    cases = parse_input(lines)
    for value, operands in cases:
        if resolve(value, operands):
            result += value
    return result


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 42283209483350
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 1026766857276279
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
