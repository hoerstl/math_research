import os
import pickle


def listData():
    if os.path.exists("leftwins.save"):
        with open("leftwins.save", "rb") as file:
            leftwins = pickle.load(file)
    else:
        leftwins = []

    print("Here are the boards where left wins:")
    for winningCode in leftwins:
        print(winningCode)

    if os.path.exists("rightwins.save"):
        with open("rightwins.save", "rb") as file:
            rightwins = pickle.load(file)
    else:
        rightwins = []

    print("Here are the boards where right wins:")
    for winningCode in rightwins:
        print(winningCode)

    if os.path.exists("ties.save"):
        with open("ties.save", "rb") as file:
            ties = pickle.load(file)
    else:
        ties = []

    print("Here are the boards where both players tie:")
    for winningCode in ties:
        print(winningCode)


listData()
