# Made by mineland
# Use it at your own accord. If anything happens do tell me

import zipfile
import os
import datetime
import argparse
import regex
import json
from colorama import Fore, Back, Style
from utils import cPrint, error, warn
# Script to package resource pack into a zip file, then send it to the resourcepack folder specified
# name is the current directory

# check for launch arguments
parser = argparse.ArgumentParser(
    description="Packing pack thingy i made lol \n -mineland", 
    epilog=""
)
parser.add_argument("-f", "--file", help="Name of the output file (Dont add the extension, it will be zip. Default: pack)", default="!!pack")

parser.add_argument("-p", "--path", help="Path to pack", default="!!.")
parser.add_argument("-d", "--dir", help="Destination folder (Default: current dir. Can be set to !copy to move the dir into the copy destination. Will ignore date if thats the case)", default="!!.")
parser.add_argument("-cp", "--copy", help="Directory to copy to. For faster testing purposes", default="!!")
parser.add_argument("-ncp", "--no-copy", help="Forces no copy if set on the config file", action="store_true")
parser.add_argument("--date", help="Append date time to name", action="store_true")
parser.add_argument("--no-date", help="Removes date if set on the config file", action="store_true")
parser.add_argument("-s", "--silent", help="Silent mode", action="store_true")
parser.add_argument("-c", "--config", help="Config file to check. Uses ./config.cfg if not set, Will ignore the default if other arguments are present", default="!!config.cfg")

args = parser.parse_args()
new_args = argparse.Namespace()


# exit()

print("----------------------")

# check if there are any arguments from console set
useConfig = True
for arg in vars(args):
    if args.__getattribute__(arg) != parser.get_default(arg):
        useConfig = False
    
        # print(str(arg) + ": args = " + str(args.__getattribute__(arg)) + " || cfg = " + str(parser.get_default(arg)))
        

if (args.config != parser.get_default("config")) or useConfig:
    try:
        configFile = str(args.config).strip("!!")
        
            
        # print(configFile)
        
        f = open(configFile)

        cPrint(Fore.LIGHTWHITE_EX, "Using config file: " + Fore.WHITE +  configFile)


        
        for line in f:
            currentLine = line.split("=")
            if line.startswith("#") or not line.__contains__("="):
                # print("skipping line")
                continue

            # print("###")
            var =   currentLine[0].strip()
            value = currentLine[1].strip()

            # check if the arg is set in the command line already. If so, ignore config file
            if args.__getattribute__(var) != parser.get_default(var):
                # print("Argument . Ignoring cfg...")
                # print(str(var) + ": args = " + str(args.__getattribute__(var)) + " || cfg = " + str(value))
                continue
            new_args.__setattr__(var, value)
            

    except IOError as e:
        # error("uh oh")
        # error(e)
        if args.config != "!!config.cfg":
            warn("Could not open config file: " + args.config)
            warn("Using default values")
        
# for each argument
# print(args)
for arg in vars(args):
    # print(arg)
    if new_args.__contains__(arg):
        # print("contains arg")
        currentArg = new_args.__getattribute__(arg)
        if currentArg is str:
            # print("stripping")
            new_args.__setattr__(arg, currentArg.strip("!!"))
        else:
            # print("not stripping")
            new_args.__setattr__(arg, currentArg)
    else:
        # print("not contains arg")
        currentArg = args.__getattribute__(arg)
        if type(currentArg) is str:
            # print("stripping")
            new_args.__setattr__(arg, currentArg.strip("!!"))
        else:
            # print("not stripping")
            new_args.__setattr__(arg, currentArg)
    
og_args = args
args = new_args
# exit()
packPath = args.path
if not os.path.exists(packPath):
    error("------------------")
    error("Error: " + packPath + " does not exist")
    exit(1)

# exit(0)

name = args.file if (args.file != "") else "pack"


if (args.date and not args.no_date):
    date = datetime.date.today().__format__("%Y-%m-%d")
    time = datetime.datetime.now().__format__("%H.%M.%S")
    zip_name = name + " " + date + "@" + time + ".zip"
else:
    zip_name = name + ".zip"


