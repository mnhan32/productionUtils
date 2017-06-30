import argparse

parser = argparse.ArgumentParser(description = 'Process input arguments.')
parser.add_argument('-s', help='Maya Scene Name')
parser.add_argument('-f', help='Output File Name')
parser.add_argument('-d', help='Output Folder Name')
parser.add_argument('-ex', help='Extra Argument String')
args = parser.parse_args()

print args.s, args.f, args.d, args.ex