import argparse
import pathlib
import tex1.tex1_to_png
import tex1.tex1_extractor


parser = argparse.ArgumentParser(prog='GT3Tex1Tools', description='')
parser.add_argument('input', type=pathlib.Path, help='input file path or directory')
parser.add_argument('output_dir', type=pathlib.Path, nargs='?', default=None, help='output directory(optional)')
parser.add_argument('-p', '--topng', help='Converts Tex1(.img) to png files. The conversion is incomplete, and many '
                                          'swizzled files in the model data, such as car and course data, '
                                          'will fail to convert or will output incomplete png files.',
                    action="store_true")
parser.add_argument('-e', '--extractor', help=':Extract Tex1 files(.img) from files containing Tex1 such as pmb, gz, '
                                              'imgs, etc.',
                    action="store_true")
parser.add_argument('-r', '--recursive', help='reads "input" as a directory and recursively retrieves files '
                                              'in the directory', action="store_true")
args = parser.parse_args()

# Print Arguments
print('input:{}'.format(repr(args.input)))
if args.output_dir:
    print('output:{}'.format(repr(args.output_dir)))

if args.extractor:
    if args.recursive:
        if args.input.is_dir():
            tex1.tex1_extractor.extractTex1Recursive(args.input, args.output_dir)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        tex1.tex1_extractor.extractTex1(args.input, args.output_dir)
    else:
        print('Error: In this case, "input" must be a file.')
else:
    if args.recursive:
        if args.input.is_dir():
            tex1.tex1_to_png.makePngFromTex1Recursive(args.input, args.output_dir)
        else:
            print('Error: When using the "-r" option, "input" must be a directory.')
    elif args.input.is_file():
        tex1.tex1_to_png.makePngFromTex1(args.input, args.output_dir)
    else:
        print('Error: In this case, "input" must be a file.')
