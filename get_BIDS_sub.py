import sys
import os
import argparse
import json
import subprocess
import nibabel as nib
import glob


def get_parser():
    # Mandatory arguments
    parser = argparse.ArgumentParser(
        description=" ",
        epilog="EXAMPLES:\n",
        add_help=None,
        prog=os.path.basename(__file__).strip('.py'))

    mandatoryArguments = parser.add_argument_group("\nMANDATORY ARGUMENTS")
    mandatoryArguments.add_argument(
        '-path',
        required=True,
        help="path to BIDS Data",
    )
    mandatoryArguments.add_argument(
        '-constraint',
        required=True,
        help="constraint field. You can use a specific fields from the header or 'orientation'",
    )

    mandatoryArguments.add_argument(
        '-value',
        required=True,
        help="value of constraint. Number or other. For orientation use capital letters (e.g., RPI) default operation is '==' if you wish to use something else please check the -ope option.",
    )
    optional = parser.add_argument_group("\nOPTIONAL ARGUMENTS")
    optional.add_argument(
        '-ope',
        default='==',
        help=" operation type. You can use '<' or '>'. Don't forget to use quote (Unix will throw EOL error otherwise)")

    optional = parser.add_argument_group("\nOPTIONAL ARGUMENTS")
    optional.add_argument(
        '-ofile',
        default='list_generated',
        help="name of output file (txt file). If the file already exist, the found subject will be added at the end of the file")

    return parser


def main(args=None):
    if args is None:
        args = None if sys.argv[1:] else ['--help']
    parser = get_parser()
    arguments = parser.parse_args(args=args)
    field = arguments.constraint
    path_data = arguments.path
    value = arguments.value
    operation = arguments.ope
    out = arguments.ofile
    path_images = (glob.glob(path_data+'/sub-*/*/*.nii.gz')) #grab all subject images path

    to_keep = []
    for im in path_images:
        nifti = nib.load(im)

        if field == 'orientation': #for now orientation gets a special case beacus it is not in the header per se
            if nib.aff2axcodes(nifti.affine) == (str(value[0]), str(value[1]), str(value[2])):
                to_keep.append(im)
        else:
            if eval(str(nifti.header[field]) + operation + str(value)): #eval() allows to ask the user for '<' or '>'
                to_keep.append(im)

    if len(to_keep)>0:
        f = open(out + field + operation + value +'.txt', 'a') # 'a' option allows you to append file to a list. 
        l1 = map(lambda x: x + '\n', to_keep)
        f.writelines(l1)
        f.close()
    else:
        print('No file matching your criteria found')


if __name__ == "__main__":
    main()





