from PIL import Image,ImageDraw
img = Image.new("RGB",(28,28),(0,0,0));
imgdraw = ImageDraw.Draw(img)
print img.size