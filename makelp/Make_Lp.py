import os
import random
import time
import argparse

from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont

# 한글 classification
korean = '가나다라마' \
         '거너더러머버서어저' \
         '고노도로모보소오조' \
         '구누두루무부수우주'

korean_taxi = '바사아자'
korean_rent = '하허호'
korean_parce1 = '배'

#배경 이미지
new_img_path = './plate_image/number_plate_new.jpg'
old_img_path = './plate_image/number_plate_old.jpg'

#User default path through environment variables
#user_profile = os.environ['USERPROFILE']

#한글 폰트
ko_font = ImageFont.truetype(f'./font/한길체.ttf', 1500, encoding='unic')

#숫자 폰트
font = ImageFont.truetype(f'./font/NotoSansKR-Medium.ttf',1700 , encoding='unic')

def run():
    count, save_path = opt.count, opt.save_path

    start = time.time()

    # Make folder to saving outputs
    os.makedirs(f'{save_path}/new8', exist_ok=True)
    os.makedirs(f'{save_path}/old8', exist_ok=True)
    os.makedirs(f'{save_path}/old7', exist_ok=True)

    # 8 digit license plate with holographic
    for i in tqdm(range(count), desc='8-digit license plate(holographic)'):
        front = f'{random.randint(100, 999)}'
        middle = random.choice(korean)
        back = f'{random.randint(1000, 9999)}'
        full_name = front + middle + back

        image_pil = Image.open(new_img_path)
        draw = ImageDraw.Draw(image_pil)
        # draw.text( (x,y), License plate string, Font color, Font)
        draw.text((65*20, -250), front, 'black', font)
        draw.text((215*20, 450), middle, 'black', ko_font)
        draw.text((300*20, -250), back, 'black', font)

        image_pil.save(f'{save_path}/new8/' + full_name + '.png', 'PNG')

    # 8 digit license plate
    for i in tqdm(range(count), desc='8-digit license plate'):
        front = f'{random.randint(100, 999)}'
        middle = random.choice(korean)
        back = f'{random.randint(1000, 9999)}'
        full_name = front + middle + back

        image_pil = Image.open(old_img_path)
        draw = ImageDraw.Draw(image_pil)
        draw.text((40*20, -200), front, 'black', font)
        draw.text((210*20, 450), middle, 'black', ko_font)
        draw.text((300*20, -200), back, 'black', font)

        image_pil.save(f'{save_path}/old8/' + full_name + '.png', 'PNG')

    # 7 digit license plate
    for i in tqdm(range(count), desc = '7-digit license plate'):
        front = f'{random.randint(10, 99)}'
        middle = random.choice(korean)
        back = f'{random.randint(1000, 9999)}'
        full_name = front + middle + back

        image_pil = Image.open(old_img_path)
        draw = ImageDraw.Draw(image_pil)
        draw.text((65*20, -200), front, 'black', font)
        draw.text((188*20, 450), middle, 'black', ko_font)
        draw.text((285*20, -200), back, 'black', font)

        image_pil.save(f'{save_path}/old7/' + full_name + '.png', 'PNG')

    print(f'Done. {round(time.time() - start, 3)}s')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=1, help='Number of image to save')
    parser.add_argument('--save-path', type=str, default='./../result', help='Outpup path')
    opt = parser.parse_args()

    run()

