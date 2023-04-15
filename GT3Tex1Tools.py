import argparse
import pathlib
import tex1.tex1_to_png
import tex1.tex1_extractor
import others.options

parser = argparse.ArgumentParser(prog='GT3Tex1Tools', description='')
parser.add_argument('input', type=pathlib.Path, help='input file path or directory')
parser.add_argument('output_dir', type=pathlib.Path, nargs='?', default=None, help='output directory(optional)')
parser.add_argument('-p', '--topng',
                    help='converts Tex1(.img) to png files. The conversion is incomplete, and many swizzled files '
                         'in the model data, such as car and course data, '
                         'will fail to convert or will output incomplete png files.',
                    action="store_true")
parser.add_argument('-e', '--extractor',
                    help=':extract Tex1 files(.img) from files containing Tex1 such as pmb, gz, imgs, etc.',
                    action="store_true")
parser.add_argument('-r', '--recursive',
                    help='reads "input" as a directory and recursively retrieves files in the directory',
                    action="store_true")
parser.add_argument('-d', '--delimiter_conversion',
                    help='When outputting a file using the -r option, the directory name is written in the file name '
                         'instead of creating a directory.'
                         '(e.g., file name and location when outputting the img file "JP/arcade1.pmb" '
                         'using the -r option)'
                         'Without -d option: JP/arcade1.pmb/0000.img'
                         'With -d option:    JP_arcade1.pmb_0001.img',
                    action="store_true")
args = parser.parse_args()
conversion_options = others.options.argsToConversionOptions(args)

# Print Arguments
print('input:{}'.format(repr(args.input)))
if args.output_dir:
    print('output:{}'.format(repr(args.output_dir)))

if args.extractor:
    if args.recursive:
        if args.input.is_dir():
            tex1.tex1_extractor.extractTex1Recursive(args.input, args.output_dir, conversion_options)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        tex1.tex1_extractor.extractTex1(args.input, args.output_dir, None, conversion_options)
    else:
        print('Error: In this case, "input" must be a file.')
else:
    if args.recursive:
        if args.input.is_dir():
            tex1.tex1_to_png.makePngFromTex1Recursive(args.input, args.output_dir, conversion_options)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        tex1.tex1_to_png.makePngFromTex1(args.input, args.output_dir, None, conversion_options)
    else:
        print('Error: In this case, "input" must be a file.')
