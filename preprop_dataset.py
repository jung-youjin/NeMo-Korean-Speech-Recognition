#!/usr/bin/env python
"""Read WAV files and compute spectrograms and save them in the same folder."""
__author__ = 'Erdene-Ochir Tuguldur'

import argparse
from tqdm import *
import numpy as np

from torch.utils.data import ConcatDataset
from datasets import Compose, LoadAudio, ComputeMagSpectrogram

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--dataset",
                    choices=['librispeech', 'mbspeech', 'bolorspeech', 'kazakh20h', 'backgroundsounds', 'aihub'],
                    default='bolorspeech', help='dataset name')
parser.add_argument("--path", type=str, default=None)
args = parser.parse_args()

if args.dataset == 'mbspeech':
    from datasets.mb_speech import MBSpeech
    dataset = MBSpeech()
elif args.dataset == 'librispeech':
    from datasets.libri_speech import LibriSpeech
    dataset = ConcatDataset([
        LibriSpeech(name='train-clean-100'),
        LibriSpeech(name='train-clean-360'),
        LibriSpeech(name='train-other-500'),
        LibriSpeech(name='dev-clean',)
    ])
elif args.dataset == 'backgroundsounds':
    from datasets.background_sounds import BackgroundSounds
    dataset = BackgroundSounds(is_random=False)
elif args.dataset == 'bolorspeech':
    from datasets.bolor_speech import BolorSpeech
    dataset = ConcatDataset([
        BolorSpeech(name='train'),
        BolorSpeech(name='train2'),
        BolorSpeech(name='test'),
        BolorSpeech(name='demo'),
        BolorSpeech(name='annotation'),
        BolorSpeech(name='annotation-1111')
    ])
elif args.dataset == 'kazakh20h':
    from datasets.kazakh20h_speech import Kazakh20hSpeech
    dataset = ConcatDataset([
        Kazakh20hSpeech(name='test'),
        Kazakh20hSpeech(name='train')
    ])
elif args.dataset == 'aihub':
    from datasets.aihub_speech import AihubSpeech
    dataset = ConcatDataset([
        AihubSpeech(name='test'),
        AihubSpeech(name='train')
    ])
elif args.dataset == 'uaihub':
    from datasets.uaihub_speech import AihubSpeech
    dataset = ConcatDataset([
        AihubSpeech(name='test'),
        AihubSpeech(name='train')
    ])
else:
    print("unknown dataset!")
    import sys
    sys.exit(1)


transform=Compose([LoadAudio(), ComputeMagSpectrogram()])
for data in tqdm(dataset):
    fname = data['fname']
    data = transform(data)
    mel_spectrogram = data['input']
    np.save(fname.replace('.pcm', '.pcm.npy'), mel_spectrogram)
