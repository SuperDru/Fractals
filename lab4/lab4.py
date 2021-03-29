from PIL import Image
import numpy as np
from scipy import stats


class FractalImage:
    def __init__(self, img_path):
        self.path = img_path
        self.img = Image.open(img_path)
        self.width = self.img.size[0]
        self.height = self.img.size[1]

    def to_grayscale(self):
        self.img = self.img.convert('L')

    def fractal_dimension_blanket(self):
        self.to_grayscale()
        cell_size = int(min(self.width, self.height) / 100)
        deltas = [1, 2]
        a_deltas = [0, 0]

        for x in range(int(self.width / cell_size)):
            for y in range(int(self.height / cell_size)):
                img = self.img.crop((x * cell_size, y * cell_size, x * cell_size + cell_size, y * cell_size + cell_size))
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


image1 = FractalImage('../images/img2.png')
print(f"{image1.path} = {image1.fractal_dimension_blanket()}")
image2 = FractalImage('../images/img3.png')
print(f"{image2.path} = {image2.fractal_dimension_blanket()}")
image3 = FractalImage('../images/img4.png')
print(f"{image3.path} = {image3.fractal_dimension_blanket()}")
image4 = FractalImage('../images/img5.png')
print(f"{image4.path} = {image4.fractal_dimension_blanket()}")
image5 = FractalImage('../images/img6.png')
print(f"{image5.path} = {image5.fractal_dimension_blanket()}")
