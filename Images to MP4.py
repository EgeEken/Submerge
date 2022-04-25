import imageio

filename = input('File name: ')
imagecount = int(input('Image count: '))

filenames = [filename + str(i) + '.png' for i in range(imagecount)]

with imageio.get_writer('mp4test.mp4', mode='I', fps = 50) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
