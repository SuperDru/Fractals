from PIL import Image
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


plt.style.use('seaborn')


class FractalImage:
    def __init__(self, img_path):
        self.path = img_path
        self.img = Image.open(img_path)
        self.width = self.img.size[0]
        self.height = self.img.size[1]

    def to_grayscale(self):
        self.img = self.img.convert('L')

    def get_dimensions(self):
        res = []
        cell_sizes = [2, 4, 8, 16, 32, 64, 128, 256]
        for c in cell_sizes:
            res.append(self.calculate_dimension(c))

        print(res)
        return res

    def calculate_dimension(self, cell_size=20):
        self.to_grayscale()
        deltas = [1, 2]
        a_deltas = np.zeros(len(deltas))

        for x in range(int(self.width / cell_size)):
            for y in range(int(self.height / cell_size)):
                img = self.img.crop((x * cell_size, y * cell_size, x * cell_size + cell_size, y * cell_size + cell_size))
                pixels = img.load()

                u = np.zeros((len(deltas) + 1, cell_size + 1, cell_size + 1))
                b = np.zeros((len(deltas) + 1, cell_size + 1, cell_size + 1))

                vol = np.zeros(len(deltas) + 1)

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


image1 = FractalImage('./images/health.png')
res1 = image1.get_dimensions()
image2 = FractalImage('./images/not_health.png')
res2 = image2.get_dimensions()

cell_sizes = [2, 4, 8, 16, 32, 64, 128, 256]
fig, ax = plt.subplots()

ax.plot(cell_sizes, res1)
ax.plot(cell_sizes, res2)

ax.set(xlabel='cell size', ylabel='dimension')
plt.show()
