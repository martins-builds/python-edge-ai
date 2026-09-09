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