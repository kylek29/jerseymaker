# jerseymaker
Pieces of a Python based jersey maker that creates the artwork files necessary for print &amp; sew manufacturing based on a dataset file.

# _nameplatemaker.py
A set of functions broken out into a separate test script. Variables "chars" and "test_names" are just for testing as well as the "for" loop at the bottom.

### Purpose & Notes
PIL can be used to generate textual names based on a font and size, but stroking the name or doing more elaborate designs for each letter is a tad cumbersome. The purpose of this script is to create a given string (player's last name) into a nameplate object based on prerastered character sets. These character sets can be created from Photoshop using the github_char.psd template file located in /_support/templates and the PS javascript in /_support/scripts. However, any art program could be used to generate these files.

A character set is comprised of the character designs you want saved as individual letter .PNG files as char_*LETTER*.png (e.g. char_a.png or for a period, char_..png). The script will take the STRING passed to it and load each character artwork file into a dictionary, skipping if it has already loaded that character. It then uses this dictionary to reassemble the string.

### Installation & Usage
#### Generating Char Set

- Open Photoshop and the github_char.psd file.
- Make any changes you want to the single character (add gradients, fills, etc.)
- Remember to turn off the background.
- Go to File > Scripts > Browse and select "LoadCSVReplaceText.js"
- The script will ask you to select an output folder.
- The script will ask you for a prefix to the filename. I usually use 'chars_' for upper A-Z (and numbers, punctuation) and 'chars_l_' for lower.
- The script will ask you to select a .CSV file. 
-- For uppercase A-Z, numbers, and punctation: upper_a-z0-9_chars.csv
-- For lowercase a-z: lower_a-z.csv
- The script will ask you if you want to force UPPERCASE on the text.
- The script will generate individual .PNG's to the output folder. 
- NOTE: On Linux, more care may need to be taken to make sure the filename is the right case.
- Move those files to the _components directory under the script folder.

#### Generating nameplate

- Open the script in a Python editor and type some names into the test_names list. 
- Update the chars variable to point to the character set folder from before.
- Hit RUN
- It'll output to the script folder as a .PNG.

#### Tips / Gotchas

- Expects the image file to be a transparent background .PNG in RGBA format.
- Included character set only includes uppercase LETTERS and ".".
- Can do uppercase and lowercase numbers, but will clip the lowercase letters that extend outside of the box. This can be changed by creating the letters in photoshop with a larger bounding box.

#### Options
The create_nameplate method has a third optional kwargs element. Defaults are set within the method, but can be overriden by passing in the options you want to override as a dict (example under TEMP Variables) as an unpackable dict (e.g. **kwargs).

- kern_offset | This sets the spacing between each character. Int value, 10px spacing = 10
- space_offset | This sets the spacing for the " " character [space]. Int value, 10px spacing = 10
- max_size | This sets the maximum pixel width of the nameplate before it'll resized to fit.
- force_upper | Whether to force the output to use Uppercase only. Default is true.
- char_prefix | Prefix to prepend to the Image.Open call for the file. e.g. chars_b.png

### Methods / Functions
- resize_image | Takes in an image object and an INT for maximum width, resizes the image object proportionally to fit the max width. Returns the resized image object.
- create_letter | Takes in an image object, resizes the bounding box to the width boundaries (maintaining the height) of the character and returns the cropped version of the image.
- create_nameplate | Takes in a STRING and a CHARSET (folder location string), returns the completed nameplate.
