from PIL import Image
from PIL import ImageDraw
import numpy as np


class FractalImage:
    def __init__(self, img_path):
        self.path = img_path
        self.img = Image.open(img_path)
        self.width = self.img.size[0]
        self.height = self.img.size[1]

    def show(self):
        self.img.show()

    def save(self, path):
        self.img.save(path)

    def to_grayscale(self):
        self.img = self.img.convert('L')

    def segment(self):
        self.to_grayscale()
        cell_size = int(min(self.width, self.height) / 20)
        deltas = [1, 2]
        w = int(self.width / cell_size) + 1
        h = int(self.height / cell_size) + 1
        a = np.zeros((w, h))

        for x in range(w):
            for y in range(h):
                img = self.img.crop((x * cell_size, y * cell_size, x * cell_size + cell_size, y * cell_size + cell_size))
                pixels = img.load()

                u = np.zeros((3, cell_size + 1, cell_size + 1))
                b = np.zeros((3, cell_size + 1, cell_size + 1))

                vol = np.zeros(3)
                a_deltas = [0, 0]

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
                a[x][y] = a_deltas[1]

        threshold = np.mean(a)
        print(threshold)

        for x in range(w):
            for y in range(h):
                if a[x][y] > threshold:
                    ImageDraw.Draw(self.img).rectangle(
                        (x * cell_size, y * cell_size, x * cell_size + cell_size, y * cell_size + cell_size),
                        fill=255, outline=255)
                else:
                    ImageDraw.Draw(self.img).rectangle(
                        (x * cell_size, y * cell_size, x * cell_size + cell_size, y * cell_size + cell_size),
                        fill=0, outline=0)

        self.show()


image1 = FractalImage('images/img5.png')
image1.segment()
image1.save('output/img5.png')
