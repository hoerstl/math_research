import os
import pickle
import xlsxwriter



def exportToXLSX(filename):
    with xlsxwriter.Workbook(filename) as workbook:
        leftCodes, rightCodes, tieCodes = getData()
        leftworksheet = workbook.add_worksheet("Left Wins")
        rightworksheet = workbook.add_worksheet("Right Wins")
        tieworksheet = workbook.add_worksheet("Ties")

        analyzeCodes(leftworksheet, leftCodes)
        analyzeCodes(rightworksheet, rightCodes)
        analyzeCodes(tieworksheet, tieCodes)


def analyzeCodes(worksheet, codes):
    headings = getHeadings()
    for col, heading in enumerate(headings):
        worksheet.write(0, col, heading)
    for row, code in enumerate(codes, start=1):
        worksheet.write(row, 0, code)
        data = analyze(code)
        for col, datum in enumerate(data):
            worksheet.write(row, col + 1, datum)


def analyze(code: str):
    data = [
        code.count("S"),
        code.count("P"),
        code.count("D"),
        code.count("T"),
        code.count("⬇"),
        code.count("⬆")
    ]
    return data


def getHeadings():
    headings = [
        "Code",
        "# of S's",
        "# of P's",
        "# of D's",
        "# of T's",
        "# of ⬇'s",
        "# of ⬆'s"
    ]
    return headings


def getData(verbose=False):
    if os.path.exists("leftwins.save"):
        with open("leftwins.save", "rb") as file:
            leftwins = pickle.load(file)
    else:
        leftwins = []

    if verbose:
        print("Here are the boards where left wins:")
        for winningCode in leftwins:
            print(winningCode)

    if os.path.exists("rightwins.save"):
        with open("rightwins.save", "rb") as file:
            rightwins = pickle.load(file)
    else:
        rightwins = []

    if verbose:
        print("Here are the boards where right wins:")
        for winningCode in rightwins:
            print(winningCode)

    if os.path.exists("ties.save"):
        with open("ties.save", "rb") as file:
            ties = pickle.load(file)
    else:
        ties = []

    if verbose:
        print("Here are the boards where both players tie:")
        for winningCode in ties:
            print(winningCode)

    return leftwins, rightwins, ties


exportToXLSX("AD non-intersting size 15.xlsx")

