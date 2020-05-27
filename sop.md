This script is made for manual labeling of BIDS folder

Run the following with python:

python manual-labeling/manual_labeling.py -file list_todo_update.txt -author lucas -path Path_to_duke/ \[-correct 1 -o label_tmp\]

- -file: txt file that contains the list of all images inside bids root folder that you want to process separated by '\n'.The format in sub-xx/anat/sub-xxx_xxx.nii.gz. Can be obtained with get_bids_sub.py.
- -path : Path the Bids root folder (duke) with a '/' at the end
- -author: Author name that will appear on the .json file 
- -correct: Boolean. Default is 0. If correct is 1, the script will look for existing label and open them with the -ilabel option from sct_label_utils so you can verify/correct existing label.
- -o: desired output folder. It will be created if missing. After the task, you will find the file there in BIDS convention sub-xxx/anat/sub-xxx_labels-disc-manual.nii.gz and sub-xxx/anat/sub-xxx_lables-disc-manual.json" if the argument is not use or empty files will be saved in BIDS_PATH/derivatives/labels/sub-xx/anat/xxx

To end the script:
Perform a keyboard interrupt from the terminal (ctrl+c). This will update the list by deleting the viewed subjects. don't forget to commit and push it on github. 

Specific:
suffix to label is labels-disc-manual
The json file contain the name of the label and the name of the author given by the -author args.

Example image for manual labeling:
![example](label_disc_capture.png)
