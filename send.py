#!/usr/bin/python
# -*- coding: UTF-8 -*-
from reports import ParcelTrackDaily

if __name__ == '__main__':
    ptd = ParcelTrackDaily()
    ptd.generate()
    ptd.send()
