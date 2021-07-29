# preprocess reference from sooftware/kospeech wiki

import math

BASE_PATH = "/content/korean-speech-recognition-quartznet/datasets/meta/aihub/"
FNAME = 'KsponSpeech_'
filenum = 59001
format = '.txt'

def filenum_padding(filenum):
    if filenum < 10: 
        return '00000' + str(filenum)
    elif filenum < 100: 
        return '0000' + str(filenum)
    elif filenum < 1000: 
        return '000' + str(filenum)
    elif filenum < 10000: 
        return '00' + str(filenum)
    elif filenum < 100000: 
        return '0' + str(filenum)
    else: 
        return str(filenum)

def get_dirnum(filenum):
    dirnum = math.floor((int(filenum)-1)/1000) +1
    return dirnum

def dirnum_padding(filenum): # get dirname (padding붙어있는 dirnum)
    dirname = get_dirnum(filenum)
    if dirname < 10: 
        return '000' + str(dirname)
    elif dirname < 100: 
        return '00' + str(dirname)
    elif dirname < 1000: 
        return '0' + str(dirname)
    else: 
        return str(dirname)

def get_path(path, fname, filenum, format):
    return path + fname + dirnum_padding(filenum) + "/" + fname + filenum + format

print(get_path(BASE_PATH,FNAME,filenum_padding(filenum),".txt"))
