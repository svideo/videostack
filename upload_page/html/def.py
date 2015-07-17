#!/usr/bin/env python

a = {'a':1, 'b': 2, 'c':3, 'd':4}


def hello(arg, **args):
    print(type(arg))
    print(args)

hello(1, a=1, b=2, c=3)

