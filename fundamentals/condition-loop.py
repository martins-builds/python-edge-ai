n=int(input("Enter a number: "))
if n >= 100:
    print(bool(n))
else:
    print(bool(n))

# Read two numbers
number1 = int(input("Enter the first number: "))
number2 = int(input("Enter the second number: "))

# Choose the larger number
if number1 > number2:
    larger_number = number1
else:
    larger_number = number2

# Print the result
print("The larger number is:", larger_number)

x = [1,2,3,4,56,7,89,9887,4,34,543,435,434,3454,1000]
largest = x[0]
print(largest)
for i in range (10):
    if largest < x[i]:
        largest = x[i]
print(largest)