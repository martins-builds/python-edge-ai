def say_hello(name):
    print('Hello' , name)

while True:
    user_input = input("Enter something >> ")
    if user_input == '0':
        print('we are done')
        break
for i in range(3):
    print(i);

item = 'Banana'
Item = 'Apple'
Item_name = 'Orange'
integer = 1234
isHappy = False
naughty_list = ['martins', 'oviawe', 'osayuki']

print(item, Item)

print('Hello ' + Item_name)
print(integer)
print(isHappy)
print(naughty_list)

say_hello('Martins')

number = input('please provide a number >> ')

try:
    print(10 + int(number))

except:
    print('That is not a valid Number!')