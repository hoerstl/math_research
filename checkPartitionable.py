from Basen import Number
import copy

def checkpartitionable(base10Lists):
    numberLists = copy.deepcopy(base10Lists)
    for numberList_ in range(len(numberLists)):
        for number_ in range(len(numberLists[numberList_])):
            numberLists[numberList_][number_] = Number(numberLists[numberList_][number_])

    for list_ in range(len(base10Lists)):
        if Number.xor(*numberLists[list_]) == "0":
            print(f"Yes you can partition: {base10Lists[list_]}")
        else:
            print(f"No you cannot partition: {base10Lists[list_]}")




if __name__ == '__main__':
    listsofNumbers = []
    while True:

        numbers = []
        while True:
            n = input("Give me a number to add to the set: ")
            if n == "" or n == "q":
                break
            numbers.append(int(n))
        listsofNumbers.append(numbers.copy())
        if n == "q":
            break


    checkpartitionable(listsofNumbers)


