# -*- coding: utf-8 -*-
"""
Created on Wed May  2 17:04:29 2018

@author: kylek

Part of a larger project to build jersey artwork automatically from a dataset
that is fed into the system. This portion of the code is designed to create a
nameplate file.

"""

from PIL import Image

# TEMP VARIABLES / To be replaced by Preset config import.
chars = '_components/_chars/_exo-red-black/'
test_names = ['Doe', 'Zoolander', 'AReallyLongNameThatIsTooLong', 'J. Smith']


options = {
        'kern_offset' : 2,
        'max_size' : 1000,
        'force_upper' : False,
        'char_prefix' : 'chars_'
        }


def resize_image(img, max_w):
    """ Resizes an image to fit the maxsize.
    
    @pil img : Image object to be resized.
    @int max_w : Maximum size to downsample to.
    
    """
    img_w, img_h = img.size[0], img.size[1]  
    resize_ratio = ((max_w - 1) / float(img_w))
    size = (int(round(img_w * resize_ratio)), int(round(img_h * resize_ratio)))
    img.thumbnail(size, Image.ANTIALIAS)
    
    return img


def crop_to_w_bbox(obj):
    """ Creates a cropped version of the letter. Crops to the width of the object. """
    
    # Get the new bounding box, White Transparency Fix
    im_cords = obj.convert("RGBa").getbbox()
    obj_w, obj_h = obj.size[0], obj.size[1]
    
    # Crop to the sides, but keep the height0
    im = obj.crop(( im_cords[0], 0, im_cords[2], obj_h))
    
    return im

 
def create_nameplate(name, charset, **kwargs):
    """ Uses PIL to create a nameplate for a jersey file. 
    
    @str name : Word or name to put together.
    @str charset : Location of the character files to use.
    @dict **kwargs : Options array that gets unpacked and overrides the defaults.
    
    """
    
    # Some holders
    pil_charset = {}
    widths = []
       
    defaults = { 
            'kern_offset' : 12,     # Spacing between characters
            'space_offset' : 48,    # Pixels to represent a space
            'max_size' : 1990,      # Int, max width before it should be flagged.
            'force_upper' : True,   # Forces to use uppercase.
            'char_prefix' : 'char_'
            }
    
    options = {**defaults, **kwargs} # Merges an options dict with the defaults.
    
    # Reusable Helpers for the Options
    kern_offset = options['kern_offset']
    space_offset = options['space_offset']
    max_size = options['max_size']
    force_upper = options['force_upper']
    char_prefix = options['char_prefix']
       
    # Get the individual letter components
    for l in name:
        
        prefix = char_prefix
        
        if force_upper:
            l = l.upper()
        elif l.islower():
            prefix += 'l_'
        
        if l == ' ':
            print('Space Detected') #DEBUG
        elif l in pil_charset:
            print('Already Found {}, skipping ..'.format(l))
        else:
            cimg = Image.open(charset + prefix + l.lower() + '.png')
            cimg = crop_to_w_bbox(cimg)
            pil_charset[l] = (cimg, cimg.size[0])
            
        # Get the widths
        if l == ' ':
            widths.append(space_offset)
        else:
            widths.append(pil_charset[l][1])
        
    # Calculate the spacing / kerning
    kern_total = (len(widths) - 1) * kern_offset
    total_w = sum(widths)
    
    # Combine them to make the nameplate.
    new_img = Image.new('RGBA', (total_w + kern_total, cimg.size[1]))
    x_offset = 0
    for l in name:
        
        if force_upper:
            l = l.upper()
            
        if l == ' ':
            x_offset +=  space_offset
        else:
            new_img.paste(pil_charset[l][0], (x_offset, 0))
            x_offset += (kern_offset + pil_charset[l][1])
    
    # Check to see if the nameplate is too large.
    if new_img.size[0] > max_size:
        print('The nameplate for {} is over the max size limit.'.format(name.upper()))
        new_img = resize_image(new_img, max_size)
        
    return new_img


if __name__ == "__main__":
    for n in test_names:
        print(n)
        nameplate = create_nameplate(n, chars, **options)
        nameplate.save('T_' + n + '.png')
