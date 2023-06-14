from os import path as osp

from basicsr.utils import scandir
from basicsr.utils.lmdb_util import make_lmdb_from_imgs


def create_lmdb():
    """Create lmdb files for dataset.

    Usage:
        Before run this script, please run `extract_subimages.py`.
        Typically, there are four folders to be processed for DIV2K dataset.
            HQ-50K_train_HR_sub
            HQ-50K_train_LR_bicubic/X2_sub
            HQ-50K_train_LR_bicubic/X3_sub
            HQ-50K_train_LR_bicubic/X4_sub
        Remember to modify opt configurations according to your settings.
    """
    # # HR images
    folder_path = 'HQ-50K/train/GTmod12/GTmod12_sub_768'
    lmdb_path = 'HQ-50K/train/LMDB/HQ-50K_GTmod12_sub_768.lmdb'
    img_path_list, keys = prepare_keys(folder_path)
    make_lmdb_from_imgs(folder_path, lmdb_path, img_path_list, keys)

    # LRx2 images
    folder_path = 'HQ-50K/train/LRX2/LRx2_sub_384'
    lmdb_path = 'HQ-50K/train/LMDB/HQ-50K_LRx2_sub_384.lmdb'
    img_path_list, keys = prepare_keys(folder_path)
    make_lmdb_from_imgs(folder_path, lmdb_path, img_path_list, keys)

    # LRx3 images
    folder_path = 'HQ-50K/train/LRX3/LRx3_sub_256'
    lmdb_path = 'HQ-50K/train/LMDB/HQ-50K_LRx3_sub_256.lmdb'
    img_path_list, keys = prepare_keys(folder_path)
    make_lmdb_from_imgs(folder_path, lmdb_path, img_path_list, keys)

    # LRx4 images
    folder_path = 'HQ-50K/train/LRX4/LRx4_sub_192'
    lmdb_path = 'HQ-50K/train/LMDB/HQ-50K_LRx4_sub_192.lmdb'
    img_path_list, keys = prepare_keys(folder_path)
    make_lmdb_from_imgs(folder_path, lmdb_path, img_path_list, keys)


def prepare_keys(folder_path):
    """Prepare image path list and keys for DIV2K dataset.

    Args:
        folder_path (str): Folder path.

    Returns:
        list[str]: Image path list.
        list[str]: Key list.
    """
    print('Reading image path list ...')
    img_path_list = sorted(list(scandir(folder_path, suffix='png', recursive=False)))
    keys = [img_path.split('.png')[0] for img_path in sorted(img_path_list)]

    return img_path_list, keys


if __name__ == '__main__':
    create_lmdb()

