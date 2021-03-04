from FractalImage import FractalImage


R, G, B = 0, 1, 2


# lab1
image = FractalImage('images/img3.png')
image.to_grayscale()
print(image.fractal_dimension())
image.save('output/lab1_img3.png')

# lab2
image = FractalImage('images/img3.png')
# nullify red and blue channels
image.nullify_channels([R, B])
# save img with green palette
image.save('output/lab2_img3.png')

# lab3
image = FractalImage('images/img3.png')
image.to_grayscale()
# save img with grayscale
image.save('output/lab3_img3.png')


