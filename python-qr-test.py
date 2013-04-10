import Image, ImageDraw

out="/home/mike/Desktop/qrtest.png"

image = Image.new("RGB",(25,25),0xFFFFFF) #white image 25x25 px
draw = ImageDraw.Draw(image)

#set up Postion
draw.rectangle((0,0,6,6),0x000000)
draw.rectangle((1,1,5,5),0xFFFFFF)
draw.rectangle((2,2,4,4),0x000000)

draw.rectangle((18,0,24,6),0x000000)
draw.rectangle((19,1,23,5),0xFFFFFF)
draw.rectangle((20,2,22,4),0x000000)

draw.rectangle((0,18,6,24),0x000000)
draw.rectangle((1,19,5,23),0xFFFFFF)
draw.rectangle((2,20,4,22),0x000000)

#set up Alignment
draw.rectangle((16,16,20,20),0x000000)
draw.rectangle((17,17,19,19),0xFFFFFF)
draw.rectangle((18,18,18,18),0x000000)

#set up Timing
image.putpixel((6,8),0x000000)
image.putpixel((6,10),0x000000)
image.putpixel((6,12),0x000000)
image.putpixel((6,14),0x000000)
image.putpixel((6,16),0x000000)

image.putpixel((8,6),0x000000)
image.putpixel((10,6),0x000000)
image.putpixel((12,6),0x000000)
image.putpixel((14,6),0x000000)
image.putpixel((16,6),0x000000)

#draw = ImageDraw.Draw(image)
#draw.line((5,5,95,95), fill=0x00ff00)
#del draw

del draw
image.save(out, 'PNG')
