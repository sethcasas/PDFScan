import textract
from pathlib import Path
import os
import re
from tkinter import filedialog
from tkinter import *


def main():
    print("Scanned Document Filer\n")
    root = Tk()
    root.withdraw()

    global mainDir
    mainDir = Path(filedialog.askdirectory())

    print(f"Folder selected: {mainDir}")

    n = ""
    while n != "n" and n != "y":
        n = input("Would you like to file this folder? (y/n): ").lower()

    if n == "n":
        print("Exiting...")
        return 0

    i = 1
    for file in os.listdir(mainDir):
        if ".pdf" in file:
            contentArray = getContent(mainDir / file)
            docType = findDocumentType(contentArray)

            if docType == "LUP":
                name = findLUPName(contentArray)
            else:
                name = ""

            nameNfile(docType, name, file)
            print(f"Documents filed: {i}")
            i += 1


def getContent(filename):
    rawText = textract.process(filename, method='tesseract', language='eng')
    neatText = rawText.decode('utf-8')

    return cleanContent(neatText)


def cleanContent(contents):
    array = re.split("\n", contents)
    neatArray = []

    for a in array:
        if a and not re.fullmatch("[\s]*", a):
            neatArray.append(a)

    return neatArray


def findDocumentType(contentArray):
    for x in contentArray[0:9]:
        if "WLIC LAKE USE" in x:
            return "LUP"

        elif "Waiver and Consent" in x:
            return "WC"

        elif "Notice by First" in x:
            return "NoticeofMail"

        elif "FOB AGREEMENT" in x:
            return "FOBAgreement"

        elif "Assignment of Access" in x:
            return "AccessAreaAssignment"

        elif "Release Form" in x:
            return "AccessAreaRelease"

        elif "RELINQUISH FORM" in x:
            return "AccessAreaRelinquish"

        elif "Space Request" in x:
            return "AccessAreaRequest"

        elif "Sublease" in x:
            return "AccessAreaSublease"

        elif "ASSIGN LAKE USE" in x:
            return "AssignLakePrivileges"

    return "MISC"


def findLUPName(contentArray):
    for x in contentArray[3:14]:
        name = re.search(r"(?<=Name\s)\W?[a-z]*,\s[a-z]*", x, flags=re.IGNORECASE)
        if name:
            return name[0]

        name = re.search(r"(?<=to:\s)\W?[a-z]*,\s[a-z]*", x, flags=re.IGNORECASE)
        if name:
            return name[0]

        name = re.search(r"^\W?[a-z]*,\s[a-z]*", x, flags=re.IGNORECASE)
        if name:
            return name[0]

    return ""


def nameNfile(docType, name, filename):
    if "AccessArea" in docType:
        if not os.path.isdir(mainDir / "AccessArea/"):
            os.mkdir(mainDir / "AccessArea/")

        i = 1
        while os.path.isfile(mainDir / f"AccessArea/{docType}_{name}.pdf"):
            if i == 1:
                name = name + str(i)

            elif i > 10:
                name = name[:-2]
                name = name + str(i)

            elif i > 100:
                name = name[:-3]
                name = name + str(i)

            else:
                name = name[:-1]
                name = name + str(i)

            i += 1

        os.rename(mainDir / filename, mainDir / f"AccessArea/{docType}_{name}.pdf")

    else:
        if not os.path.isdir(mainDir / f"{docType}/"):
            os.mkdir(mainDir / f"{docType}/")

        i = 1
        while os.path.isfile(mainDir / f"{docType}/{docType}_{name}.pdf"):
            if i == 1:
                name = name + str(i)

            elif i > 10:
                name = name[:-2]
                name = name + str(i)

            elif i > 100:
                name = name[:-3]
                name = name + str(i)

            else:
                name = name[:-1]
                name = name + str(i)

            i += 1

        os.rename(mainDir / filename, mainDir / f"{docType}/{docType}_{name}.pdf")


main()
