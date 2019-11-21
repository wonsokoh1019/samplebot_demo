#!/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./')
from scripts.initDB import init_db
from scripts.registerBot import init_bot


def main():
    init_db()
    init_bot()


if __name__ == "__main__":
    main()
