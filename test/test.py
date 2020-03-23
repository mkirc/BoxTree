# testing
from pprint import pprint

from container import Container
from item import Item

def parse_result(fn):
    file = open(fn, 'r')
    # file = open('data_recent_01.csv', 'r')
    # file = open('data_r_01.csv', 'r')
    _d = [x.split(',') for x in file.read().split('\n')]
    file.close()
    # pprint(_d)

    data = []
    for d in _d:
        data.append([d[0], [int(x) for x in d[1:4]], [int(x) for x in d[4:7]]])

    # pprint(data[:-1])
    return data[:-1]

def boxes_from_file(fn):

    # file = open('data_r_01.csv', 'r')
    file = open(fn, 'r')
    _d = [x.split(',') for x in file.read().split('\n')]
    file.close()
    # pprint(_d)
    
    data = []
    for d in _d:
        ddim = [int(x) for x in d[1:4]]
        if len(ddim) == 3:
            data.append([d[0], ddim])

    return data


def parse_test_data(fn):
    file = open(fn, 'r')
    # file = open('data_recent_01.csv', 'r')
    # file = open('data_r_01.csv', 'r')
    _d = [x.split(',') for x in file.read().split('\n')]
    file.close()
    # pprint(_d)

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
        # pprint(data)

    # pprint(data[:-1])
    return data[:-1]

def repack(container, items):
    # make sure container are sorted by volume asc

    for i in items:
        for c in container:
            if c.fit(i):
                c.items.append(i)
                break
        else:
            # raise Exception(f'cannot fit item {i}')
            # print(f'cannot fit item {i}')
            continue

    return container


def main(*args):

    # res_data = parse_result(args[0])

    _boxes = boxes_from_file(args[0])

    # pprint(res_data[0])
    # pprint(len(res_data))

    # _packages = {}
    # for r in res_data:
    #     if r[0] not in _packages:
    #         _packages[r[0]] = r[1]

    # # pprint(_packages)
    # # pprint(len(_packages))

    # new_containers = []
    # for n, dim in _packages.items():
    #     _c = Container(dim)
    #     _c.name = n
    #     new_containers.append(_c)

    new_containers = []
    for p in _boxes:
        _c = Container(p[1])
        _c.name = p[0]
        new_containers.append(_c)

    # pprint([str(c) for c in containers])
    pprint(len(new_containers))

    test_data = parse_test_data(args[1])
    pprint(test_data[0])
    print(len(test_data))

    test_data_items = []
    _test_data_boxes = {}

    for t in test_data:
        test_data_items.append(Item(t[2]))

        if t[0] not in _test_data_boxes:
            _c = Container(t[1])
            _c.name = t[0]

            _test_data_boxes[t[0]] = _c

    old_containers = []
    for n,b in _test_data_boxes.items():
        old_containers.append(b)

    pprint([str(c) for c in old_containers])
    pprint(len(old_containers))
    pprint(len(new_containers))

    new_containers.sort(key= lambda x: x.volume)
    old_containers.sort(key= lambda x: x.volume)

    re_old = repack(old_containers, test_data_items)
    re_new = repack(new_containers, test_data_items)

    # pprint([x.log() for x in new_containers])
    pprint('-----------------------')
    # pprint([x.log() for x in old_containers])
    # item_total_volume = sum([it.volume for it in test_data_items])
    old_total_volume = sum([x.volume * len(x.items) for x in re_old])
    new_total_volume = sum([x.volume * len(x.items) for x in re_new])
    check_new_total_volume = sum([len(x.items) for x in re_new])
    check_old_total_volume = sum([len(x.items) for x in re_old])

    print('check')
    print(check_new_total_volume, check_old_total_volume)
    print(check_old_total_volume == check_new_total_volume)
    print('-.')

    pprint(old_total_volume - new_total_volume)
    pprint(new_total_volume / old_total_volume)
    pprint(old_total_volume)
    pprint(new_total_volume)
    
    print(len(test_data_items))


    # sonder test nur mit items die auch verpackt werden können
    _sitems = []
    for c in re_new:
        _sitems += c.items

    pprint(len(_sitems))
    for o in old_containers:
        o.items = []
    for n in new_containers:
        n.items = []

    re_old = repack(old_containers, _sitems)
    re_new = repack(new_containers, _sitems)

    # pprint([x.log() for x in new_containers])
    pprint('-----------------------')
    # pprint([x.log() for x in old_containers])
    
    old_total_volume = sum([x.volume * len(x.items) for x in re_old])
    new_total_volume = sum([x.volume * len(x.items) for x in re_new])
    check_new_total_volume = sum([len(x.items) for x in re_new])
    check_old_total_volume = sum([len(x.items) for x in re_old])

    print('check')
    print(check_new_total_volume, check_old_total_volume)
    print(check_old_total_volume == check_new_total_volume)
    print('-.')

    pprint(old_total_volume - new_total_volume)
    pprint(new_total_volume / old_total_volume)
    pprint(old_total_volume)
    pprint(new_total_volume)

    # pprint([x.log() for x in re_new])
    pprint([x.log() for x in re_old])


result_file = '../assets/candidates.csv'
# data_file = '../assets/data_new_biggest_01.csv'
data_file = '../assets/data_old_biggest_01.csv'


if __name__ == '__main__':
    main(result_file, data_file)