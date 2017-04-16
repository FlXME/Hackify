# Copyright (C) CroackDesign, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Felix Bergmann <FelixBergmannDE@GMail.com>, May 2016


from PIL import Image, ImageDraw
from os import linesep, path, makedirs, listdir
from random import randint, sample, uniform
import itertools
from shutil import rmtree
from images2gif import writeGif
import sys
import warnings
warnings.filterwarnings("ignore")
sys.tracebacklimit = 0

# Set up variables to check
irImage = None

# Load image
while irImage is None:
    try:
        irImage = Image.open(raw_input("Image: "))
        print "Trying to load image ..."
    except IOError as e:
        print e
        print linesep

print "Successfully loaded " + str(irImage.filename) + ".\n"
		
speed = raw_input("Speed [Defaut: 0.2]: ") or 0.2
maxOffsetInput = raw_input("Max glitch offset (Left & Right in %) [Default: 20]: ") or 20
maxAmount = raw_input("Max amount of glitches per frame [Default: 6]: ") or 6
framesLen = raw_input("Frames to generate [Default: 6]: ") or 6

# Set up imported image variables
iName = path.splitext(irImage.filename)[0]
print "Converting image to advanced RGB"
iImage = irImage.convert("RGB")
del irImage
iWidth, iHeight = iImage.size
minChunkSize = int(round(iHeight / 30))
maxChunkSize = int(round(iHeight / 5))
maxHeight = iHeight - maxChunkSize
maxOffset = int(round(iWidth * (float(maxOffsetInput) / 100)))

# Replace Colors
print "Replacing all colors over 248 248 248 for a perfect transparent image. This could take some time."
newData = []
datas = iImage.getdata()
for item in datas:
    if item[0] > 248 and item[1] > 248 and item[2] > 248:
        newData.append((248, 248, 248))
    else:
        newData.append(item)

iImage.putdata(newData)

print "Done!"

# Make new image with border
new_size = (iWidth + maxOffset * 2, iHeight)
old_size = (iWidth, iHeight)

print "Generating new image. This could take some time."

newIm = Image.new("RGB", new_size, "white")


# Paste original image in middle
newIm.paste(iImage, ((new_size[0] - old_size[0]) / 2, (new_size[1] - old_size[1]) / 2))
print "Done!"
del iImage

print "Trying to create temporary folder."
#Create Folder
if not path.exists("tmpHackify"):
    makedirs("tmpHackify")
else:
    try:
        rmtree("tmpHackify")
        makedirs("tmpHackify")
    except WindowsError as e:
        print "\n" + str(e) + "\n\nSomething went wrong. Trying create a new folder anyways."
        makedirs("tmpHackify")

print "Generating image BackUp in RAM."
		
imageBak = Image.new("RGB", newIm.size)
imageBak.paste(newIm)

print "Done!\nGenerating starting frame..."

newIm.save("tmpHackify/Hackify0.gif", "GIF", transparency=0)

# Glitch
for x in range(1, int(framesLen)):
    print "Generating frame " + str(x) + "..."
    for _ in itertools.repeat(None, randint(0, int(maxAmount))):
        ChunkSize = randint(minChunkSize, maxChunkSize)
        ChunkLoc = randint(0, maxHeight)
        transparent_area = (maxOffset, ChunkLoc, iWidth + maxOffset, ChunkLoc + ChunkSize)
        glitchData = newIm.crop(transparent_area)
        glitchData.load()
        newIm.paste((255, 255, 255), transparent_area)
        newIm.paste(glitchData, (transparent_area[0] + int(round(uniform(-maxOffset, maxOffset))), transparent_area[1]))
    newIm.save("tmpHackify/Hackify" + str(x) + ".gif", "GIF", transparency=0)
    newIm.paste(imageBak)

print "Generating gif..."
file_names = sorted(fn for fn in listdir('tmpHackify') if fn.endswith('.gif'))
images = [Image.open("tmpHackify/" + fn) for fn in file_names]
print "Adding a custom GraphicsControlExt [GraphicsControlExt: \\x21 \\xF9 \\x04 \\x09 (000 010 0 1) \\x00]...\nDo not change this!"
writeGif(''.join(sample(iName, len(iName))) + iName + ''.join(sample(iName, len(iName))) + "_hackify.gif", images, duration=float(speed), loops=float("inf"))
raw_input("\nDone! Press enter to continue")