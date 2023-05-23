class Number:

    def __init__(self, value):
        self.value = value

    def get(self, base):
        val = ""
        base10num = self.value
        do = True

        while base10num != 0 or do:
            val = str(base10num % base) + val
            base10num //= base
            do = False

        return val

    @staticmethod
    def xor(*args: []):
        binaryStrings = []
        maxLength = -1
        for number in args:
            binaryString = number.get(2)
            binaryStrings.append(binaryString)
            maxLength = max(len(binaryString), maxLength)

        for bnumber in range(len(binaryStrings)):
            binaryStrings[bnumber] = ("0" * (maxLength - len(binaryStrings[bnumber]))) + binaryStrings[bnumber]

        result = ""
        for i in range(maxLength):
            count = 0
            for bS in binaryStrings:
                if bS[i] == "1":
                    count += 1
            if count % 2 == 1:
                result += "1"
            else:
                result += "0"

        noLeadingZeroes = ""
        oneFound = False
        for character in result:
            if character == "1":
                oneFound = True
            if oneFound:
                noLeadingZeroes += character
        if noLeadingZeroes == "":
            noLeadingZeroes = "0"
        return noLeadingZeroes


    def __str__(self):
        return self.value










def test(v1, v2):
    if v1 == v2:
        print("Test passed.")
    else:
        print(f"Test failed between {v1} and {v2}.")


if __name__ == '__main__':
    test(Number(0).get(3), "0")
    test(Number(12).get(3), "110")
    test(Number(12).get(2), "1100")
    test(Number(2).get(9), "2")
    test(Number(15).get(3), "120")
    test(Number(15).get(2), "1111")
