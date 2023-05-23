import pickle
from Basen import *




def passesxor(a, b, c):
    a = a.get(2)
    b = b.get(2)
    c = c.get(2)

    longest = 0
    for number in [a, b, c]:
        longest = max(longest, len(number))

    a = "0" * (longest - len(a)) + a
    b = "0" * (longest - len(b)) + b
    c = "0" * (longest - len(c)) + c

    result = ""
    for digit in range(longest):
        count = 0
        for num in [a, b, c]:
            if num[digit] == "1":
                count += 1
        if count % 2 == 0:
            result += "0"
        else:
            result += "1"

    if result == "0" * longest:
        return True
    return False

#print(passesxor(Number(10), Number(5), Number(15)))



if __name__ == '__main__':
    v1 = Number(2)
    v2 = Number(3)
    v3 = Number(8)
    passingsetsofNumbers = []
    l = [v1, v2, v3]
    while True:
        if passesxor(*l):
            passingsetsofNumbers.append(l.copy())
        i = input(f"Here's the board:\n{l[0].get(2)}, {l[1].get(2)}, {l[2].get(2)}\nChoose a number to change (0, 1, 2): ")
        if i.lower() == "":
            break
        else:
            i = int(i)
        change = int(input(f"Change {l[i].get(2)} to: "))
        l[i] = Number(change)


    with open("out.pickle", "wb") as file:
        pickle.dump(passingsetsofNumbers, file)








