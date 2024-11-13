# A script that makes a bunch of files with a specified format and contents
# Made by mineland
# Use it at your own accord. If anything happens do tell me

import os
import sys
import shutil
import argparse
import regex
from colorama import Fore, Back, Style

def error(message):
    print(Fore.RED + str(message) + Style.RESET_ALL)
def warn(message):
    print(Fore.YELLOW + str(message) + Style.RESET_ALL)
def cPrint(color, message):
    print(color + message + Style.RESET_ALL)
def varPrint(message, variable):
    print(Fore.LIGHTWHITE_EX + message + " " + Style.RESET_ALL + str(variable))
def success(message):
    print(Back.LIGHTGREEN_EX + Fore.BLACK + str(message) + Style.RESET_ALL)

def filePrint(fileName, fileContents):
    i = 0
    print(Fore.BLACK + Back.LIGHTWHITE_EX + "   " + fileName + "   " + Style.RESET_ALL)
    
    if type(fileContents) == list:
        fileContents = "\n".join(fileContents)

    name = os.path.basename(fileName)
    for line in fileContents.splitlines():
        print(Fore.BLACK + Back.LIGHTWHITE_EX + str(i).rjust(3) + "" + Style.RESET_ALL + " " + line.replace(name, Fore.LIGHTGREEN_EX + name + Style.RESET_ALL))
        i += 1
    print(Fore.BLACK + Back.LIGHTWHITE_EX + "   [END OF FILE]   " + Style.RESET_ALL)

def createFile(fileName, fileContents):

    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))

    with open(fileName, 'w') as f:
        f.write(fileContents)
        f.close()


# Bulk create file
# 
# Will create a new file or append lines to an existing file with the inner text replaced
# ------------
# Examples: 
# (inputs: "oak_door spruce_door")
# 
# > singleLine.txt
#    /give @p xxx
# 
# => commands.txt
#     /give @p oak_door
#     /give @p spruce_door
# 
# ------------
# > multipleCommands.txt
#    /give @p xxx
#    /give @p xxx[block_state={"display": "ui"}]
# 
# => multipleCommands.txt
#     /give @p oak_door
#     /give @p oak_door[block_state={"display": "ui"}]
#     /give @p spruce_door
#     /give @p spruce_door[block_state={"display": "ui"}]
# 
def bulkCreateFile(inputFile, outputFile, textToReplace, nameArray) -> list:
    if not args.silent:
        varPrint("Input file:", inputFile)
        varPrint("Output file:", outputFile)
        varPrint("Template text to replace:", textToReplace)
        varPrint("Names to use:", nameArray)
    else:
        varPrint("Input file: ", inputFile)
        varPrint("Output file: ", outputFile)
        varPrint("Template text to replace: ", textToReplace)
        varPrint("Names to use: ", nameArray)

    print("Starting...")
    print("-"*10)
    outputContent = ""

    with open(inputFile, 'r') as f:
        inputContent = f.readlines()
        
        # replace the inner text in the file
        if args.verbose:
            # varPrint(">", Fore.LIGHTCYAN_EX + inputFile)
            filePrint(inputFile, inputContent)
            print("-"*10)
        f.close()


    i = 0
    for name in nameArray:
        for line in inputContent:
            outputContent += line.replace(textToReplace, name)
            if outputContent[-1] != "\n":
                outputContent += "\n"
            i += 1

            if (not args.silent):
                print(Fore.LIGHTWHITE_EX + str(i).rjust(3) + "" + Style.RESET_ALL + " " + line.replace(textToReplace, Fore.LIGHTGREEN_EX + name + Style.RESET_ALL))

    createFile(os.path.join(".", outputFile), outputContent)
    return [0, "Created file with " + str(i) + " lines"]

def bulkCreateFolderStructure(inputNameStructure, inputFileStructure, outputFolder, textToReplace, nameArray) -> list:
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)


    fileCount = 0
    # walk through every file and folder in the structure
    for root, dirs, files in os.walk(inputFileStructure):
        for file in files:
            inputFiles.append(os.path.join(root.replace(inputFileStructure, ""), file))


    if not args.silent:
        varPrint("Total input files:", len(inputFiles))
        varPrint("Input names from:", inputNameStructure)
        varPrint("Base input files from:", inputFileStructure)
        varPrint("Output folder:", outputFolder)

    else:
        varPrint("Total input files: ", len(inputFiles))


    print("Starting...")
    print("-"*10)
    for inputFile in inputFiles:
        if (not args.silent):
            varPrint(">", Fore.LIGHTCYAN_EX + inputFile)

        for name in nameArray:
            if args.verbose and not args.silent:
                varPrint("  >", Fore.LIGHTYELLOW_EX + name)
            
            outputFileName = str(inputFile).replace(textToReplace, name)

            with open(inputFileStructure + inputFile, 'r') as f:
                fileContents = f.read()
                replacedContents = fileContents.replace(textToReplace, name)



                if args.show_output_contents and not args.silent:

                    # cPrint((Back.LIGHTWHITE_EX + Fore.CYAN), "Contents: ")
                    i = 0
                    for line in replacedContents.splitlines():
                        
                        print(Fore.BLACK + Back.WHITE + str(i).rjust(3) + "" + Style.RESET_ALL + " " + line.replace(name, Fore.LIGHTGREEN_EX + name + Style.RESET_ALL))
                        i += 1
                    
                    exitVar = input("Press enter to continue, q to quit: ")
                    if exitVar == "q":
                        return [2, "Quitting..."]
                
                createFile(outputFolder + outputFileName, replacedContents)
                fileCount += 1

    ret = [0, "Created " + str(fileCount) + " files to " + outputFolder]
    return ret



