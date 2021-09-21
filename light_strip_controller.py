#!/usr/bin/env python

import glob
import threading
import time
import serial

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as UIImage
from kivy.uix.pagelayout import PageLayout
from PIL import Image


image_path = 'images/purpleTwinkles.png'
running = True


class ClickableImage(UIImage):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            global image_path
            image_path = self.source
            print(self.source)


class ImageGrid(GridLayout):
    def __init__(self, cols=3, images=[], **kwargs):
        super(ImageGrid, self).__init__(**kwargs)
        self.cols = cols
        self.images = images

        for img in self.images:
            thumb = ClickableImage(source=img, allow_stretch=True, keep_ratio=False)
            self.add_widget(thumb)


class ImagePages(PageLayout):
    def __init__(self, cols=3, rows=3, directory='images', **kwargs):
        super(ImagePages, self).__init__(**kwargs)
        self.cols = cols
        self.rows = rows
        self.image_directory = directory
        self.images = glob.glob(f'{self.image_directory}/*.png')

        for i in range(0, len(self.images), rows * cols):
            page_images = self.images[i:i + self.rows * self.cols]
            grid = ImageGrid(cols=self.cols, images=page_images)
            self.add_widget(grid)


class ImageSelectorApp(App):
    def __init__(self, directory='images', *args, **kwargs):
        super(ImageSelectorApp, self).__init__(*args, **kwargs)
        self.image_directory = directory

    def build(self):
        print("Building grid")
        return ImagePages(cols=3, rows=3, directory=self.image_directory, border=200, swipe_threshold=0.2)


def connect_to_arduino():
    ser = None
    for i in range(100):
        try:
            ser = serial.Serial('/dev/ttyACM' + str(i), 9600)
            print('Connected to ttyACM' + str(i))
            time.sleep(2)
            return ser
        except Exception:
            pass
    print('Connection failed')
    return None


def render_image():
    ser = connect_to_arduino()
    if ser is None:
        raise Exception('FUCKFUCKFUCK')

    current_image_path = None
    image = None

    current_image_path = image_path
    image = Image.open(current_image_path)
    image = image.resize((450, image.height))

    while running:
        # Render image
        if image is not None:
            for y in range(image.height):
                # Load image if new image selected
                if image_path != current_image_path:
                    current_image_path = image_path
                    image = Image.open(current_image_path)
                    image = image.resize((450, image.height))
                    print(f'NEW STUFF! {current_image_path}')
                    break

                for x in range(image.width):
                    pixel_color = image.getpixel((x, y))
                    pixel_data = bytes([x % 255, x // 255, pixel_color[0], pixel_color[1], pixel_color[2]])
                    ser.write(pixel_data)

    ser.close()


if __name__ == '__main__':
    app = ImageSelectorApp()
    Window.maximize()
    thread = threading.Thread(target=render_image)
    thread.start()
    app.run()
    running = False
