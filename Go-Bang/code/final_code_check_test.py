#!/usr/bin/env python3
import sys
from new_code_check2 import CodeCheck
def main():
    code_checker = CodeCheck("/Users/wangyutong/PycharmProjects/AI/new13.py", 15)
    if not code_checker.check_code():
        print(code_checker.errormsg)
    else:
        print('pass')

if __name__ == '__main__':
    main()