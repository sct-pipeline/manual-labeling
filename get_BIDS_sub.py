import sys
import os
import argparse
import json
import subprocess
import nibabel as nib
import glob
import numpy

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
    optional = parser.add_argument_group("\nOPTIONAL ARGUMENTS")
    optional.add_argument(
        '-constraint',
        help="constraint field. You can use a specific fields from the header or 'orientation'",
    )

    optional.add_argument(
        '-value',
        help="value of constraint. Number or other. For orientation use capital letters (e.g., RPI) default operation is '==' if you wish to use something else please check the -ope option.",
    )
    optional.add_argument(
        '-ope',
        default='==',
        help=" operation type. You can use '<' or '>'. Don't forget to use quote (Unix will throw EOL error otherwise)")

    optional.add_argument(
        '-ofile',
        help="name of output file (txt file). If the file already exist, the found subject will be added at the end of the file")

    return parser


def get_view(im):
    nifti = nib.load(im)
    axis = nib.aff2axcodes(nifti.affine)
    best_res_axis = numpy.where(nifti.header['pixdim'][1:4] == nifti.header['pixdim'][1:4].min())[0]
    if len(best_res_axis)==3:
        return 'valid'
    elif len(best_res_axis)==2:
        plane_dic={'SA':'sagittal','SP':'sagittal','IA':'sagittal','IP':'sagittal','AS':'sagittal','PS':'sagittal','AI':'sagittal','PI':'sagittal','SR':'coronal','SL':'coronal','IR':'coronal','IL':'coronal','RS':'coronal','LS':'coronal','RI':'coronal','LI':'coronal','AR':'axial','AL':'axial','PR':'axial','PL':'axial','RP':'axial','LP':'axial','RA':'axial','LA':'axial'}
        best_plane = axis[best_res_axis[0]]+axis[best_res_axis[1]]
        print (best_plane)
        return (plane_dic[best_plane])



def main(args=None):
    if args is None:
        args = None if sys.argv[1:] else ['--help']
    parser = get_parser()
    arguments = parser.parse_args(args=args)
    if arguments.constraint is not None and arguments.value is None:
        parser.error("-constraint requires the -value option")
    field = arguments.constraint
    path_data = arguments.path
    value = arguments.value
    operation = arguments.ope
    if arguments.ofile is not None:
        out = arguments.ofile
    else:
        out =  'list-generated'+ field + operation + value 
    path_images = (glob.glob(path_data+'/sub-*/anat/*.nii.gz')) #grab all subject images path

    to_keep = []
    for im in path_images:

        if field == 'orientation':
            #Orientation gets a special case because it is not in the header per se
            if nib.aff2axcodes(nifti.affine) == (str(value[0]), str(value[1]), str(value[2])):
                spli = im.rsplit('/',3) #we get the last 3 element
                subj = spli[-3]+'/'+spli[-2]+'/'+spli[-1]
                to_keep.append(subj)

        elif field == 'view':
            #sagittal or axial or coronal. 
            if get_view(im) == value or get_view(im) == 'valid':
                spli = im.rsplit('/',3) #we get the last 3 element
                subj = spli[-3]+'/'+spli[-2]+'/'+spli[-1]
                to_keep.append(subj)


        elif field is not None:
            nifti = nib.load(im)
            if eval(str(nifti.header[field]) + operation + str(value)): #eval() allows to ask the user for '<' or '>'
                spli = im.rsplit('/',3) #we get the last 3 element
                subj = spli[-3]+'/'+spli[-2]+'/'+spli[-1]
                to_keep.append(subj)
        else:
            spli = im.rsplit('/',3) #we get the last 3 element
            subj = spli[-3]+'/'+spli[-2]+'/'+spli[-1]
            to_keep.append(subj)

    if len(to_keep)>0:
        f = open(out + '.txt', 'a') # 'a' option allows you to append file to a list. 
        l1 = map(lambda x: x + '\n', to_keep)
        f.writelines(l1)
        f.close()
    else:
        print('No file matching your criteria found')


if __name__ == "__main__":
    main()





