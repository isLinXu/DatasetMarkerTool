import os


def check_dir(directory):
    '''
    检查路径
    :param directory:
    :return:
    '''
    if not os.path.exists(directory):
        os.makedirs(directory)
        print('Creating directory -', directory)
    else:
        print('Directory exists -', directory)