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

def bracket_filter(sentence):
    new_sentence = str()
    flag = False
    
    for ch in sentence:
        if ch == '(' and flag == False: 
            flag = True
            continue
        if ch == '(' and flag == True:
            flag = False
            continue
        if ch != ')' and flag == False:
            new_sentence += ch
    return new_sentence

import re

def special_filter(sentence):
    SENTENCE_MARK = ['?', '!']
    NOISE = ['o', 'n', 'u', 'b', 'l']
    EXCEPT = ['/', '+', '*', '-', '@', '$', '^', '&', '[', ']', '=', ':', ';', '.', ',']
    
    new_sentence = str()
    for idx, ch in enumerate(sentence):
        if ch not in SENTENCE_MARK:
            # o/, n/ 등 처리
            if idx + 1 < len(sentence) and ch in NOISE and sentence[idx+1] == '/': 
                continue 

        if ch == '#': 
            new_sentence += '샾'

        elif ch not in EXCEPT: 
            new_sentence += ch

    pattern = re.compile(r'\s\s+')
    new_sentence = re.sub(pattern, ' ', new_sentence.strip())
    return new_sentence

def sentence_filter(raw_sentence):
    return special_filter(bracket_filter(raw_sentence))

import pandas as pd

filepath = "/content/nemo-korean-speech-recognition/kspon_character_labels.csv"

def load_label(filepath):
    char2id = dict()
    id2char = dict()
    ch_labels = pd.read_csv(filepath)
    id_list = ch_labels["id"]
    char_list = ch_labels["char"]
    freq_list = ch_labels["freq"]
    
    for (id, char, freq) in zip(id_list, char_list, freq_list):
        char2id[char] = id
        id2char[id] = char

    # print(char2id)
    # print(id2char)
    return char2id, id2char

import pandas as pd

filepath = "/content/nemo-korean-speech-recognition/kspon_character_labels.csv"

char2id = dict()
id2char = dict()

def load_label(filepath):

    ch_labels = pd.read_csv(filepath)
    id_list = ch_labels["id"]
    char_list = ch_labels["char"]
    freq_list = ch_labels["freq"]
    
    for (id, char, freq) in zip(id_list, char_list, freq_list):
        char2id[char] = id
        id2char[id] = char

    # print(char2id)
    # print(id2char)
    return char2id, id2char

load_label(filepath)

def sentence_to_target(sentence, char2id):
    target = ""
    for ch in sentence:
        try:
            target += (str(char2id[ch]) + ' ')
            # print(char2id[ch])
        except:
            target += (str(0) + ' ')  

    return target[:-1]

    import pandas as pd

filepath = "/content/nemo-korean-speech-recognition/kspon_character_labels.csv"

char2id = dict()
id2char = dict()

def load_label(filepath):

    ch_labels = pd.read_csv(filepath)
    id_list = ch_labels["id"]
    char_list = ch_labels["char"]
    freq_list = ch_labels["freq"]
    
    for (id, char, freq) in zip(id_list, char_list, freq_list):
        char2id[char] = id
        id2char[id] = char

    # print(char2id)
    # print(id2char)
    return char2id, id2char

load_label(filepath)

def target_to_sentence(target, id2char):
    sentence = ""
    targets = target.split()

    for n in targets:
        sentence += id2char[int(n)]
    return sentence