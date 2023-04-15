import struct
from PIL import Image
from others.helper import makeOutputDir
import others.options


def calculateAlphaChannelForPNG(input_a):
    output_a = input_a * 2
    if output_a >= 0x100:
        output_a = 0xff
    return output_a


def makePaletteSorted(plt_data):
    plt_list = []
    ptr = 0
    while ptr < len(plt_data):
        pl = [[]]
        for i in range(4):
            for j in range(8):
                r = struct.pack('>B', plt_data[ptr])
                g = struct.pack('>B', plt_data[ptr + 1])
                b = struct.pack('>B', plt_data[ptr + 2])
                a = struct.pack('>B', calculateAlphaChannelForPNG(plt_data[ptr + 3]))
                plt = r + g + b + a
                pl[i].append(plt)
                ptr += 4
            if i < 3:
                pl.append([])
        temp = pl[0] + pl[2] + pl[1] + pl[3]
        plt_list += temp
    return plt_list


def makePalette(plt_data):
    plt_list = []
    ptr = 0
    while ptr < len(plt_data):
        r = struct.pack('>B', plt_data[ptr])
        g = struct.pack('>B', plt_data[ptr + 1])
        b = struct.pack('>B', plt_data[ptr + 2])
        a = struct.pack('>B', calculateAlphaChannelForPNG(plt_data[ptr + 3]))
        plt = r + g + b + a
        plt_list.append(plt)
        ptr += 4
    return plt_list


def tex1_to_png(p_input, p_output):
    tex1_data = p_input.read_bytes()
    # Check the magic number
    if tex1_data[0:4] != b'Tex1':
        raise ValueError('Not Tex1 file.')

    # Get data from the header
    h_file_size = struct.unpack('I', tex1_data[0xC:0x10])[0]
    h_c2_count = struct.unpack('H', tex1_data[0x16:0x18])[0]
    h_c2_ofs = struct.unpack('I', tex1_data[0x1C:0x20])[0]

    # Returns an error if the tex1 file has no data
    if h_c2_ofs == h_file_size:
        raise ValueError('It is an Tex1 file without substance')

    # Returns an error if there are more than three chunk2s, since they are not supported
    if h_c2_count > 3:
        raise ValueError('Unsupported Tex1 files:Three or more chunk2 exist')

    # Get data from chunk2
    c2_data_ofs = struct.unpack('I', tex1_data[h_c2_ofs:h_c2_ofs + 0x4])[0]
    c2_data_type = struct.unpack('B', tex1_data[h_c2_ofs + 0x7:h_c2_ofs + 0x8])[0]
    c2_data_width = struct.unpack('H', tex1_data[h_c2_ofs + 0x8:h_c2_ofs + 0xa])[0]
    c2_data_height = struct.unpack('H', tex1_data[h_c2_ofs + 0xa:h_c2_ofs + 0xc])[0]
    c2_plt_ofs = struct.unpack('I', tex1_data[h_c2_ofs + 0xc:h_c2_ofs + 0x10])[0]
    c2_plt_width = struct.unpack('H', tex1_data[h_c2_ofs + 0x14:h_c2_ofs + 0x16])[0]
    c2_plt_height = struct.unpack('H', tex1_data[h_c2_ofs + 0x16:h_c2_ofs + 0x18])[0]
    plt_size = c2_plt_width * c2_plt_height

    # If palette exists
    if c2_plt_ofs != 0:
        tex1_image_data = tex1_data[c2_data_ofs:c2_plt_ofs]
        plt_data = tex1_data[c2_plt_ofs:c2_plt_ofs + (plt_size * 4)]
        im_new = Image.new('RGBA', (c2_data_width, c2_data_height))

        # Check bpp
        if c2_data_type == 0x0 or c2_data_type == 0x14:
            bpp = 4
        elif c2_data_type == 0x1 or c2_data_type == 0x13:
            bpp = 8
        else:
            raise ValueError('Unsupported Tex1 files:Data type value in chunk2 is not supported by this tool')
        if bpp == 4:
            bpp_data = b''
            for i in tex1_image_data:
                bpp_data_l = i & 0xf
                bpp_data_r = (i >> 4) & 0xf
                bpp_data += bpp_data_l.to_bytes(1, byteorder='little') + bpp_data_r.to_bytes(1, byteorder='little')
            tex1_image_data = bpp_data

        if plt_size >= 0x20:
            plt_list = makePaletteSorted(plt_data)
        else:
            plt_list = makePalette(plt_data)

        ptr = 0
        for y in range(c2_data_height):
            for x in range(c2_data_width):
                i = tex1_image_data[ptr]
                r = plt_list[i][0]
                g = plt_list[i][1]
                b = plt_list[i][2]
                a = calculateAlphaChannelForPNG(plt_list[i][3])
                im_new.putpixel((x, y), (r, g, b, a))
                ptr += 1

    # If palette does not exist
    else:
        tex1_image_data = tex1_data[c2_data_ofs:h_file_size]
        if c2_data_type == 1:
            im_new = Image.new('RGB', (c2_data_width, c2_data_height))
            ptr = 0
            for y in range(c2_data_height):
                for x in range(c2_data_width):
                    r = tex1_image_data[ptr]
                    g = tex1_image_data[ptr + 1]
                    b = tex1_image_data[ptr + 2]
                    im_new.putpixel((x, y), (r, g, b))
                    ptr += 3
        elif c2_data_type == 0 or c2_data_type == 0x13 or c2_data_type == 0x14:
            im_new = Image.new('RGBA', (c2_data_width, c2_data_height))
            ptr = 0
            for y in range(c2_data_height):
                for x in range(c2_data_width):
                    r = tex1_image_data[ptr]
                    g = tex1_image_data[ptr + 1]
                    b = tex1_image_data[ptr + 2]
                    a = calculateAlphaChannelForPNG(tex1_image_data[ptr + 3])
                    im_new.putpixel((x, y), (r, g, b, a))
                    ptr += 4
        else:
            raise ValueError('Unsupported tex1 files:Data type value in chunk2 is not supported by this tool')
    im_new.save(p_output)


def makePngFromTex1(p_input, p_output_dir, p_relative, conversion_options):
    print(str(p_input) + '\t', end='')
    if conversion_options.is_delimiter_conversion and p_relative is not None:
        png_filename = others.options.delimiterConversion(p_relative.with_suffix('.png'))
    else:
        png_filename = p_input.with_suffix('.png').name
    p_output = makeOutputDir(p_input, p_output_dir) / png_filename
    try:
        tex1_to_png(p_input, p_output)
        print('Success')
    except Exception as e:
        print('Failure:', e.args)


def makePngFromTex1Recursive(p_input, p_output_dir, conversion_options):
    p_output_dir = makeOutputDir(p_input, p_output_dir)
    input_path_list = [p for p in p_input.rglob('*.img') if p.is_file()]
    for p in input_path_list:
        p_r = p.relative_to(p_input)
        if conversion_options.is_delimiter_conversion:
            p_o = p_output_dir
        else:
            p_o = p_output_dir / p_r.parents[0]
            if p_o.exists() is False:
                p_o.mkdir(parents=True, exist_ok=True)
        makePngFromTex1(p, p_o, p_r, conversion_options)
