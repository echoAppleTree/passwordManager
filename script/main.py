"""
Author : David-Alexandre Guenette <da.guenette@icloud.com>
Date   : 2021-01-18
Purpose: Execution File fo Password Manager
"""

import argparse
import interface as itf 
import authentication as auth

def get_args():
    """ Get command-line arguments """
    
    parser = argparse.ArgumentParser(
        description='Password Manager',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
    parser.add_argument('uname',
                        metavar='str',
                        help='Your username')

    return parser.parse_args()


def main():
    """Build the magic!"""
    args = get_args()
    uname = args.uname

    if auth.authentication(uname):
        itf.build_itf()
    else:
        print("Sorry! You're not authorized.")

if __name__ == '__main__':
    main()