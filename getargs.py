#!/usr/bin/env python3

import argparse


class GetArgs():
    def __init__(self):
        self.set_args_list()

    def set_args_list(self):
        py_des = '''\
                ----------------------------------------------------------------------------

                remoteCLI: Remote cli command options.

                ----------------------------------------------------------------------------

                '''

        py_usage = '''%(prog)s remoteCLI [options] / [-h/--help]'''

        py_ver = '%(prog)s Experimental'

        self.parser = argparse.ArgumentParser(prog="remoteCLI",
                                              allow_abbrev=False,
                                              formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                              description=py_des,
                                              usage=py_usage,
                                              epilog="For more information about each option, please see man remoteCLI.1 " +
                                              "This program is distributed under GPL-2 license",
                                              add_help=False)

        self.parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                                 help='Show this help message and exit.')

        subparsers = self.parser.add_subparsers(title='System Commands')
        system_parser = subparsers.add_parser("system")
        system_parser.add_argument("command",
                                   help="System command",
                                   choices=["ls", "pwd", "cwd"]
                                   )

    def check_args(self, args):
        args = self.parser.parse_args(args)

        args_dict = {}
        for i in args.__dict__:
            if args.__dict__[i] not in [False, None]:
                args_dict[i] = args.__dict__[i]

        return args_dict
