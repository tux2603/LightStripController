#!/usr/bin/env python

import glob
import threading

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from PIL import Image

image_path = 'images/1white.png'
running = True


class ClickableImage(Image):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # global image_path
            # image_path = self.source
            print(self.source)


class ImageGrid(GridLayout):
    def __init__(self, cols=3, images=[], **kwargs):
        super(ImageGrid, self).__init__(**kwargs)
        self.cols = cols
        self.images = images

        for img in self.images:
            thumb = ClickableImage(source=img)
            self.add_widget(thumb)


class ImagePages(PageLayout):
    def __init__(self, cols=3, rows=2, directory='images', **kwargs):
        super(ImagePages, self).__init__(**kwargs)
        self.cols = cols
        self.rows = rows
        self.image_directory = directory
        self.images = glob.glob(f'{self.image_directory}/*.png')

        for i in range(0, len(images), rows * cols):
            pass


class ImageSelectorApp(App):
    def __init__(self, directory='images', *args, **kwargs):
        super(ImageSelectorApp, self).__init__(*args, **kwargs)
        self.image_directory = directory

    def build(self):
        print("Building grid")
        return ImageGrid(cols=3, images=glob.glob(f'{self.image_directory}/*.png'))


def render_image():
    current_image_path = None
    while running:
        # Load image if new image selected
        if image_path != current_image_path:
            current_image_path = image_path
            image = Image.open(current_image_path).resize(450, 450)
            # TODO make resecale intelligent and not distort on y axis

        # Render image
        for row in image:
            for pixel in row:
                print(pixel)


if __name__ == '__main__':
    app = ImageSelectorApp()
    Window.fullscreen = True
    thread = threading.Thread(target=render_image)
    app.run()
    running = False
