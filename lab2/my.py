a = [0, 1, 2, 3]
a = a[0:2]
print a

a = [0]
a = a[0:2]
print a

a = [[0], [1], [2], [3]]
def pop_shortest_path_from_agenda(agenda):
    path = min(agenda, key=lambda n: len(n))
    agenda.remove(path)
    return path
print a
print pop_shortest_path_from_agenda(a)
print a
print pop_shortest_path_from_agenda(a)
print a


