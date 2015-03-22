__author__ = 'srai2'
import re

def split_initial(route):
    if route[0]=="\\":
        route = route[2:]
    if route[0]==".":
        route=route[1:]
    if route[0]=="1":
        route=route[1:]
    if route[:2] == "44":
        route=route[2:]
    return " ".join(word.rstrip("X") for word in route.split())

def Pattern(routes):
    dial_patterns = []
    for route in routes:
        pattern = route
        route = split_initial(route)
        if route[:2]== "44":
            route = route[2:]
        elif route[:1]=="9":
            route = route[1:]
        dial_patterns.append((route.replace("X", "[0-9]", 5), pattern))
    return dial_patterns



def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def get_pattern_with_proper_length(pattern, length):
    start_point = find(pattern, '[')
    end_point = find(pattern, ']')
    points = sorted(start_point+end_point)
    value = 0
    for index in range(length):
        if value >= index:
            if find(points, value):
                value = points[points.index(value)+1]+1
            else:
                value = value+1
        else:
            value = value+1
    return pattern[:value]



def search_dial_plan(string, pattern):
    dial_list = []
    string_length= len(string)
    for route in Pattern(pattern):
       dial_pattern = get_pattern_with_proper_length(route[0], string_length)
       if route[1][-4:] == ".911":
            pass
       else:
           regex = re.compile(dial_pattern)
           if regex.match(string):
               print route[1]
               dial_list.append(route[1])
    return dial_list


