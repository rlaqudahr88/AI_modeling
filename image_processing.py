import os
import random
import glob
import cv2
import numpy as np

from PIL import Image, ImageOps
from pathlib import Path


class image_processing:

    '''This image pre-processing will focus on
        * convertion of transparent images to mask images
        * putting original images to masked images
        * adding background to transparent image
        * resizing images
        '''

    ''' For Salient Object Detection(SOD) background removal project following
        pre-processes are taken in order to train U2Net model:
        1. collect transparent images with google_crawling.py
        2. convert transparent images to mask images -> def trans_to_gt()
        3. add background to transparent images
        4. we can also expand our training data by fliping images horizontally
        Now you have images to train a model
        5. After training the U2Net model, we need to test the prediction of mask images
        once we have gained mask output we need to convert them to transparent images

        '''

    def __init__(self):
        # directories of images
        # img : original image
        # trans : foreground image with transparent background
        # gt : mask images (black and white)
        # gt and trans images are .png files
        # img files are .jpg
        self.img_path = os.path.join(
            os.getcwd(), 'train_data', '03-12_train_data', 'images', 'trained_online-shop_img'+os.sep)
        self.img_trans = os.path.join(
            os.getcwd(), 'train_data', '03-09', '가구_trans'+os.sep)
        self.img_gt = os.path.join(
            os.getcwd(), 'train_data', '03-12_train_data', 'images', 'trained_online-shop_mask'+os.sep)
        self.background = os.path.join(
            os.getcwd(), 'trial', 'background' + os.sep)
        self.img_combined = os.path.join(
            os.getcwd(), 'trial', 'img_combined' + os.sep)
        self.pred_mask = os.path.join(
            os.getcwd(), 'trial', 'output', 'mask'+os.sep)
        self.pred_trans = os.path.join(
            os.getcwd(), 'trial', 'output', 'trans'+os.sep)

    def directory_check(self):
        if not os.path.exists(self.img_path):
            print(self.img_path+'path created!')
            os.makedirs(self.img_path, exist_ok=True)
        if not os.path.exists(self.img_trans):
            print(self.img_trans+'path created!')
            os.makedirs(self.img_trans, exist_ok=True)
        if not os.path.exists(self.img_gt):
            print(self.img_gt+'path created!')
            os.makedirs(self.img_gt, exist_ok=True)
        if not os.path.exists(self.background):
            print(self.background+'path created!')
            os.makedirs(self.background, exist_ok=True)
        if not os.path.exists(self.img_combined):
            print(self.img_combined+'path created! \n')
            print('creating path..')
            os.makedirs(self.img_combined, exist_ok=True)
            print('img_combined path created')
        if not os.path.exists(self.pred_mask):
            print(self.pred_mask+'path created! \n')
            print('creating path..')
            os.makedirs(self.pred_mask, exist_ok=True)
            print('img_combined path created')
        if not os.path.exists(self.pred_trans):
            print(self.pred_trans+'path created! \n')
            print('creating path..')
            os.makedirs(self.pred_trans, exist_ok=True)
            print('img_combined path created')
        else:
            print('directory all chcked!!')

    def resize_img(self):
        dir_folder = '/home/nick/Documents/Nick/github_models/salient_object_detection/U-2-Net/train_data/03-12_train_data/images/train_img_trans/'
        img_folder = []
        for folder in os.listdir(dir_folder):
            img_folder.append(folder)
        for folder in img_folder:
            for filename in os.listdir(dir_folder+folder):
                image = Image.open(os.path.join(
                    dir_folder, folder, filename)).convert('RGBA')
                image = image.resize((480, 480))
                image.save(dir_folder+folder+'/'+filename)
                print('saving resized trans imgs: ' + folder+filename)

    def trans_to_gt(self):
        # convert transparent images to mask images
        # convertion varies with alpha transparency level from 0-255
        # all images are resized to width 480, height 480

        # dir_folder = '/home/nick/Documents/Nick/github_models/salient_object_detection/U-2-Net/train_data/03-12_train_data/images/train_img_trans/'
        # img_folder = []
        # for folder in os.listdir(dir_folder):
        #     img_folder.append(folder)
        dir_folder_mask = '/home/nick/Documents/Nick/github_models/salient_object_detection/U-2-Net/train_data/03-12_train_data/images/online-shop_img_trans/'
        for filename in os.listdir(dir_folder_mask):
            # for filename in os.listdir(self.img_trans):

            image = Image.open(os.path.join(
                dir_folder_mask, filename)).convert('RGBA')
            #image = image.resize((480, 480))
            pixelMap = image.load()
            newImg = Image.new(image.mode, image.size)
            pixelsNew = newImg.load()
            width, height = newImg.size
            for i in range(width):
                for j in range(height):
                    pixelsNew[i, j] = pixelMap[i, j]
                    if pixelMap[i, j][3] < 120:  # 128 is transparent glasses
                        # (255,255,255,255) white color
                        pixelsNew[i, j] = (0, 0, 0, 255)
                    elif pixelMap[i, j][0] < 254:  # 255
                        pixelsNew[i, j] = (255, 255, 255, 255)  # white
                    elif pixelMap[i, j][1] < 254:
                        pixelsNew[i, j] = (255, 255, 255, 255)
                    elif pixelMap[i, j][2] < 254:
                        pixelsNew[i, j] = (255, 255, 255, 255)
                    elif pixelMap[i, j][0] < 80:
                        pixelsNew[i, j] = (0, 0, 0, 255)
                    elif pixelMap[i, j][1] < 80:
                        pixelsNew[i, j] = (0, 0, 0, 255)
                    elif pixelMap[i, j][2] < 80:
                        pixelsNew[i, j] = (0, 0, 0, 255)

            newImg.save(dir_folder_mask+filename.split('-')[0]+'.png')
            print('converting transparent images to mask images' + filename)

    def trans_to_gt_recorrect(self):
        dir_folder = '/home/nick/Documents/Nick/github_models/salient_object_detection/U-2-Net/train_data/03-12_train_data/images/train_img_trans/'
        folder = 'fashion'
        dir_folder_mask = '/home/nick/Documents/Nick/github_models/salient_object_detection/U-2-Net/train_data/03-12_train_data/images/train_img_mask/'
        img = 'morefashionresized15.png'
        if img in os.listdir(dir_folder+folder):
            # for filename in os.listdir(self.img_trans):
            image = Image.open(os.path.join(
                dir_folder, folder, img)).convert('RGBA')
            image = image.resize((480, 480))
            pixelMap = image.load()
            newImg = Image.new(image.mode, image.size)
            pixelsNew = newImg.load()
            width, height = newImg.size
            for i in range(width):
                for j in range(height):
                    pixelsNew[i, j] = pixelMap[i, j]
                    if pixelMap[i, j][3] < 220:  # 128 is transparent glasses
                        # (255,255,255,255) white color
                        pixelsNew[i, j] = (0, 0, 0, 255)
                    elif pixelMap[i, j][0] < 254:  # 255
                        pixelsNew[i, j] = (255, 255, 255, 255)  # white
                    elif pixelMap[i, j][1] < 254:
                        pixelsNew[i, j] = (255, 255, 255, 255)
                    elif pixelMap[i, j][2] < 254:
                        pixelsNew[i, j] = (255, 255, 255, 255)
                    elif pixelMap[i, j][0] < 80:
                        pixelsNew[i, j] = (0, 0, 0, 255)
                    elif pixelMap[i, j][1] < 80:
                        pixelsNew[i, j] = (0, 0, 0, 255)
                    elif pixelMap[i, j][2] < 80:
                        pixelsNew[i, j] = (0, 0, 0, 255)

            newImg.save(dir_folder_mask+folder+'/'+img)
            print('converting transparent images to mask images' +
                  folder + img)

    def add_background(self):
        for filename in os.listdir(self.img_trans):

            foreground = Image.open(self.img_trans + filename).convert('RGBA')
            foreground = foreground.resize((480, 480))
            # get random background from the background folder
            ran = random.choice(os.listdir(self.background))
            back = Image.open(self.background+ran).convert('RGB')
            # layer2 = layer2.resize((960,960))
            back = back.resize((480, 480))
            back.paste(foreground, (0, 0), foreground)
            # layer2.show()
            back.save(self.img_combined + filename.split('.')[0]+'.jpg')
            print('saved: ' + filename.split('.')[0]+'.jpg')

    def put_custom_background(self):
        for filename in os.listdir(self.img_trans):

            foreground = Image.open(self.img_trans + filename).convert('RGBA')
            foreground = foreground.resize((480, 480))
            # we can also use plain RGB custom background
            # first set the same size
            img_size = foreground.size
            # create a background by giving R G B (0-255) values 0:black, 255:White
            whiteimg = Image.new(
                'RGB', (img_size[0], img_size[1]), (255, 255, 255))
            whiteimg.paste(foreground, (0, 0), foreground)
            whiteimg.save(self.img_combined+filename.split('.')[0]+'.jpg')
            print('saving'+filename)

    def flip_images(self):
        for filename in os.listdir(self.img_gt):
            newmask = Image.open(self.img_gt+filename)
            im_mirror = ImageOps.mirror(newmask)
            im_mirror.save(self.img_gt+filename.split('.')[0]+'flip.png')
            print('flipped mask image saved..' + filename)

        for filename in os.listdir(self.img_path):
            newImg = Image.open(self.img_path + filename)
            im_mirror2 = ImageOps.mirror(newImg)
            im_mirror2.save(self.img_path +
                            filename.split('.')[0]+'flip.jpg')

            print('flipped image saved..' + filename)
        print('done')

    def flip_images_multi_folders(self, train_img_tr):
        main_dir = '/home/nick/Documents/Nick/github_models/salient_object_detection/U-2-Net/train_data/03-12_train_data/images'
        # train_img_tr = 'train_img_trans'
        # train_img_mk = 'train_img_mask'
        # train_mall_img = 'trained_online-shop_img'
        # train_mall_mask = 'trained_online-shop_mask'
        for folder in os.listdir(os.path.join(main_dir, train_img_tr+os.sep)):
            print(folder)
            for filename in os.listdir(os.path.join(main_dir, train_img_tr, folder+os.sep)):
                newimg = Image.open(os.path.join(
                    main_dir, train_img_tr, folder+os.sep)+filename)
                im_mirror = ImageOps.mirror(newimg)
                im_mirror.save(os.path.join(main_dir, train_img_tr,
                                            folder+os.sep)+filename.split('.')[0]+'flip.png')
                print(f'flipped img file: {filename} in {folder}')

    def mask_to_trans(self):
        for filename in os.listdir(self.pred_mask):
            img = Image.open(os.path.join(
                self.pred_mask, filename.split('.')[0]+'.jpg')).convert('RGB')
            mask = Image.open(os.path.join(self.pred_mask, filename)
                              ).convert('L')  # gray scale
            img.putalpha(mask)
            img.save(self.pred_trans+filename)
            print("saving transparent image.." + filename)

    def dilation_erosion(self):
        # opencv provides denoising opening and closing method

        save_to = os.path.join(
            os.getcwd, 'trial', 'output', 'closoing_gt'+os.sep)
        if not os.path.exists(save-to):
            os.makedirs(save_to, exist_ok=True)

        for filename in os.listdir(self.pred_mask):
            img = cv2.imread(self.pred_mask+filename, 0)
            closing = cv2.morphologyEx(
                img, cv2.MORPH_CLOSE, np.ones((10, 10), np.uint8))
            closing = Image.fromarray(closing)
            closing.save(save_to+filename)
            print('saving closing noise.. ' + filename)

    def check_difference(self):

        # check if there are non matching image names between the two data
        imgname = []
        maskname = []

        for filename in os.listdir(self.img_combined):
            imgname.append(filename.split('.')[0])
        for filename in os.listdir(self.img_gt):
            maskname.append(filename.split('.')[0])
        x = set(imgname)
        y = set(maskname)
        # make a set of only non-matching strings
        z = x.symmetric_difference(y)
        print(z)
        print(x == y)

    def combine_3_images(self):
        # combine 3 images to one image as a series
        # image_dir : original test images
        image_dir = '/home/nick/Documents/Nick/backgroundremoval/test_data/images/test/'
        img2_dir = '/home/nick/Documents/Nick/backgroundremoval/test_data/images/test_combined/'
        img3_dir = '/home/nick/Documents/Nick/backgroundremoval/test_data/images/test-trans/'
        save_3img = os.path.join(os.getcwd(), 'trial',
                                 'test_3_combined' + os.sep)
        if not os.path.exists(save_3img):
            os.makedirs(save_3img, exist_ok=True)
        for filename in os.listdir(image_dir):
            org_img = Image.open(os.path.join(image_dir, filename))

            output_combined = Image.open(os.path.join(img2_dir, filename))
            out_trans = Image.open(os.path.join(
                img3_dir, filename.split('.')[0]+'.png')).convert('RGBA')
            # resize, first image
            org_img = org_img.resize((600, 800))
            out_trans = out_trans.resize((600, 800))
            org_img_size = org_img.size
            output_combined_size = output_combined.size
            out_trans_size = out_trans.size
            new_image = Image.new(
                'RGBA', (3*org_img_size[0], org_img_size[1]), (250, 250, 250))
            new_image.paste(org_img, (0, 0))
            new_image.paste(output_combined, (2*org_img_size[0], 0))
            new_image.paste(out_trans, (org_img_size[0], 0))
            new_image.save(save_3img + filename.split('.')[0]+'.png')
            print('combining 3 images: '+filename.split('.')[0]+'.png')

    def random_crop_background(self):
        dir_folder = '/home/nick/Documents/Nick/github_models/salient_object_detection/U-2-Net/train_data/03-17_train_data/background/'
        #in_file = '01.jpg'
        out_file = 'out.png'
        # generate random background
        ran = random.choice(os.listdir(dir_folder))
        img = Image.open(dir_folder+ran)
        width, height = img.size
        print(f"width:{width}")
        print(f"height:{height}")
        x = 0
        y = 0
        if width > 480 and height > 480:
            x = random.randrange(0, (width-480), 1)
            y = random.randrange(0, (height-480), 1)
            print('largest')
        if width > 480 and height == 480:
            x = random.randrange(0, (width-480), 1)
            y = 0
            print('long width / same height')
        if width > 480 and height < 480:
            img = img.resize((width, 480))
            x = random.randrange(0, (width-480), 1)
            y = 0
            print('long horizontal / enlarged height')
        if width == 480 and height > 480:
            x = 0
            y = random.randrange(0, (height-480), 1)
            print('same width / long height')
        if width == 480 and height < 480:
            img = img.resize((480, 480))
            x = 0
            y = 0
            print('same width / enlarged height')
        if width == 480 and height == 480:
            x = 0
            y = 0
            print('480x480')
        if width < 480 and height > 480:
            img = img.resize((480, height))
            x = 0
            y = random.randrange(0, (height-480), 1)
            print('enlarged width / long height')
        if width < 480 and height == 480:
            img = img.resize((480, 480))
            x = 0
            y = 0
            print('enlarged width / same height')
        if width < 480 and height < 480:
            img = img.resize((480, 480))
            x = 0
            y = 0
            print('enlarged width / enlarged height')

        print(f"position x:{x}")
        print(f"position y:{y}")

        cropped_background = img.crop((x, y, 480+x, 480+y))
        # cropped_background.save(dir_folder+out_file)
        return cropped_background

    def add_random_background(self):
        main_dir = '/home/nick/Documents/Nick/github_models/salient_object_detection/U-2-Net/train_data/03-17_train_data/'
        trans_dir = 'train_img_trans/'
        img_dir = 'train_img_generated/'

        for folder in os.listdir(main_dir+trans_dir):
            if not os.path.exists(main_dir+img_dir+folder+os.sep):
                os.makedirs(main_dir+img_dir+folder+os.sep)
            for filename in os.listdir(main_dir+trans_dir+folder+os.sep):

                foreground = Image.open(
                    main_dir+trans_dir+folder+os.sep + filename).convert('RGBA')
                foreground = foreground.resize((480, 480))
                # get random background from the background folder
                back = self.random_crop_background().convert('RGB')
                # layer2 = layer2.resize((960,960))
                #back = back.resize((480, 480))
                back.paste(foreground, (0, 0), foreground)
                # layer2.show()

                back.save(main_dir+img_dir + folder + os.sep +
                          filename.split('.')[0]+'.jpg')
                print('saved: ' + filename.split('.')[0]+'.jpg')

    def get_img_list(self):
        PATH = '/home/nick/Documents/Nick/github_models/salient_object_detection/F3Net-master/data/Aircode_all_images/image/'

        name = []

        for filename in os.listdir(PATH):
            name.append(filename.split('.')[0])

        # saving list of filenames as a .txt file
        with open("test.txt", 'w') as output:
            for row in name:
                output.write(str(row) + '\n')


if __name__ == "__main__":

    run = image_processing()
    # obtain training data

    run.directory_check()
    # run.flip_images()
    # run.flip_images_multi_folders('train_img_mask')
    # run.trans_to_gt()
    run.random_crop_background()
    run.add_random_background()
    # run.add_background()
    # run.put_custom_background()
    # run.flip_images()

    # get transparent image from predicted mask and input image
    # mask_to_trans()

    # run.check_difference()
    # run.combine_3_images()
