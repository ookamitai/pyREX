import os.path
import subprocess
import configparser
import sys
import soundfile as sf
import re
import audio

def checkUUID():
    white_list = ["C5D83F47-5D7C-5DC1-A95D-4DD2D956DF20","E40E34CF-F222-4795-8CCA-C931559516EC","384DD2CC-1FDA-11B2-A85C-9E22EBBF8340"]
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15].upper()
    if uuid in white_list:
        return 1
    else:
        return 0

def readconfig():
    config_dict = {}
    #flags = {}
    config = configparser.ConfigParser()
    config.read("C:\\ProgramData\\pyREX\\rexconfig.txt")
    config.sections()
    for key in config['resamplers']:
        config_dict.update({key:config['resamplers'][key]})
    #for key2 in config['flags']:
    #    flags.update({key2:config['flags'][key2]})
    return config_dict

def check_int(string):
    return re.match(r"[-+]?\d+(\.0*)?$", string) is not None

def processFlags(rawflag):
    number = []
    letter = []
    switchflag = ("G","R")
    specialflag = ["G", "R", "B", "I", "D", "T", "L", "S"]
    switchflags = ''.join(switchflag)
    dictflag={}
    flag = re.findall('(\d+|[A-Za-z]+)', rawflag)
    for item in flag:
        #print(type(item))
        if check_int(item):
            number.append(float(item))
        else:
            if item.startswith(switchflag):
                dictflag.update({item[0]: 1.0})
            for w in switchflags:
                item = item.replace(w,"")
            letter.append(item)
    dictflag.update(dict(zip(letter,number)))
    for key in list(dictflag):
        if not key in specialflag:
            dictflag.pop(key,None)
    return dictflag

def main():
    args = sys.argv[1:]
    outpath = args[1]
    flag = args[4]
    flage = processFlags(flag)
    configkey = readconfig()
    print("Reading configuration...")
    print(configkey, "done")
    resampler = configkey.get(list(configkey)[0])
    for item1 in configkey:
        if item1 in flag:
            resampler = configkey.get(item1)

    command = resampler + ' "' + args[0] + '" "' + args[1] + '" ' + ' '.join(args[2:])
    print("Flag is", flag)
    print("Command to be excuted:", command)
    print("Output path:", outpath)
    print("Calling resampler...")
    subprocess.call(command, shell=False)
    print("Adding effect...")
    x, sr = sf.read(outpath)
    y = x
    if "R" in flage:
        y = ''.join(x)[::-1]
    elif "I" in flage:
        y = audio.apply_fadein(x, sr, flage.get("I"))
    elif "D" in flage:
        y = audio.apply_fadeout(x, sr, flage.get("D"))
    elif "L" in flage:
        y = audio.normalize(x)
    sf.write(outpath, y, sr)
    print("Done")

if __name__ == "__main__":
    if checkUUID():
        if os.path.exists("C:\\ProgramData\\pyREX\\rexconfig.txt"):
            if len(sys.argv) == 1:
                print("pyREX only works as a back-end for utau.")
                input()
            else:
                main()
        else:
            print("Missing file...")
            input()
    else:
        print("pyREX is not designed to run on your system.")
        input()


