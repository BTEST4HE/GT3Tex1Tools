# GT3Tex1Tools
___
This is a tool for handling image files (.img) called Tex1 used in GT3.
Currently there is a function to convert from Tex1 files to PNG files (incomplete) and a function to extract Tex1 files from pmb, gz, imgs, etc. files.

# Downloads
___
[Latest release](https://github.com/BTEST4HE/GT3Tex1Tools/releases/latest)

# Dependancies
___
    Pillow

## Usage
___
`GT3Tex1Tools [options] input [output_dir]`

### Positional arguments
`input`:input file path or directory  
`output_dir`:output directory(optional)  

### Optional arguments(options)
`-h, --help`:show this help message and exit  
`-p, --topng`:converts Tex1(.img) to png files. The conversion is incomplete, and many swizzled files in the model data, such as car and course data, will fail to convert or will output incomplete png files.  
`-e, --extractor`:extract Tex1 files(.img) from files containing Tex1 such as pmb, gz, imgs, etc.  
`-r, --recursive`:reads "input" as a directory and recursively retrieves files in the directory  
`-d, --extractor`:When outputting a file using the -r option, the directory name is written in the file name instead of creating a directory.  
(e.g., file name and location when outputting the img file "JP/arcade1.pmb" using the -r option)  
Without -d option: JP/arcade1.pmb/0000.img  
With -d option:    JP_arcade1.pmb_0001.img
