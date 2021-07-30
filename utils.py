"""Utility methods."""
__author__ = 'Erdene-Ochir Tuguldur'

import os
import sys
import glob
import torch
import math
import requests
from tqdm import tqdm


def get_last_checkpoint_file_name(logdir):
    """Returns the last checkpoint file name in the given log dir path."""
    checkpoints = glob.glob(os.path.join(logdir, '*.pth'))
    checkpoints.sort()
    if len(checkpoints) == 0:
        return None
    return checkpoints[-1]


def load_checkpoint(checkpoint_file_name, model, optimizer, use_gpu=False, remove_module_keys=True):
    """Loads the checkpoint into the given model and optimizer."""
    checkpoint = torch.load(checkpoint_file_name, map_location='cpu' if not use_gpu else None)
    state_dict = checkpoint['state_dict']
    
    # print(checkpoint)
    # print(state_dict.keys())
    # print(model)
    # model_load = model(checkpoint['epoch'], checkpoint['global_step'], checkpoint['state_dict'], checkpoint['optimizer'])
    model_load = torch.load(checkpoint_file_name)

    if remove_module_keys:
        new_state_dict = {}
        for k, v in state_dict.items():
            if k.startswith('module.'):
                new_state_dict[k[len('module.'):]] = v
            else:
                new_state_dict[k] = v
        state_dict = new_state_dict
    # print(state_dict)
    # print(state_dict.keys())
    model.load_state_dict(model_load, strict=False)
    # model.load_state_dict(state_dict, strict=False)
    # model.float()
    # print(model)
    if optimizer is not None:
        optimizer.load_state_dict(checkpoint['optimizer'], strict=False)
    start_epoch = checkpoint.get('epoch', 0)
    global_step = checkpoint.get('global_step', 0)
    # optimizer_ = checkpoint.get('optimizer', 0)
    # print(optimizer_)
    del checkpoint
    print("loaded checkpoint epoch=%d step=%d" % (start_epoch, global_step))
    return start_epoch, global_step
    # return model_load

def save_checkpoint(logdir, epoch, global_step, model, optimizer):
    """Saves the training state into the given log dir path."""
    checkpoint_file_name = os.path.join(logdir, 'epoch-%04d.pth' % epoch)
    print("saving the checkpoint file '%s'..." % checkpoint_file_name)
    checkpoint = {
        'epoch': epoch + 1,
        'global_step': global_step,
        'state_dict': model.state_dict(),
        'optimizer': optimizer.state_dict(),
    }
    torch.save(checkpoint, checkpoint_file_name)
    drive_path = F"/suresoft/backup/weight/210730/".join('epoch-%04d.pth' % epoch)
    torch.save(checkpoint, drive_path)
    del checkpoint


def download_file(url, file_path):
    """Downloads a file from the given URL."""
    print("downloading %s..." % url)
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024 * 1024
    wrote = 0
    with open(file_path, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size // block_size), unit='MB'):
            wrote = wrote + len(data)
            f.write(data)

    if total_size != 0 and wrote != total_size:
        print("downloading failed")
        sys.exit(1)
