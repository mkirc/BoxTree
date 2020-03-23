
def read_file(fn):
    file = open(fn, 'r')
    _d = [x.split(',') for x in file.read().split('\n')]
    file.close()

    return _d
# checks for wrong lines in file
def test_filter(fn):
    
    _d = read_file(fn)
    data = []
    for d in _d:
        if 'SPEDI' in d[0]:
            continue
        if '51' in d[0]:
            continue
        if '20' in d[0]:
            continue
        if '19' in d[0]:
            continue
        if 'BEH' in d[0]:
            continue
        if '90' in d[0]:
            continue
        data.append([d[0], [int(x) for x in d[1:4]], [int(x) for x in d[4:7]]])

    if len(data) < len(_d):
        return False

    return True


def test_sizes(fn):
    _d = read_file(fn)

    for d in _d:
        box = sorted([int(x) for x in d[1:4]])
        item = sorted([int(x) for x in d[4:7]])


        # make sure item < box

        


def test(fn):

    try:
        test_filter(fn)
    except Exception as e:
        print(repr(e))


test('../assets/data_old_biggest_01.csv')