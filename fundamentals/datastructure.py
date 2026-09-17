#list
x = list()
x = ['a', '25', 'dog', 8.42]
print(x)

x = [m for m in range (8)]
print(x)

del(x[1])
print(x)
x.pop()
print(x)
x.reverse()
print(x)
x.sort()
print(x)
x.reverse()

#tuples
y = tuple(x)
print(y)
y = ([1,2],3)
del(y[0][0])
print(y)

#sets
z = set()
z = {3, 5, 10, 11}
print(z)
z = {3*x for x in range(10) if x>5}
print(z)

#dict
m = {'pork':25.3, 'beef':33.8, 'chicken':22.7}
print(m.keys())
print(m.values())
print(m.items())

my_list = [8, 10, 6, 2, 4]  # list to sort
swapped = True  # To enter the while loop.

while swapped:
    swapped = False  # no swaps so far
    for i in range(len(my_list) - 1):
        if my_list[i] > my_list[i + 1]:
            swapped = True  # a swap occurred!
            my_list[i], my_list[i + 1] = my_list[i + 1], my_list[i]

print(my_list)

