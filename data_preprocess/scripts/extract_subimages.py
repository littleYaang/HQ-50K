import cv2
import numpy as np
import os
import sys
from multiprocessing import Pool
from os import path as osp
from tqdm import tqdm
import math
from basicsr.utils import scandir


def main():
    """A multi-thread tool to crop large images to sub-images for faster IO.

    opt (dict): Configuration dict. It contains:
        n_thread (int): Thread number.
        compression_level (int):  CV_IMWRITE_PNG_COMPRESSION from 0 to 9.
            A higher value means a smaller size and longer compression time.
            Use 0 for faster CPU decompression. Default: 3, same in cv2.

        input_folder (str): Path to the input folder.
        save_folder (str): Path to save folder.
        crop_size (int): Crop size.
        step (int): Step for overlapped sliding window.
        thresh_size (int): Threshold size. Patches whose size is lower
            than thresh_size will be dropped.

    Usage:
        For each folder, run this script.
        Typically, there are four folders to be processed for HQ-50K dataset.
            HQ-50K_train_HR
            HQ-50K_train_LR_bicubic/X2
            HQ-50K_train_LR_bicubic/X3
            HQ-50K_train_LR_bicubic/X4
        After process, each sub_folder should have the same number of
        subimages.
        Remember to modify opt configurations according to your settings.
    """

    opt = {}
    opt['n_thread'] = 20
    opt['compression_level'] = 0

    # # HR images
    opt['input_folder'] = 'HQ-50K/train/GTmod12'
    opt['save_folder'] = 'HQ-50K/train/GTmod12/GTmod12_sub_768'
    opt['crop_size'] = 768
    opt['step'] = 576
    opt['thresh_size'] = 0
    # opt['start'] = 540
    extract_subimages(opt)

    # # LRx2 images
    opt['input_folder'] = 'HQ-50K/train/LRX2'
    opt['save_folder'] = 'HQ-50K/train/LRX2/LRx2_sub_384'
    opt['crop_size'] = 384
    opt['step'] = 288
    # opt['start'] = 270
    opt['thresh_size'] = 0
    extract_subimages(opt)

    # LRx3 images
    opt['input_folder'] = 'HQ-50K/train/LRX3'
    opt['save_folder'] = 'HQ-50K/train/LRX3/LRx3_sub_256'
    opt['crop_size'] = 256
    opt['step'] = 192
    # opt['start'] = 180
    opt['thresh_size'] = 0
    extract_subimages(opt)

    # # LRx4 images
    opt['input_folder'] = 'HQ-50K/train/LRX4'
    opt['save_folder'] = 'HQ-50K/train/LRX4/LRx4_sub_192'
    opt['crop_size'] = 192
    opt['step'] = 144
    # opt['start'] = 135
    opt['thresh_size'] = 0
    extract_subimages(opt)


def extract_subimages(opt):
    """Crop images to subimages.

    Args:
        opt (dict): Configuration dict. It contains:
            input_folder (str): Path to the input folder.
            save_folder (str): Path to save folder.
            n_thread (int): Thread number.
    """
    input_folder = opt['input_folder']
    save_folder = opt['save_folder']
    if not osp.exists(save_folder):
        os.makedirs(save_folder)
        print(f'mkdir {save_folder} ...')
    else:
        print(f'Folder {save_folder} already exists. Exit.')
        sys.exit(1)

    img_list = list(scandir(input_folder, full_path=True))

    pbar = tqdm(total=len(img_list), unit='image', desc='Extract')
    pool = Pool(opt['n_thread'])
    for path in img_list:
        pool.apply_async(worker, args=(path, opt), callback=lambda arg: pbar.update(1))
    pool.close()
    pool.join()
    pbar.close()
    print('All processes done.')


def worker(path, opt):
    """Worker for each process.

    Args:
        path (str): Image path.
        opt (dict): Configuration dict. It contains:
            crop_size (int): Crop size.
            step (int): Step for overlapped sliding window.
            thresh_size (int): Threshold size. Patches whose size is lower
                than thresh_size will be dropped.
            save_folder (str): Path to save folder.
            compression_level (int): for cv2.IMWRITE_PNG_COMPRESSION.

    Returns:
        process_info (str): Process information displayed in progress bar.
    """
    crop_size = opt['crop_size']
    step = opt['step']
    thresh_size = opt['thresh_size']
    img_name, extension = osp.splitext(osp.basename(path))

    # remove the x2, x3, x4 and x8 in the filename for data
    img_name = img_name.replace('x2', '').replace('x3', '').replace('x4', '').replace('x8', '')

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    h, w = img.shape[0:2]
    start = opt['start']
    h_space = np.arange(0, h - crop_size + 1, step)
    if h - (h_space[-1] + crop_size) > thresh_size:
        h_space = np.append(h_space, h - crop_size)
    w_space = np.arange(0, w - crop_size + 1, step)
    if w - (w_space[-1] + crop_size) > thresh_size:
        w_space = np.append(w_space, w - crop_size)
    # h_space = np.arange(start,start+1)
    # print('h_space',h_space)
    # w_space = np.arange(start,start+1)
    # print('w_space',w_space)
    index = 0
    for x in h_space:
        for y in w_space:
            index += 1
            cropped_img = img[x:x + crop_size, y:y + crop_size, ...]
            cropped_img = np.ascontiguousarray(cropped_img)
            cv2.imwrite(
                osp.join(opt['save_folder'], f'{img_name}_s{index:03d}{extension}'), cropped_img,
                [cv2.IMWRITE_PNG_COMPRESSION, opt['compression_level']])
    process_info = f'Processing {img_name} ...'
    return process_info


if __name__ == '__main__':
    main()
