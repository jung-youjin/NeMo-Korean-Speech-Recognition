import pickle
import os
from xml.etree.ElementTree import parse, Element, dump, ElementTree

folder_path = "/content/korean-speech-recognition-quartznet/datasets/meta/aihub/"

with open("test.txt", 'wb') as f:
    for dirname, _, filenames in os.walk(folder_path):
        # print(dirname) #/content/korean-speech-recognition-quartznet/datasets/meta/aihub/KsponSpeech_0027
        # print(filenames) #[KsponSpeech_023872.txt, KsponSpeech_023873.txt, ]
        subdirname = dirname.replace(folder_path, "")
        for filename in sorted(filenames):
            # print(filename) # KsponSpeech_023872.txt
            if filename.endswith(".txt"):
                try:
                    with open(subdirname+"/"+filename, 'rb') as txtfile:
                        data = txtfile.readlines() 
                        # print(data) # [b'\xbc\xd2\xbc\xb3 \xc0\xd0\xbe\xfa\xb4\xc2\xb5\xa5? b/\r\n']
                        char2idx = dict()
                        char2idx = {char:idx for idx, char in enumerate(data)}
                        idx2char = list()
                        idx2char = {idx:char for idx, char in enumerate(data)}
                        print(char2idx)
                        pickle.dump(data, f)
                        txtfile.close()
                except:
                    print(filename+': no such file')
    f.close()

with open("test.txt", 'rb') as f:
    data = pickle.load(f)
    print(data)
    f.close()