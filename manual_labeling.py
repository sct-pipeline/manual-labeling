import sys
import os
import argparse
import json
import subprocess


def get_parser():
    # Mandatory arguments
    parser = argparse.ArgumentParser(
        description=" ",
        epilog="EXAMPLES:\n",
        add_help=None,
        prog=os.path.basename(__file__).strip('.py'))

    mandatoryArguments = parser.add_argument_group("\nMANDATORY ARGUMENTS")
    mandatoryArguments.add_argument(
        '-json',
        required=True,
        help="Json file containing list of path to image file",
    )
    mandatoryArguments.add_argument(
        '-author',
        required=True,
        help="Author name for json file",
    )
    optional = parser.add_argument_group("\nOPTIONAL ARGUMENTS")
    optional.add_argument(
        '-correct',
        default=0,
        help=" if this is activated the -ilabel option will be used and therefore existing file will be open")
    optional.add_argument(
        '-o',                                                                                                              help="output path")
    
    return parser


def main(args=None):
    if args is None:
        args = None if sys.argv[1:] else ['--help']
    parser = get_parser()
    arguments = parser.parse_args(args=args)
    json_path = arguments.json
    author_name = arguments.author
    correct = arguments.correct
    json_content = {"author": author_name, "label": "labels-disc-manual"}
    list_of_subj = [line.rstrip('\n') for line in open(json_path)]
    derivatives_base = list_of_subj[0].rsplit('/', 3)[0]  # file path is BIDS: last 3 elements are /sub-xx/anat/FILENAM
    derivatives_path = derivatives_base + '/derivatives/labels/'

    for im_path in list_of_subj:
        label_base = im_path.rsplit('/', 1)[-1][:-7]  # we remove the last 7 caracters that are .nii.gz
        subj = im_path.rsplit('/', 3)[-3]
        label_filename = label_base + '_labels-disc-manual.nii.gz'
        json_filename = label_base + '_labels-disc-manual.json'
        if arguments.o is not None:
            if os.path.exists(arguments.o +'/'+ subj + '/anat'):
                pass
            else:
                os.makedirs(arguments.o +'/'+ subj + '/anat')
            path_json =  arguments.o+'/'+ subj +'/anat/' + json_filename
            path_label = derivatives_path + subj + '/anat/' + label_filename  # retrieving label filename
            path_out = arguments.o +'/'+ subj + '/anat/' + label_filename
        else:
            path_json = derivatives_path + subj + '/anat/' + json_filename
            path_label = derivatives_path + subj + '/anat/' + label_filename  # retrieving label filename
            path_out = path_label

        if correct:
            if os.path.exists(path_label):
                command = """sct_label_utils -i """ + im_path + """ -create-viewer 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20 -ilabel """ + path_label + """ -o """ + path_out
            else:
                command = """sct_label_utils -i """ + im_path + """ -create-viewer 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20 -o """ + path_out

            subprocess.run(command, shell=True)

            with open(path_json, 'w') as f:
                json.dump(json_content, f)
        else:
            if os.path.exists(path_label):
                pass
            else:
                command = """sct_label_utils -i """ + im_path + """ -create-viewer 3,4,5,6,7,8,9,10,11,12,13,14,15 -o """ + path_out
                subprocess.run(command, shell=True)                                                                                     
                with open(path_json, 'w') as f:
                    json.dump(json_content, f)

                    
if __name__ == "__main__":
    main()
