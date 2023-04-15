class ConversionOptions:
    def __init__(self, delimiter_conversion):
        self.is_delimiter_conversion = delimiter_conversion


def argsToConversionOptions(args):
    conversion_options = ConversionOptions(args.delimiter_conversion)
    return conversion_options


def delimiterConversion(p_r):
    file_name = ''
    for name in p_r.parts:
        file_name += name + '_'
    return file_name[:-1]
