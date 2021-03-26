from FractalImage import FractalImage


R, G, B = 0, 1, 2

# lab1
image = FractalImage('images/img5.png')
image.to_grayscale()
print(image.fractal_dimension_minkowski())

# lab2
image = FractalImage('images/img5.png')
# nullify red and blue channels
image.nullify_channels([R, B])
# save img with green palette
image.save('output/lab2_img3.png')

# lab3
image = FractalImage('images/img5.png')
image.to_grayscale()
# save img with grayscale
image.save('output/lab3_img3.png')

# lab4
image = FractalImage('images/img5.png')
image.to_grayscale()
print(image.fractal_dimension_blanket())
