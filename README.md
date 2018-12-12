# WAMP-image-proc
Image processing for the iamges taken from the Hawaii AMP.

## Requirments
Python2  
OpenCv for python2 (```$pip install opencv-python``` will work for most distributions)  
Numpy (full SciPy information here: [https://www.scipy.org/install.html])   

## Installation
Installation has been tested on an Ubuntu 18.04 OS, should work for most OS's.  

Navigate to installation path and clone:  
```
$ cd <path_to_install_directory>  
$ git clone https://github.com/apl-ocean-engineering/WAMP-image-proc.git  
```
Remember to document issues.  

## Contribution
Add a pull request to contribute to the codebase.  

## Codebase
The main Python module is the wampImageProc.py file, which provides high-level functionality for processing WAMP image data. This module can process all WAMP images and check for correspondance between camera frames, provided you provide a base_path which points to the WAMP folder. The file image_proc.py shows an example setup using this module, **but verify that the path (base_folder on line 26) is properly set** or the script will not run.  

There are also a few other example scripts that were used to help determine camera properties. image_intensity.py will determine the intensity of all images within the root_folder. affine_transformation.py will calculate an affine transformation between the two images, using a specified image. triggered_events.py will display all photos specified by trigger_events.py.  

## Running the code
The python script image_proc.py will traverse over all images specified by the base_folder and search for high_trigger images which also correspond to sonar triggers. It will (optinally) save trigger and overlap data to folder <path_to_WAMP-image-proc>/data. To run in Linux, run:
```
$ ./image_proc.py [--help][--save_trigger_data bool (default False)][--save_overlap_data bool (default False)]
```    

Example 1:
```
$./image_proc.py --save_triggers_data True --save_overlap_data True  
```
Will run the code and save triggers and overlap information to /data.  


