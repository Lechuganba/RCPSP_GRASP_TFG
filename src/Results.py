import pandas as pd

from src import Const


def milisecs():
    inputPath = "../resources/opthrs/j30opt.sm"
    start = [22, " "]
    inputFile = open(inputPath, "r")
    lines = inputFile.readlines()
    media = 0
    total = (len(lines) - 1) - start[0]
    for k in range(start[0], len(lines) - 1):
        line = lines[k]
        lineAux = line.split(start[1])
        numbers = getNumbersAux(lineAux, "j30")
        media = media + float(numbers[3])
    print("Media " + str(media / total))


def mediaMakespan():
    j30 = pd.read_csv("../results/j30.csv")
    j60 = pd.read_csv("../results/j60.csv")
    j90 = pd.read_csv("../results/j90.csv")
    j120 = pd.read_csv("../results/j120.csv")
    res = [j30, j60, j90, j120]
    for r in res:
        i = 3
        total = len(r.values)
        media = 0
        media2 = 0
        dur = 0
        dur2 = 0
        while i < total:
            res = r.values[i]
            if res[0] == 100:
                media = media + res[2]
                dur = dur + res[3]
            elif res[0] == 200:
                media2 = media2 + res[2]
                dur2 = dur2 + res[3]
            i = i + 4
        print("Media: " + str(media / 50))
        print("Ms: " + str(dur / 50))
        print("Media2: " + str(media2 / 50))
        print("Ms: " + str(dur2 / 50))


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
            rnd = r.values[i + 1]
            media = media + float(res[3].replace(";", ""))
            mediaRND = mediaRND + float(rnd[3].replace(";", ""))
            i = i + 2
        print("Media: " + str(media / (total / 2)))
        print("MediaRND: " + str(mediaRND / (total / 2)))


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
    outputFile.write("alpha, iterations, count\n")
    i = 0
    c0 = 0
    c1 = 0
    c2 = 0
    c3 = 0
    c01 = 0
    c11 = 0
    c21 = 0
    c31 = 0
    while i < len(panda.values):
        vA = panda.values[i]
        cA = panda.values[i + 1]
        sA = panda.values[i + 2]
        rA = panda.values[i + 3]
        mA = [vA[2], cA[2], sA[2], rA[2]]
        best = getMin(mA)
        if best == 0:
            c0 = c0 + 1
        elif best == 1:
            c1 = c1 + 1
        elif best == 2:
            c2 = c2 + 1
        elif best == 3:
            c3 = c3 + 1
        vB = panda.values[i + 4]
        cB = panda.values[i + 5]
        sB = panda.values[i + 6]
        rB = panda.values[i + 7]
        m1 = [vB[2], cB[2], sB[2], rB[2]]
        best1 = getMin(m1)
        if best1 == 0:
            c01 = c01 + 1
        elif best1 == 1:
            c11 = c11 + 1
        elif best1 == 2:
            c21 = c21 + 1
        elif best1 == 3:
            c31 = c31 + 1
        i = i + 8
    outputFile.write("0.25, 100, " + str(c0) + "\n")
    outputFile.write("0.5, 100, " + str(c1) + "\n")
    outputFile.write("0.75, 100,  " + str(c2) + "\n")
    outputFile.write("RND, 200,  " + str(c3) + "\n")
    outputFile.write("0.25, 200, " + str(c01) + "\n")
    outputFile.write("0.5, 200, " + str(c11) + "\n")
    outputFile.write("0.75, 200,  " + str(c21) + "\n")
    outputFile.write("RND, 200,  " + str(c31) + "\n")
    outputFile.close()


def getMin(m):
    best = 0
    valor = 100000000
    for i in range(0, len(m)):
        if m[i] < valor:
            valor = m[i]
            best = i
    return best


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
            outputFile.write(str(name) + ", " + str(opts[2]) + ", " + str(result[2]) + ", " + str(diff) + "\n")


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
