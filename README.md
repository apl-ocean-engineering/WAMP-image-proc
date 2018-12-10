# WAMP-image-proc
Image processing for the iamges taken from the Hawaii AMP.

## Requirments
Python2  
OpenCv  
Numpy  

## Installation
To install, clone package into desired directory  

## Codebase
The main Python module is the wampImageProc.py file, which provides high-level functionality for processing WAMP image data. This module can process all WAMP images and check for correspondance between camera frames, provided you provide a base_path which points to the WAMP folder. The file image_proc.py shows an example setup using this module, ** but verify that the path (base_folder on line 26) is properly set ** or the script will not run.  

There are also a few other example scripts that were used to help determine camera properties. image_intensity.py will determine the intensity of all images within the root_folder. affine_transformation.py will calculate an affine transformation between the two images, using a specified image. triggered_events.py will display all photos specified by trigger_events.py.  

## Running the code
The python script image_proc.py will traverse over all images specified by the base_folder and search for high_trigger images which also correspond to sonar triggers. It could save all high_trigger events to a specified folder if desired. To run in Linux, run  ./image_proc.py. To save high trigger events, run as: ./image_proc.py \[SaveTriggers (bool)\] \[SaveOverlap (bool)\] \[SavePath (string)]. For example, running as ./image_proc.py True True /home/mitchell will save the file high_value.txt and overlap.txt to my /home/mitchell folder. high_value.txt contains path locations where both sonar and cameras are triggered and overlap.txt has the overlap intensity of all stereo images traversed.   

## To Do
Better documenation and user interfacing... 


