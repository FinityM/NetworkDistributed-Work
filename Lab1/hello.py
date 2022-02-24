print("Hello")

age = 10


def getname():
    print("What is your name? ")
    name = input()

    print("Hello there your age is " + str(age))

    print("Hello there " + str(name))

    if age > 5:
        print("Age is greater than 5")
        print("Other One")
    elif age == 10:
        print("yes")


getname()
