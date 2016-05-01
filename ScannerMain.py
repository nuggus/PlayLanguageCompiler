import sys
from Tokenizing import *

sourceFile = 'sqrt.tl'
fileExtension = ".tl"
tokenList = []


def scannerMethod():
    if sourceFile.endswith(fileExtension, 3):
        try:
            f = open(sourceFile, 'r')
            for line in f:
                flag = 0
                tokenList = line.split()
                for index in range(len(tokenList)):
                    tokenFlag = identifyingKeyWords(tokenList[index])
                    if tokenFlag == "%":
                        break
                    elif tokenFlag == 'invalid':
                        flag = 1
                        break
                if flag == 1:
                    break
            else:
                f.close()
        except:
            print(
                    sourceFile + ' not found, makesure ' + sourceFile + ' is in the same folder where this python file is placed!')
    else:
        print("Entered Source File name is not valid in TL 15.0, Please enter a valid file with extension .tl")
    # creating output file name based on input file name
    outputFile = sourceFile[:-3] + ".tok"
    # opening outfile in write mode
    tokensFile = open(outputFile, 'w')
    # to print the tokens into filename.tok
    for index in tokens:
        # print (index[0], ', '.join(map(str, index[1:])))
        for _string in index:
            tokensFile.write(str(_string))
        tokensFile.write('\n')
    else:
        tokensFile.close()
    mytokens = parserTokens
    return mytokens

    # tList=scannerMethod();
