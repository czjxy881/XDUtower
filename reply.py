import xhj,sql,renren


def reply(mes):
    if u'转发' in mes:
        return 0
    elif u'捡' in mes or u'拾' in mes:


if __name__ == "__main__":
    while 1:
        s = raw_input('find:')
        print reply(s.decode('GBK'))
