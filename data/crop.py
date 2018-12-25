from PIL import Image
img = Image.open('cards.png')
area = (400, 400, 800, 800)
img = img.crop(area)
img.save('cards-out.png')
