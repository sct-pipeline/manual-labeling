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
        '-file',
        required=True,
        help="Json file containing list of path to image file",
    )
    mandatoryArguments.add_argument(
            '-path',
            required=True,
            help="path to bids folder",)
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
            '-o',
            help="output path. if empty it will save in BIDS_path/label/derivatives/sub/anat ")
    
    return parser


def main(args=None):
    if args is None:
        args = None if sys.argv[1:] else ['--help']
    parser = get_parser()
    arguments = parser.parse_args(args=args)
    file_path = arguments.file
    author_name = arguments.author
    correct = arguments.correct
    json_content = {"author": author_name, "label": "labels-disc-manual"}
    list_of_subj = [line.rstrip('\n') for line in open(file_path)]
    derivatives_base = arguments.path  # file path is BIDS: last 3 elements are /sub-xx/anat/FILENAM
    derivatives_path = derivatives_base + 'derivatives/labels'
    if arguments.o is not None:
        out_path = argument.o
    else:
        out_path = derivatives_path
        i=0

    try:
        for rel_path in list_of_subj:
            im_path = arguments.path+rel_path
            label_base = im_path.rsplit('/', 1)[-1][:-7]  # we remove the last 7 caracters that are .nii.gz
            subj = im_path.rsplit('/', 3)[-3]
            label_filename = label_base + '_labels-disc-manual.nii.gz'
            json_filename = label_base + '_labels-disc-manual.json'
        
            if os.path.exists( out_path+'/'+ subj + '/anat'):
                pass
            else:
                os.makedirs(out_path +'/'+ subj + '/anat')
            path_json =  out_path +'/'+ subj +'/anat/' + json_filename
            path_label = derivatives_path + subj + '/anat/' + label_filename  # retrieving label filename
            path_out = out_path +'/'+ subj + '/anat/' + label_filename

            if correct:
                if os.path.exists(path_label):
                    command = """sct_label_utils -i """ + im_path + """ -create-viewer 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20 -ilabel """ + path_label + """ -o """ + path_out
                else:
                    command = """sct_label_utils -i """ + im_path + """ -create-viewer 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20 -o """ + path_out

                subprocess.run(command, shell=True)
                i=i+1

                with open(path_json, 'w') as f:
                    json.dump(json_content, f)
            else:
                if os.path.exists(path_label):
                    pass
                else:
                    command = """sct_label_utils -i """ + im_path + """ -create-viewer 3,4,5,6,7,8,9,10,11,12,13,14,15 -o """ + path_out
                    subprocess.run(command, shell=True)
                    i=i+1
                    with open(path_json, 'w') as f:
                        json.dump(json_content, f)

    except KeyboardInterrupt:
            print('saving list')
            following = list_of_subj[i:]
            f = open(file_path,'w') # 'a' option allows you to append file to a list.
            l1 = map(lambda x: x + '\n', following)
            f.writelines(l1)
            f.close()

                    
if __name__ == "__main__":
    main()
