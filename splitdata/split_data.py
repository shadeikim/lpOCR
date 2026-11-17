import os
import random
import shutil
import argparse

from tqdm import tqdm

def split_dataset(src_dir, dst_dir, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2):
    ratio_sum = train_ratio + val_ratio + test_ratio
    if abs(ratio_sum - 1.0) > 1e-6:
        raise ValueError(f'비율의 합이 1이 되어야 합니다. 현재 합: {ratio_sum}')

    #이미지 파일 목록 수집
    files = [f for f in os.listdir(src_dir)]

    if len(files) == 0:
        raise ValueError(f'{src_dir} 에서 이미지 파일을 찾지 못했습니다.')

    random.shuffle(files)

    total = len(files)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    splits = {
        'train' : files[:train_end],
        'val' : files[train_end:val_end],
        'test' : files[val_end:]
    }

    for split_name in splits:
        os.makedirs(os.path.join(dst_dir, split_name), exist_ok=True)
    # 파일 복사/이동
    op = shutil.copy2

    for split_name , file_list in splits.items():
        for fname in tqdm(file_list, desc=f'{split_name} ({len(file_list)}개)'):
            src_path = os.path.join(src_dir, fname)
            dst_path = os.path.join(dst_dir, split_name, fname)
            op(src_path, dst_path)

    print(f'\n총 {total}개 파일 분할 완료')
    print(f"train: {len(splits['train'])}개")
    print(f"val: {len(splits['val'])}개")
    print(f"test : {len(splits['test'])}개")

    return splits

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src' ,type=str, required=True, help='원본 이미지가 있는 폴더')
    parser.add_argument('--dst' ,type=str, default='dataset', help='train/val/test 폴더를 생성할 경로')
    parser.add_argument('--train-ratio', type=float, default=0.6)
    parser.add_argument('--val-ratio', type=float, default=0.2)
    parser.add_argument('--test-ratio', type=float, default=0.2)

    opt= parser.parse_args()

    split_dataset(src_dir=opt.src, dst_dir=opt.dst, train_ratio=opt.train_ratio, val_ratio=opt.val_ratio, test_ratio=opt.test_ratio)