# -----------------------------------------------------------------------
# Main


parser = argparse.ArgumentParser(
    description="Repetition goes bye bye", 
    epilog=""
)

inputNameStructure = "./names/"
inputFileStructure = "./input/"
outputFolder = "./output/"
nameArray = []
inputFiles = []
textToReplace = ""

inputFileStructure = None
outputFile = None

operation = ""

parser.add_argument("-n", "--names-file", help="file/folder with the names to use. Use a new line for each name in the file, or use a folder with a file for each name (will ignore extension)", default="")
parser.add_argument("-l", "--list", help="List of names to use. String with spaces for each new name. Will override -n", default="")
parser.add_argument("-p", "--prompt", help="Prompt string to be replaced. Default: xxx", default="xxx")
parser.add_argument("-i", "--input", help="Input folder / (TODO) file structure json. Default: input", default="input")
parser.add_argument("-o", "--output", help="Output folder / file. Default: output", default="input")

parser.add_argument("--show-output-contents", help="Show the output file as it is processed. Will prompt an input to continue", action="store_true")

parser.add_argument("-v", "--verbose", help="Verbose mode. Will print each input and output file processed", action="store_true")
parser.add_argument("-s", "--silent", help="Silent mode. Will give minimal info about the process", action="store_true")
args = parser.parse_args()


if args.names_file != "":
    if os.path.isdir(args.names_file):
        for file in os.listdir(args.names_file):
            # use regex to get rid of the last .xxx extension in case the files have . for whatever reason
            nameArray.append(regex.sub(r"\.[a-zA-Z0-9]*$", "", file))
    else:
        # read from file    
        with open(args.names_file, "r") as f:
            for line in f:
                if line.strip() == "":
                    continue
                nameArray.append(line.strip())

if args.prompt != "":
    textToReplace = args.prompt


# add a help message if -help is used



# read from folder inputNameStructure
# Instead of making a text file with all the names, just put the textures inside the ./names/ folder
# oak_door.png, spruce_door.png, etc. -> nameArray = ["oak_door", "spruce_door" ...]

if args.list != "":
    nameArray = args.list.split(" ")


if args.input != "":
    inputFileStructure = args.input

if os.path.isdir(inputFileStructure):
    if inputFileStructure[-1] != "/":
        inputFileStructure += "/"
    
    for file in os.listdir(inputNameStructure):
        fileName = file.split(".")[0]
        nameArray.append(fileName)
    operation = "structure"


elif os.path.isfile(inputFileStructure):
    inputFile = inputFileStructure
    # cPrint(Fore.LIGHTMAGENTA_EX, "Using input file: " + inputFile)
    if args.output != parser.get_default("output"):
        outputFile = args.output
    else:
        sameFile = input("Write to same file? (y/n): ")
        if sameFile == "y":
            outputFile = inputFileStructure
        else:
            outputFile = input("Output file: ")
    operation = "file"
        

    
else:
    warn("Uh oh")
    error("Input does not exist: " + inputFileStructure)
    # exit(1)


if nameArray == []:
    error("No names found in " + inputNameStructure)
    exit(1)

if textToReplace == "":
    textToReplace = input("Template text to replace: ")

res = [-1, "Default value"]
match operation:
    case "file":
        cPrint(color=Fore.LIGHTMAGENTA_EX, message= "FILE OPERATION")
        res = bulkCreateFile(inputFile, outputFile, textToReplace, nameArray)
    case "structure":
        cPrint(color=Fore.LIGHTCYAN_EX, message= "STRUCTURE OPERATION")
        res = bulkCreateFolderStructure(inputNameStructure, inputFileStructure, outputFolder, textToReplace, nameArray)


match res[0]:
    case 0:
        cPrint(color=Back.LIGHTGREEN_EX, message="  Done!  ")
        if res[1] != "":
            cPrint(color=Fore.LIGHTGREEN_EX, message=res[1])
            exit(0)
    case 1:
        cPrint(color=Back.LIGHTRED_EX, message="  Uh oh  ")
        if res[1] != "":
            cPrint(color=Fore.LIGHTRED_EX, message=res[1])
            exit(1)
    case 2:
        cPrint(color=Back.LIGHTYELLOW_EX, message="  Warning!  ")
        if res[1] != "":
            cPrint(color=Fore.LIGHTYELLOW_EX, message=res[1])
            exit(2)
    case -1:
        cPrint(color=Back.LIGHTRED_EX, message="  Something went wrong  ")
        if res[1] != "":
            cPrint(color=Fore.LIGHTRED_EX, message=res[1])
            exit(1)



