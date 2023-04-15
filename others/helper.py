def makeOutputDir(p_input, p_output_dir):
    if p_output_dir is None or p_input == p_output_dir:
        p_output_dir = p_input / 'out' if p_input.is_dir() else p_input.parent / 'out'
        if p_output_dir.is_dir() is False:
            p_output_dir.mkdir()
    return p_output_dir

