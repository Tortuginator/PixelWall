from PIL import Image, ImageDraw


class Frame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pilObject = Image.new("RGBA", (self.height, self.width), (0, 0, 0, 255))
