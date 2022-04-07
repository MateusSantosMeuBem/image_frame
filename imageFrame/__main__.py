import argparse
from cgitb import text
import cv2 as cv
import numpy as np
import os

extensions = ['gif', 'jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff', 'eps', 'raw']
def isImage(img: str):
    global extensions
    return True if img.split('.')[-1] in extensions else False

parse = argparse.ArgumentParser(description='Create a white frame around image.', usage='python .\imageFrame\ -fp "c:\Users\Mateus\Pictures" -fr 0.1 -pm 5',)

parse.add_argument('-fr', '--frame_range', help = 'Especify the range for the frame. Use -fr 0.2. Default -fr 0.5.',type = float, action = 'store', default = 0.2)

parse.add_argument('-fp', '--folder_path', help = 'Folder with all the images to be modified.',type = str, action = 'store', default = None)

parse.add_argument('-pm', '--polaroid_mode', help = 'If make images as polaroids. If not, set this as 1, if so, any integer positive. Default: 1.',type = int, action = 'store', default = 1)

args = parse.parse_args().__dict__
folder_path: str = args['folder_path']
range: int = args['frame_range']
polaroid_length: int = args['polaroid_mode']

if not os.path.isdir(folder_path):
    exit('You informed an invalid folder path.')

if polaroid_length < 1:
    exit('You informed an invalid value for polaroid')

files: str = os.listdir(folder_path)
not_images: list = []
for file_name in files:
    if(isImage(file_name)):
        img_path: str = f'{folder_path}/{file_name}'
        img = cv.imread(img_path)

        height, width, _ = img.shape
        width_gap , height_gap = int(width * (range) / 2), int(height * (range) / 2)
        gap: int = width_gap if width_gap < height_gap or width_gap == height_gap else height_gap

        canva = np.ones(
                    (
                        int(height + gap * 2 * polaroid_length),
                        int(width + gap * 2),
                        3),
                    np.uint8
                )*255

        new_img = canva.copy()

        print(f'Buiding <{file_name}>...')
        new_img[gap : gap + height, gap : gap + width] = img

        output_folder: str = f'{folder_path}/framed_images'
        if(not os.path.isdir(output_folder)):
            os.mkdir(output_folder)

        cv.imwrite(f'{output_folder}/f_{file_name}', new_img)
    else:
        not_images.append(file_name)

if len(not_images) > 0:
    message: str = 'Not framed files:\n'
    for file in not_images:
        message += f' - <{file}>\n'
    message += '\n These files are not in the formats accept:\n'
    message += ', '.join(extensions)
    with open(f'{output_folder}/report.txt', 'w') as file:
        file.write(message)