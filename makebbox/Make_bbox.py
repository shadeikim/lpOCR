import cv2
import os
import time
import argparse
import matplotlib.pyplot as plt
import random

def run():
    input_path, output_path = opt.input_path, opt.output_path

    start = time.time()

    os.makedirs(f'{output_path}', exist_ok=True)

    imglist = os.listdir(input_path)
    label_list = []
    final_label =[]
    remove_index = []
    korean = ['가', '나', '다', '라', '마', '거', '너', '더', '러', '머','버', '서', '어', '저', '고', '노', '도', '로', '모', '보', '소', '오', '조', '구', '누', '두', '루', '무', '부', '수', '우', '주', '바', '사', '아', '자', '하', '허', '호', '배']
    class_num = 0
    for img in imglist:
        if img[-4:] == '.png':
            label_list.clear()
            final_label.clear()
            img_name = img.split('.')[0]
            image = cv2.imread(f'{input_path}/{img}')
            dst = cv2.resize(image, (520, 110), cv2.INTER_AREA)
            dst_height, dst_width  = dst.shape[:2]
            gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

            _, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            #cv2.imwrite(f'{output_path}/{img_name}_binary.png' ,th)
            #contour_num = 0
            contours, hier = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if x > dst_width/13*1 and x < dst_width/13*12 and w >15 and h > 15:
                    label_list.append([x,y,w,h])

            label_list.sort()

            #1. 큰 bbox에 포함된 작은 bbox 제거
            for i in range(len(label_list)):
                if i > 0 and label_list[i-1][0] + label_list[i-1][2] > label_list[i][0] + label_list[i][2]:
                    print('removed!')
                else:
                    final_label.append(label_list[i])
            #2. 한글 bbox 합치기
            #모음
            if len(final_label) == len(img_name):
                final_label[-5][1] = final_label[0][1]
                final_label[-5][3] = final_label[0][3]
            #자음
            elif len(final_label) == len(img_name) + 1 :
                final_label[-6][2] = final_label[-5][0] + final_label[-5][2] - final_label[-6][0]
                final_label[-6][1] = final_label[-5][1]
                final_label[-6][3] = final_label[-5][3]
                del final_label[-5]
            else:
                final_label = []
            #final_label = label_list
            print(final_label)
            #for label in final_label:
                #cv2.rectangle(dst, (label[0], label[1]), (label[0]+label[2], label[1]+label[3]), (random.randint(0, 255), random.randint(0,255), random.randint(0,255)),3)
            #cv2.imwrite(f'{output_path}/{img_name}_contours.png', dst)
            f= open(f"{output_path}/{img_name}.txt", 'w')

            if len(final_label) == len(img_name):
                for i in range(len(final_label)):
                    if i == len(img_name)-5:
                        class_num = korean.index(img_name[-5]) + 10
                    else:
                        class_num = img_name[i]

                    data = f"{class_num} {(2*final_label[i][0] + final_label[i][2])/520/2} {(2*final_label[i][1] + final_label[i][3])/110/2} {final_label[i][2]/520} {final_label[i][3]/110}\n"
                    f.write(data)
            f.close()




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='./', help='input path')
    parser.add_argument('--output_path', type=str, default='labels', help='output path')
    opt = parser.parse_args()

    run()
