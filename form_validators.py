def is_empty(field):
    return not bool(field)

def is_file_format_correct(filename):
    file_format = filename.split('.')[-1]
    if file_format == 'xls':
        return True
    else:
        return False