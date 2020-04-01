import os


def write_text(name, suffix, text, path='.'):
    assert os.path.exists(path)
    os.chdir(path)
    with open("%s.%s" % (name, suffix), 'w') as f:
        f.write(text)


def write_image(name, suffix, images, path='.'):
    assert os.path.exists(path)
    assert isinstance(images, list)
    os.chdir(path)
    # 以下的代码由于os.path.join()方法无法输入中文路径而废弃
    """if not os.path.isdir(os.path.join(path, name)):
        os.mkdir(os.path.join(path, name))
    os.chdir(os.path.join(path, name))"""
    for i, each in enumerate(images):
        with open("%d.%s" % (i, suffix), 'wb') as f:
            f.write(each)
