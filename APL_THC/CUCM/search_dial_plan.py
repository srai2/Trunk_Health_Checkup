import re

def split_initial(route):
    route = route.replace("\+[14]+","")
    route = route.replace("\+44","")
    route = route.replace("\+1","")
    route = route.replace("\+.[14]+","")
    route = route.replace("\+.1","")
    route = route.replace("\+.44","")
    route = route.replace("\+","")

    if route[0]=="1":
        route=route[1:]
    if route[:2] == "44":
        route=route[2:]
    return route.replace("X", "[0-9]", 10)

def Pattern(routes):
    dial_patterns = []
    for route in routes:
        pattern = route
        route = split_initial(route)
        dial_patterns.append((route, pattern))
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
               dial_list.append(route[1])
    return list(set(dial_list))

#Testing Scripts
#search_dial_plan("200", ["\+1[2-5][02468]0XX[79]XXXX", "\+[14]+2[0-1][0-9]XXXXXXX", "\+55577+", "\+[14]+5[4-5][0-9]XXXXXXX", "\+1[2-5][02468]0XX[79]XXXX", "\+44[2-5][02468]0X06XXXX"])

