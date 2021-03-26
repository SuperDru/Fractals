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

    def fractal_dimension_minkowski(self):
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

    def fractal_dimension_blanket(self):
        cell_size = int(min(self.width, self.height) / 100)
        deltas = [1, 2]
        a_deltas = [0, 0]

        for x in range(int(self.width / cell_size)):
            for y in range(int(self.height / cell_size)):
                img = self.img.crop((x, y, x + cell_size, y + cell_size))
                pixels = img.load()

                u = np.zeros((3, cell_size + 1, cell_size + 1))
                b = np.zeros((3, cell_size + 1, cell_size + 1))

                vol = np.zeros(3)

                for delta in deltas:
                    for i in range(cell_size):
                        for j in range(cell_size):
                            u[0][i][j] = pixels[i, j]
                            b[0][i][j] = pixels[i, j]

                            u_prev = u[delta - 1]
                            u[delta][i][j] = max(u_prev[i][j] + 1, max(u_prev[i + 1][j + 1],
                                                                       u_prev[i - 1][j + 1],
                                                                       u_prev[i + 1][j - 1],
                                                                       u_prev[i - 1][j - 1]))
                            b_prev = b[delta - 1]
                            b[delta][i][j] = min(b_prev[i][j] - 1, min(b_prev[i + 1][j + 1],
                                                                       b_prev[i - 1][j + 1],
                                                                       b_prev[i + 1][j - 1],
                                                                       b_prev[i - 1][j - 1]))

                            vol[delta] += u[delta][i][j] - b[delta][i][j]
                    a_deltas[delta - 1] += (vol[delta] - vol[delta - 1]) / 2

        res = stats.linregress(np.log2(a_deltas), np.log2(deltas))
        return 2 - -res.slope
