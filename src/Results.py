import pandas as pd


def processResults():
    j30 = pd.read_csv("../results/j30.csv")
    j60 = pd.read_csv("../results/j60.csv")
    j90 = pd.read_csv("../results/j90.csv")
    j120 = pd.read_csv("../results/j120.csv")

    compareOpt("j30", j30)
    compareOpt("j60", j60)
    compareOpt("j90", j90)
    compareOpt("j120", j120)


def compareOpt(problemType, panda):
    draw = 0
    worse = 0
    better = 0
    outputPath = "../results/compare" + problemType + ".csv"
    outputFile = open(outputPath, "w")
    if problemType == "j30":
        inputPath = "../resources/opthrs/" + problemType + "opt.sm"
        start = [22, " "]
    else:
        inputPath = "../resources/opthrs/" + problemType + "hrs.sm"
        start = [5, "\t"]
    inputFile = open(inputPath, "r")
    lines = inputFile.readlines()
    outputFile.write("problemType, GRASP, OPT/HEUR, DRAW\n")
    for result in panda.values:
        name = result[0]
        opts = findLine(lines, name, start, problemType)
        if opts[2] == result[2]:
            draw = draw + 1
        elif opts[2] > result[2]:
            better = better + 1
        else:
            worse = worse + 1
    outputFile.write(problemType + ", " + str(better) + ", " + str(worse) + ", " + str(worse))


def findLine(lines, name, start, problemType):
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
        if problemType != "j30" and i == 3:
            break
        if a[i] != "":
            if a[i].__contains__("\n"):
                n = a[i].split("\n")
                if n[0] != '':
                    numbers.append(float(n[0]))
            else:
                numbers.append(int(a[i]))
    return numbers
