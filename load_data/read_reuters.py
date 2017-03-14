from __future__ import print_function

import os
import pickle
import sys

PYTHON_3 = sys.version_info >= (3, 0)


def read():
    for ls in os.listdir('data'):
        if ls.endswith('.pkl'):
            with open('data/' + ls, 'rb') as f:
                if PYTHON_3:
                    data = pickle.load(f, encoding='latin1')
                else:
                    data = pickle.load(f)
                for datum in data:
                    print('ts = {}, t = {}, h= {}'.format(datum['ts'], datum['title'], datum['href']))


if __name__ == '__main__':
    read()