# current directory where the script is
# rootFolder = (os.path.dirname(os.path.abspath(__file__)))


dirPath = args.dir
fullZip = dirPath + "/" + zip_name




if args.dir == "!copy": 
    zip_name = name + ".zip"
    cPrint(Fore.LIGHTBLUE_EX,"Using copy destination as destination")
    if args.copy != "":
        fullZip = args.copy + "/" + name + ".zip"
        args.copy = ""

    else:
        cPrint(Fore.LIGHTYELLOW_EX, "No destination specified. Will create in current dir")
        fullZip = "./" + name + ".zip"

pathIgnore = [".vscode/"]
extIgnore = [".xcf", ".py", ".gif", ".bak", ".zip"]
extWhitelist = [".png", ".json", ".mcmeta", ".vsh", ".fsh", ".mcfunction", ".ttf"]

cPrint(Fore.LIGHTCYAN_EX, "> Pack path:   "   + Fore.WHITE + packPath)
cPrint(Fore.LIGHTCYAN_EX, "> File name:   "   + Fore.WHITE + zip_name)
cPrint(Fore.LIGHTCYAN_EX, "> Path to zip: " + Fore.WHITE + fullZip)

# exit()
print ("Starting...")


# check if pack.mcmeta is a valid json file
try:
    print ("------------------")
    # print("Opening " + packPath + "/pack.mcmeta")
    f = open(packPath + "/pack.mcmeta")
    # check if pack.mcmeta is a valid json file
    try:
        mcmeta = json.load(f)
    except ValueError as e:
        error("Error: pack.mcmeta is not a valid json file")
        exit(1)



    pack = mcmeta["pack"]

    for thingy in ["pack_format", "description"]:
        if pack.get(thingy) == None:
            error("Error: pack.mcmeta lacks [" + thingy + "] to be displayed in game")
            exit(1)

    f.close()

    cPrint(Fore.LIGHTCYAN_EX, zip_name)
    for thing in pack:
        cPrint(Fore.LIGHTWHITE_EX, "> " + thing + ": " + Fore.WHITE + str(pack[thing]))
except IOError as e:
    # check if its a file not found error
    if e.errno == 2:
        error("Error: pack.mcmeta not found")
        exit(1)
    error("Error: " + str(e))
    exit(1)

if (args.silent):
    cPrint(Fore.LIGHTBLUE_EX, "Processing files...")
else:
    cPrint(Fore.LIGHTBLUE_EX, "Processing files:")

    
with zipfile.ZipFile(fullZip, 'w', zipfile.ZIP_DEFLATED) as zip:
    for root, dirs, files in os.walk(packPath):
        for file in files:
            filepath = os.path.join(root, file)
            if not(args.silent):
                cPrint(Fore.LIGHTWHITE_EX,"  [file] " + filepath)
            # print(filepath)
            if any(ignore in filepath for ignore in pathIgnore):
                continue
            if any(ignore in file for ignore in extIgnore):
                continue
            if not any(ignore in file for ignore in extWhitelist):
                continue
            zip.write(filepath, os.path.relpath(filepath, packPath))

cPrint (Fore.LIGHTGREEN_EX, "Zip packaging done")

if args.copy != "" and not args.no_copy:
    destination = args.copy
    if args.copy.endswith("/"):
        destination = args.copy + name + ".zip"
    cPrint(Fore.LIGHTBLUE_EX, "Copying to " + destination)
    try:
        # copy file to destination folder (fix any os specific issues with spaces and stuff)
        if os.name == "nt":
            fullZip = fullZip.replace(" ", "\\ ")
            destination = destination.replace(" ", "\\ ")
            command = "xcopy /s /y " + fullZip + " " + destination
        else:
            destination = destination.replace(" ", "\\ ")
            fullZip = fullZip.replace(" ", "\\ ")
            command = "cp -r " + fullZip + " " + destination

        os.system(command)    
        cPrint(Fore.LIGHTCYAN_EX, "Copied to " + destination)
    except Exception as e:
        error("------------------")
        error("Uh oh")
        error(e)
        exit(1)


print("----------------------")
cPrint(Fore.LIGHTGREEN_EX, "Pack packed!")
exit(0)




