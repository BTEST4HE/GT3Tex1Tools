import gzip
import io
import struct
from .helper import makeOutputDir


def extractTex1FromPMB(p_input, p_output_dir):
    # Reading pmb file
    pmb_data = p_input.read_bytes()

    # Define Variables
    tex1_count = struct.unpack('I', pmb_data[0x8:0xc])[0]
    tex1_offset = struct.unpack('I', pmb_data[0xc:0x10])[0]
    tex1_size_list = []
    tex1_offset_list = []

    # Create directory
    if tex1_count != 0:
        p_output_dir = makeOutputDir(p_input, p_output_dir) / p_input.name
        if p_output_dir.is_dir() is False:
            p_output_dir.mkdir()

    # Unpack PMB
    # Create list of offsets and sizes
    ptr = tex1_offset
    for i in range(tex1_count):
        tex1_size = struct.unpack('L', pmb_data[ptr:ptr + 0x4])[0]
        tex1_offset = struct.unpack('L', pmb_data[ptr + 0x4:ptr + 0x8])[0]
        tex1_size_list.append(tex1_size)
        tex1_offset_list.append(tex1_offset)
        ptr += 0x8

    # Extract Tex1 file
    for i in range(tex1_count):
        if i != tex1_count - 1:
            tex1_data = pmb_data[tex1_offset_list[i]:tex1_offset_list[i + 1]]
        else:
            tex1_data = pmb_data[tex1_offset_list[i]:]

        # Check if data is tex1 or gz
        magic_number = tex1_data[0:4]
        if magic_number[:2] == b'\x1f\x8b':
            check_padding = struct.unpack('I', tex1_data[-4:])[0]
            while check_padding != tex1_size_list[i]:
                tex1_data = tex1_data[:-1]
                check_padding = struct.unpack('I', tex1_data[-4:])[0]
            with io.BytesIO(gzip.decompress(tex1_data)) as gzip_file:
                tex1_output = gzip_file.read()
        elif magic_number == b'Tex1':
            tex1_output = tex1_data
        else:
            raise ValueError('Incorrect Tex1 data exists. Count:{}'.format(i))

        p_output = makeOutputDir(p_input, p_output_dir) / ('{:0>4}.img'.format(i))
        p_output.write_bytes(tex1_output)


def extractTex1FromOther(p_input, p_output_dir):
    # Reading Files
    if p_input.suffix == '.gz':
        with io.BytesIO(gzip.decompress(p_input.read_bytes())) as gzip_file:
            expanded_data = gzip_file.read()
        data = bytearray(expanded_data)
    else:
        data = bytearray(p_input.read_bytes())
    temp = data
    idx = temp.find(b'Tex1\x00\x00\x00\x00')
    i = 0

    # Create directory
    if idx != -1:
        p_output_dir = makeOutputDir(p_input, p_output_dir) / p_input.name
        if p_output_dir.is_dir() is False:
            p_output_dir.mkdir()

    # Extract Tex1 file
    while idx != -1:
        file_size = struct.unpack('I', temp[idx + 0xC:idx + 0x10])[0]
        tex1 = temp[idx:idx + file_size]
        p_output = makeOutputDir(p_input, p_output_dir) / ('{:0>4}.img'.format(i))
        p_output.write_bytes(tex1)
        temp = temp[idx + file_size:]
        idx = temp.find(b'Tex1\x00\x00\x00\x00')
        i += 1


def extractTex1(p_input, p_output_dir):
    print(str(p_input) + '\t', end='')
    try:
        if p_input.suffix == '.pmb':
            extractTex1FromPMB(p_input, p_output_dir)
        else:
            extractTex1FromOther(p_input, p_output_dir)
        print('Success')
    except Exception as e:
        print('Failure:', e.args)


def extractTex1Recursive(p_input, p_output_dir):
    p_output_dir = makeOutputDir(p_input, p_output_dir)
    input_path_list = [p for p in p_input.glob('**/*') if p.is_file()]
    for p in input_path_list:
        p_r = p.relative_to(p_input)
        p_o = p_output_dir / p_r.parents[0]
        if p_o.exists() is False:
            p_o.mkdir(parents=True, exist_ok=True)
        extractTex1(p, p_o)

