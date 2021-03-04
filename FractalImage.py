from PIL import Image
import numpy as np
from scipy import stats
import math


class FractalImage:
    def __init__(self, img_path):
        self.img = Image.open(img_path)
        self.width = self.img.size[0]
        self.height = self.img.size[1]

    def show(self):
        self.img.show()

    def save(self, path):
        self.img.save(path)

    def nullify_channels(self, channels):
        source = self.img.split()
        for channel in channels:
            source[channel].paste(source[channel].point(lambda i: 0))
        self.img = Image.merge(self.img.mode, source)

    def to_grayscale(self):
        self.img = self.img.convert('L')

    def fractal_dimension(self):
        sizes = [i + 1 for i in range(30)]
        pixels = self.img.load()
        counts = []
        log_sizes = []
        for size in sizes:
            h_count = int(self.height / size)
            w_count = int(self.width / size)
            filled_boxes = np.zeros((w_count + (1 if self.width > w_count * size else 0),
                                     h_count + (1 if self.height > h_count * size else 0)), dtype=bool)
            for i in range(self.width):
                for j in range(self.height):
                    if pixels[i, j] < 127:
                        x_box = int(i / size)
                        y_box = int(j / size)
                        filled_boxes[x_box][y_box] = True

            counts.append(math.log(filled_boxes.flatten().sum()))
            log_sizes.append(math.log(1 / size))
        res = stats.linregress(log_sizes, counts)
        return res.slope

