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

my_list = []
swapped = True
num = int(input("How many elements do you want to sort: "))

for i in range(num):
    val = float(input("Enter a list element: "))
    my_list.append(val)

while swapped:
    swapped = False
    for i in range(len(my_list) - 1):
        if my_list[i] > my_list[i + 1]:
            swapped = True
            my_list[i], my_list[i + 1] = my_list[i + 1], my_list[i]

print("\nSorted:")
print(my_list)

list_1 = [1]
list_2 = list_1[:] #not copying the memory
list_1[0] = 2
print(list_2)



