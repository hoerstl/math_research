import pickle


with open("out.pickle", "rb") as file:
    passingsetsofNumbers = pickle.load(file)

for base in range(2, 10):
    print(f"For base {base}:")
    for set in passingsetsofNumbers:
        for number in set:
            print(("0" * (4 - len(number.get(base)))) + number.get(base), end=", ")
        print("")
