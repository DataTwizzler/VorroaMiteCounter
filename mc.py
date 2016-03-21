#!/usr/bin/env python
import sys
print sys.argv
from SimpleCV import *

#v04 = binarize without setting threshold
# python mc3.py bb
# Call from the command line and exclude the ".jpg"
filename = sys.argv[1]
filetype = '.jpg'
directory_path = 'C:/mites/'
image_path = directory_path + filename + filetype
processed_image_path     = directory_path + filename + '_mite_count_v04'     + filetype
processed_bin_image_path = directory_path + filename + '_mite_count_bin_v04' + filetype

known_mite_pos_x = 670
known_mite_pos_y = 350
known_mite_box   = 20

bin_threshold = 150

minMiteWidth  = 5
maxMiteWidth  = 15 #15
minMiteLength = 5
maxMiteLength = 15 #15
minMiteArea   = 40
maxMiteArea   = 80 #80
miteCircle    = 10

search_area_height   = 0
search_area_width    = 0
search_area_offset_height  = 0
search_area_offset_width   = 0

text_line_height = 50
text_first_line_offset = 10
text_line_indent       = 10
text_line_1 = text_first_line_offset
text_line_2 = text_line_1 + text_line_height
text_line_3 = text_line_2 + text_line_height
text_line_4 = text_line_3 + text_line_height
text_line_5 = text_line_4 + text_line_height

print ' '
print '*** Constants ***'
print 'The minMiteWidth  is ' + str(minMiteWidth)  
print 'The maxMiteWidth  is ' + str(maxMiteWidth)  
print 'The minMiteLength is ' + str(minMiteLength)  
print 'The maxMiteLength is ' + str(maxMiteLength)  
print 'The minMiteArea   is ' + str(minMiteArea)  
print 'The maxMiteArea   is ' + str(maxMiteArea)  
print 'The search_area_height is ' + str(search_area_height)  
print 'The search_area_width  is ' + str(search_area_width)  
print 'The search_area_offset_height is ' + str(search_area_offset_height)  
print 'The search_area_offset_width  is ' + str(search_area_offset_width)  
print 'The bin_threshold is ' + str(bin_threshold)

search_area_height   = 0
search_area_width    = 0
search_area_offset_height  = 0
search_area_offset_width   = 0

bb = Image(image_path)
bb_size = bb.size()




print ' '
print '*** Image Attributes ***'
print 'The ' + image_path + ' size  is ' + str(bb_size)
#print ' '
#print '*** EXIF Data ***'
f = open(image_path, 'rb')
tags = EXIF.process_file(f)
#for tag in tags.keys():
#    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename','EXIF MakerNote'):
#        print "Key: %s, value %s" % (tag, tags[tag])


bb_crop = bb.crop(search_area_offset_width,search_area_offset_height,
                  bb.width-search_area_width,bb.height-search_area_height)

# Setup the text layer to write analysis data.
bb_crop_size = bb_crop.size()
textLayer = DrawingLayer(bb_crop_size)
textLayer.selectFont('arial')
textLayer.setFontSize(24)
textLayer.setFontBold(True)
textLayer.text('The ' + image_path + ' size  is ' + str(bb_size),  (text_line_indent, text_line_1), color=Color.RED)
textLayer.text('EXIF DateTimeOriginal is' + str(tags['EXIF DateTimeOriginal']),  (text_line_indent, text_line_2), color=Color.RED)

# Setup the mite marking layer to highlight the blobs identified as mites.
miteLayer = DrawingLayer(bb_crop_size)

#bb_crop_bin = bb_crop.binarize(thresh=bin_threshold)
bb_crop_bin = bb_crop.binarize()

blobs = bb_crop_bin.findBlobs(minsize=minMiteWidth, maxsize=maxMiteArea)

num_mite_blobs     = 0
num_not_mite_blobs = 0

if (blobs is not None):
    print ' '
    print '*** Feature Set Analysis ***'
    print 'The narrowest width is ' + str(np.min(blobs.width()))  
    print 'The widest width is ' + str(np.max(blobs.width()))  
    print 'The shortest length is ' + str(np.min(blobs.length()))  
    print 'The longest length is ' + str(np.max(blobs.length()))  
    print 'The smallest area is ' + str(np.min(blobs.area()))  
    print 'The largest area is ' + str(np.max(blobs.area()))  

    for b in blobs:
#        print ' '
        if ((b.length() >= minMiteLength) and (b.width() <= maxMiteLength) and 
            (b.length() >= minMiteWidth) and (b.width() <= maxMiteWidth) and 
            (b.area() >= minMiteArea) and (b.area() <= maxMiteArea)):  
            num_mite_blobs = num_mite_blobs + 1
            b.draw(width=2, color=Color.BLUE)
            miteLayer.circle(b.centroid(), 
                             miteCircle,
                             color=Color.BLUE)
                             #width=int(2)) 

#            print '*Mite blob found:'
#            print '  The position    is ' + str(b.centroid())  
#            print '  The width       is ' + str(b.width())  
#            print '  The length      is ' + str(b.length())  
#            print '  The area        is ' + str(b.area())  
#            print '  The meanColor   is ' + str(b.meanColor())
#            print '  The centroid    is ' + str(b.centroid())
#            print '  The isCircle    is ' + str(b.isCircle())
#            print '  The isRectangle is ' + str(b.isRectangle())
#            print '  The isSquare    is ' + str(b.isSquare())
            
        else:
            num_not_mite_blobs = num_not_mite_blobs + 1
            b.draw(width=2, color=Color.ORANGE)
            miteLayer.circle(b.centroid(), 
                             miteCircle,
                             color=Color.ORANGE)
                             #width=int(2)) 
#            print ' Non-Mite blob found:'

    print ' '
    print '*** Mite Count ***'
    print 'num_mite_blobs     is ' + str(num_mite_blobs)  
    print 'num_not_mite_blobs is ' + str(num_not_mite_blobs)  
    textLayer.text('Mite estimate is ' + str(num_mite_blobs),               (text_line_indent, text_line_3), color=Color.RED)
    textLayer.text('Non mite objects found is ' + str(num_not_mite_blobs),  (text_line_indent, text_line_4), color=Color.RED)
#    textLayer.text("12 ft", (400, 300), color=Color.RED)
#    textLayer.text("15 ft", (500, 300), color=Color.RED)

else:
    print ' '
    print '*** NO BLOBS FOUND ***'
    
bb_crop_bin.addDrawingLayer(textLayer)

bb_crop.addDrawingLayer(textLayer)
bb_crop.addDrawingLayer(miteLayer)

bb_crop_bin.show()
#bb_crop_bin.save(processed_bin_image_path)
bb_crop.save(processed_image_path)
Display().quit()