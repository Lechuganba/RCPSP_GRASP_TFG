import pandas as pd

from src import Const


def milisecs():
    inputPath = "../resources/opthrs/j30opt.sm"
    start = [22, " "]
    inputFile = open(inputPath, "r")
    lines = inputFile.readlines()
    media = 0
    total = (len(lines) -1 )- start[0]
    for k in range(start[0], len(lines) -1):
        line = lines[k]
        lineAux = line.split(start[1])
        numbers = getNumbersAux(lineAux, "j30")
        media = media + float(numbers[3])
    print("Media " + str(media/total))


def mediaMakespan():
    j30 = pd.read_csv("../results/compareOPTj30.csv")
    j60 = pd.read_csv("../results/compareOPTj60.csv")
    j90 = pd.read_csv("../results/compareOPTj90.csv")
    j120 = pd.read_csv("../results/compareOPTj120.csv")
    res = [j30, j60, j90, j120]
    for r in res:
        i = 0
        total = len(r.values)
        media = 0
        mediaOPT = 0
        dif = 0
        while i < total:
            res = r.values[i]
            media = media + res[2]
            mediaOPT = mediaOPT + res[1]
            dif = dif + res[3]
            i = i + 1
        print("Media: " + str(media/total))
        print("MediaOPT: " + str(mediaOPT/total))
        print("Dif: " + str(dif / total))

def mediaRND():
    j30 = pd.read_csv("../results/j30.csv")
    j60 = pd.read_csv("../results/j60.csv")
    j90 = pd.read_csv("../results/j90.csv")
    j120 = pd.read_csv("../results/j120.csv")
    res = [j30, j60, j90, j120]
    for r in res:
        i = 0
        total = len(r.values)
        media = 0
        mediaRND = 0
        while i < total:
            res = r.values[i]
            rnd = r.values[i+1]
            media = media + float(res[3].replace(";", ""))
            mediaRND = mediaRND + float(rnd[3].replace(";", ""))
            i = i + 2
        print("Media: " + str(media/(total/2)))
        print("MediaRND: " + str(mediaRND/(total/2)))


def alphaRND(dir):
    if dir == Const.J30:
        j30 = pd.read_csv("../results/j30.csv")
        compareRND(Const.J30, j30)
    elif dir == Const.J60:
        j60 = pd.read_csv("../results/j60.csv")
        compareRND(Const.J60, j60)
    elif dir == Const.J90:
        j90 = pd.read_csv("../results/j90.csv")
        compareRND(Const.J90, j90)
    elif dir == Const.J120:
        j120 = pd.read_csv("../results/j120.csv")
        compareRND(Const.J120, j120)


def compareRND(problemType, panda):
    outputPath = "../results/compareRND" + problemType + ".csv"
    outputFile = open(outputPath, "w")
    outputFile.write("alpha,count\n")
    i = 0
    cont = 0
    contRnd = 0
    draw = 0
    while i < len(panda.values):
        res = panda.values[i]
        rnd = panda.values[i+1]
        if res[2] == rnd[2]:
            draw = draw + 1
        elif res[2] < rnd[2]:
            cont = cont + 1
        else:
            contRnd = contRnd + 1
        i = i + 2
    outputFile.write("0.25, " + str(cont) + "\n")
    outputFile.write("RND, " + str(contRnd) + "\n")
    outputFile.write("DRAW, " + str(draw) + "\n")
    outputFile.close()


def processResults(dir):
    if dir == Const.J30:
        j30 = pd.read_csv("../results/j30.csv")
        compareOpt(Const.J30, j30)
    elif dir == Const.J60:
        j60 = pd.read_csv("../results/j60.csv")
        compareOpt(Const.J60, j60)
    elif dir == Const.J90:
        j90 = pd.read_csv("../results/j90.csv")
        compareOpt(Const.J90, j90)
    elif dir == Const.J120:
        j120 = pd.read_csv("../results/j120.csv")
        compareOpt(Const.J120, j120)


def compareOpt(problemType, panda):
    outputPath = "../results/compareOPT" + problemType + ".csv"
    outputFile = open(outputPath, "w")
    if problemType == Const.J30:
        inputPath = "../resources/opthrs/" + problemType + "opt.sm"
        start = [22, " "]
    else:
        inputPath = "../resources/opthrs/" + problemType + "hrs.sm"
        start = [5, "\t"]
    inputFile = open(inputPath, "r")
    lines = inputFile.readlines()
    outputFile.write("problemType, makespan, GRASP, diff\n")
    for result in panda.values:
        name = result[0]
        opts = findLines(lines, name, start, problemType)
        if result[1] == "0.25" and opts is not None:
            diff = result[2] - opts[2]
            outputFile.write(str(name ) + ", " + str(opts[2]) + ", " + str(result[2]) + ", " + str(diff) + "\n")


def findLines(lines, name, start, problemType):
    nameAux = name.split("_")
    i = nameAux[0][3:len(nameAux[0])]
    j = nameAux[1]
    for k in range(start[0], len(lines)):
        line = lines[k]
        lineAux = line.split(start[1])
        numbers = getNumbersAux(lineAux, problemType)
        if numbers[0] == int(i) and numbers[1] == int(j):
            return numbers
    return None


def getNumbersAux(a, problemType):
    numbers = []
    for i in range(0, len(a)):
        if problemType != Const.J30 and i == 3:
            break
        if a[i] != "":
            if a[i].__contains__("\n"):
                n = a[i].split("\n")
                if n[0] != '':
                    numbers.append(float(n[0]))
            else:
                numbers.append(int(a[i]))
    return numbers
