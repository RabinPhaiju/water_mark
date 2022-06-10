from PIL import Image, ImageDraw, ImageFont

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

if __name__ == '__main__':

    fontname = "Roboto-Black.ttf"
    fontsize = 34
    text = "Khwopa Engineering College"
    
    colorText = "white"
    colorOutline = "red"
    colorBackground = "blue"

    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(text, font)
    img = Image.new('RGB', (width+8, height*2))
    d = ImageDraw.Draw(img)
    d.text((2, height/2), text, fill=colorText, font=font)
    # d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
    
    img.save("image.png")