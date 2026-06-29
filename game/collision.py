def distance(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return (dx * dx + dy * dy) ** 0.5

def in_range(a, b, required_distance):
    return distance(a, b) < required_distance
