#!/usr/bin/env python3

import os
import sys
from server import Server


def main():
    server = Server()
    server.start()

if __name__ == '__main__':
    main()