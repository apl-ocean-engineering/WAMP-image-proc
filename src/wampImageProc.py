#!/usr/bin/env python2.7
"""
Created on Wed Nov 14 16:07:34 2018

@author: Mitchell Scott
@contact: miscott@uw.edu
"""
import glob
import cv2
import numpy as np
import os
import sys
import signal


class wampImageProc:
    """
    Class containign modules to help process WAMP image data
    
    Attributes:
        -root_dir (str): Location of root directory
        -sub_directories (list<str>): List of all subdirectories containing 
        -images H (np.mat): Linear transformation matrix between images
        
    Methods:
        -image_overlap: Check overlap between stereo images
        -background_subtraction: Runs openCv createBackgroundSubtractorMOG2 alg.
        -VPS: Runs Video Peak Source algorithm
        -get_hour: Determines hour from full image/folder name
    """
    def __init__(self, root_dir = " ", affine_transformation = " ", 
                                     hour_min = 0.0, hour_max = 24.0):
        """
        Args:
            [root_dir(string)]: Location of the root directory where images are
            [affine_transformation(str)]: Path to file containing affine_tranformation
            [hour_min(float)]: Minimium hour to consider images. Images which
                are below this amount will be discarded
            [hour_max(float)]: Maximium hour to consider images. Images which
                are above this amount will be discarded
        ValueError:
            If the wampImageProc is initated such that no directories and 
            images are found, a ValueError will be raised
        """
        if root_dir == " ":
            self.root_dir = os.getcwd()
        else:
            self.root_dir = root_dir
            
        self.hour_min = hour_min
        self.hour_max = hour_max
        self.triggers_exist = os.path.exists(self.root_dir + "/Triggers.txt")
        
        
        #Affine transformation
        if affine_transformation == " ":
            self.H = np.array([[8.10993053*10**-1,1.27196567*10**0,-1.10498100*10**3], 
                               [-.77104618*10**-1,8.67541888*10**-1,3.28146455*10**2]])       
        else:
            file = open(affine_transformation, "r") 
            self.H = np.array(file.read().split(',')[0:6], dtype=np.float32).reshape((2,3))
    
        self.sub_directories = self._subdirs()
        if self.sub_directories == []:
            raise ValueError("There are no images which satisfy the input format")
        

    def image_overlap(self, display_images = False, display_overlap = False):
        """
        Check the overlap of images, check image intensity
        Inputs:
            [display_images(bool)]: Display the images
            [display_overlap(bool)]: Display the overlap between transformed images
        Returns:
            None
        """            
        for subdir in self.sub_directories:
            #subdir is a string
            #Call self._background_subtraction with overlap on
            overlap_intensity = self._background_subtraction(subdir + "Manta 1/*.jpg", 
                subdir + "Manta 2/*.jpg", overlap = True, 
                display_images = display_images, 
                display_overlap= display_overlap)    
        return overlap_intensity
            
    def background_subtraction(self, display_images = False):
        """
        Run a background subtraction algorithm on all images in desired directory
        
        Input:
            [display_images(bool)]: Display the images
        Return:
            None
        """            
        for subdir in self.sub_directories:
            #subdir is a string
            #Call self._background_subtraction. Return value is Null
            self._background_subtraction(subdir + "Manta 1/*.jpg", 
                    subdir + "Manta 2/*.jpg", display_images = display_images)                

    def get_hour(self, name):
        """
        Convert from folder name type to hour in 24-hour format
        
        Input:
            name (str): Input in form YYYY_MM_DD hh_mm_ss
        Return:
            Hour (int): Hour in 0-24 hour form
        """
        full_time = name.split(" ")
        hour = full_time[1].split("_")[0]
               
        return int(hour)    
          
    
    def _subdirs(self):
        """
        Returns list of subdirectories under main directory which satisifes
        the time constraint 
        
        Input:
            None
        Return:
            return_subdirs(list<str>): List of all subdirectories which satisfy
                                       input paramaters
        """
        #Get list of all folders in the current directory
        all_subdirs = self._get_paths(self.root_dir + "/*/")
        #Only return sub directories that contain images, i.e. begin with 2018
        return_subdirs = []
        for path in all_subdirs:
            names = path.split('/')
            #all folders start with 2018. If a folder starts with 2018, append
            #to return list
            folder_name = names[len(names) - 2]
            if folder_name[0:4] == "2018":
                hour = self.get_hour(names[len(names) - 2])
                if hour > self.hour_min and hour < self.hour_max:
                    return_subdirs.append(path)
        
        return return_subdirs    

        
    def _get_paths(self, directory):
        """
        Get list of all files and folders under a specific directory satisfying
        the input form
        
        Input:
            directory (str): Name of directory in which files should be, PLUS 
            the file type, if desired. Must have '*' symbol were searchign will 
            take place. It will return all files that fit the
            specified format, filling in for the '*'
            
            Example 1: path + *.jpg will return all .jpg files in the location
            specified by path
            
            Example 2: path + */ will return all folders in the location 
            specified  by oath
            
            Example 3: path + * will return all folders AND files in the 
            location specified by path
            
        Return:
            paths (list<strs>): List of strings for each file/folder which 
            satisfies the in input style.
            Empty list if no such file/folder exists
        """
        paths = sorted(glob.glob(directory))
        return paths
    
    def _background_subtraction(self, d1, d2, overlap = False, display_images = False, display_overlap=False):
        """
        Run background subtraction algorithm using openCv 
        createBackgroundSubtractorMOG2. Will do background subtraction for all
        images in d1 and d2 (directories 1 and 2, respectively). d1 and d2
        inputs should be the directories where each of the stereo camera iamges 
        are located.
        
        The function will also claculate overlap, if desired, and return the 
        intensity of the image(s) overlap. Image one's frame will be transformed 
        into image one's frame and will check for overlap. If false, return 
        empty list
        
        Input:
            d1(str): Directory 1 containing images (i.e subdir + Manta 1)
            d2(str): Directory 2 containing images
            [overlap(bool)]: Calcuate image overlap
            [display_images(bool)]: Display images
            [display_overlap(bool)]: Display overlapped image
        Return:
            overlap_intensity(list<float>): List of all image intensities
        """
        #get list of all images from current directory
        images1 = self._get_paths(d1)
        images2 = self._get_paths(d2)
        #create a background subtraction object
        fgbg1 = cv2.createBackgroundSubtractorMOG2()
        fgbg2 = cv2.createBackgroundSubtractorMOG2()
        #zip images so that we can loop through image names
        images = zip(images1, images2)
        #initialize window size
        if display_images:
            cv2.namedWindow('frame1', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame1', 800,800) 
            cv2.namedWindow('frame2', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame2', 800,800) 
        if display_overlap:
            cv2.namedWindow('overlap', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('overlap', 800,800)    
        if display_overlap or display_images:
            print("To exit, press cntrl + c")
        #Create list of image_intensity
        overlap_intensity = []
        #Kernel for median blur
        kernel = np.ones((5,5),np.uint8)
        for fname1, fname2 in images:
            """
            Loop through all image frames and run background subtraction.
            If overlap is selected, compare the overlap between the two images
            """
            signal.signal(signal.SIGINT, self._sigint_handler)
            #Read images and inport
            img1 = cv2.imread(fname1)
            img2 = cv2.imread(fname2)
            #Apply the mask
            fgmask1 = fgbg1.apply(img1)
            fgmask2 = fgbg2.apply(img2)
            #Apply a median blur to reduce noise
            blur1 = cv2.medianBlur(fgmask1, 3)
            blur2 = cv2.medianBlur(fgmask2, 3)
            #Display images
            if display_images:
                cv2.imshow('frame1',blur1)
                cv2.imshow('frame2',blur2)
                #If cntrl + c, exit          
            if overlap:
                #Transform image one by an affine transformation
                blur1_trans = cv2.warpAffine(blur1, self.H, 
                                (blur1.shape[1],blur1.shape[0]))
                #Dilate the images
                blur1_trans_dilate = cv2.dilate(blur1_trans,kernel,iterations = 1)
                blur2_dilate = cv2.dilate(blur2,kernel,iterations = 1)
                #Check Overlap between images using bitwise_and
                overlap_img = np.bitwise_and(blur1_trans_dilate, blur2_dilate)
                if display_overlap:
                    cv2.imshow('overlap', overlap_img)
            #If cntrl+c is pressed, exit
            if display_images or display_overlap:
                k = cv2.waitKey(1)
                if k == 99:
                    cv2.destroyAllWindows()
                    sys.exit()  
                    
        #Return list of overlap intensities or empty list
        return overlap_intensity
    
    def _sigint_handler(self, signum, frame):
        """
        Exit system if SIGINT
        """
        sys.exit()
        
class image_transform:
    """
    Class to help determine transformation between frames in two WAMP cameras
    
    Attributes:
        -Images_path(str): Path to directory containing images for calibration
        -x#_points, y#_points (list<float>): 4 lists containing corresponding
            points in each camera frame
        -image1, image2 (np.mat<float>): Images
        -m1_subdirectories, m2_subdirectories (list<str>): List 
            containing image paths
    Methods:
        -corresponding_image_points: Manual correspondance of points between 
            two image frames
        -find_perspective: Calculates the perspective transform matrix
        -find_homography: Calculates the homography transform matrix
        -find_affine: Calculates the affine transform matrix
        -get_points: Returns corresponding image points between the two frames
        
    """
    def __init__(self, images_path):
        """
        Args:
            images_path(str): Path pointing to location of images
        """
        self.images_path = images_path
        self.x1_points = []
        self.y1_points = []
        self.x2_points = []
        self.y2_points = []
        self.image1 = np.zeros([0,0])
        self.image2 = np.zeros([0,0])
        
        self.m1_subdirectories, self.m2_subdirectories = self._subdirs()
        
    def corresponding_image_points(self):
        """
        Determine coressponding image points between the frames
        
        Will display two WAMP images. User must click on identical point
        in two frames. x#_points, and y#_points will populate as the user 
        clicks on points            
        """
        #Initalzie image windows
        cv2.namedWindow('image1', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image1', 1200,1200)
        cv2.namedWindow('image2', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image2', 1200,1200)
        #Define mouse callback functions
        cv2.setMouseCallback('image1',self._mouse_click1)
        cv2.setMouseCallback('image2',self._mouse_click2)
        #Loop through all images in subdirectory location
        print("Click on the same point in both images")
        print("Press enter to move to next corresponding images")
        print("Press 'f' to finish")
        print("Press cntrl+c to quit")
        for i in range(0, len(self.m1_subdirectories)):
            signal.signal(signal.SIGINT, self._sigint_handler)
            #Get img1 and img2 from the subdirectories
            f1, f2 = self.m1_subdirectories[i], self.m2_subdirectories[i]
            self.img1, self.img2 = cv2.imread(f1), cv2.imread(f2)
            #Show images
            cv2.imshow('image1', self.img1)
            cv2.imshow('image2', self.img2)
            #Press 'enter' to move on, f to finish, cntrl+c to quit
            k = cv2.waitKey(0)
            if k == 99:
                cv2.destroyAllWindows()
                sys.exit()  
            if k == 102:
                cv2.destroyAllWindows()
                break            
        cv2.destroyAllWindows()
        
    def find_perspective(self, save = False, path=""):
        """
        Calculate perpsective transformation matrix from corresponding points
        
        NOTE: Must be exactly 4 points, or error will raise
        
        Args:
            [save(bool)]: If the data should be saved or not
            [path(str)]: Path to save, is desired
        
        Return: 
            perspective_transform (np.mat<float>): (3X3) transformation matrix    
        """
        #Get corresponding points
        pnts1, pnts2 = self._image_points()
        if len(pnts1)!=4 or len(pnts2)!=4:
            raise ValueError("Must have exactly four corresponding image points")
        #Get transform
        perspective_transform = cv2.getPerspectiveTransform(pnts1, pnts2)
        if save:
            #Save data to text file
            np.savetxt(path+"perspective_transform.txt", 
                       perspective_transform.reshape(1,9), delimiter=',', fmt="%f") 
        
        return perspective_transform
    
    def find_homography(self, save = False, path =""):
        """
        Calculate homography transformation matrix from corresponding points
        
        Should use at least four points to be accruate
        
        Args:
            [save(bool)]: If the data should be saved or not
            [path(str)]: Path to save, is desired
        
        Return: 
            homography_transform (np.mat<float>): (2X3) homography matrix
        """
        #Get corresponding points
        pnts1, pnts2 = self._image_points()
        #Get transform
        homography_transform = cv2.findHomography(pnts1, pnts2)
        
        if save:
            #Save data to text file
            np.savetxt(path+"homography_transform.txt", 
                       homography_transform.reshape(1,6), delimiter=',', fmt="%f")         
        
        return homography_transform   

    def find_affine(self, save=False, path = ""):
        """
        Calculate affine transformation matrix from corresponding points
        
        NOTE: Must be exactly 3 points, or error will raise
        
        Args:
            [save(bool)]: If the data should be saved or not
            [path(str)]: Path to save, is desired
        
        Return: 
            homography_transform (np.mat<float>): (2X3) homography matrix
        """     
        #Get corresponding points
        pnts1, pnts2 = self._image_points()
        if len(pnts1)!=3 or len(pnts2)!=3:
            raise ValueError("Must have exactly three corresponding image points")   
        #Get affine transform
        affine_transform = cv2.getAffineTransform(pnts1, pnts2)
        
        if save:
            #Save data to text file
            np.savetxt(path+"affine_transform.txt", 
                       affine_transform.reshape(1,6), delimiter=',', fmt="%f") 
            
        return affine_transform          
        
    def get_points(self):
        """
        Return corresponding image points
        
        Return:
            points1, points2 (list<tuple<float>>): Corresponding points
        """
        points1, points2 = self._image_points()

        return points1, points2
    
            
    def _image_points(self):
        """
        Organize image points into two lists of corresponding tuples
        
        Return:
            pnts1, pnts2 (list<tuple<float>>): Corresponding points
        """
        #Check that points clicked are equal
        if len(self.x1_points) != len(self.x2_points):
            raise AttributeError("Unequal Points Clicked")
        #Organize points
        pnts1 = []
        pnts2 = []
        for i in range(0, len(self.x1_points)):
            pnts1.append((self.x1_points[i], self.y1_points[i]))
            pnts2.append((self.x2_points[i], self.y2_points[i]))
        #Must be float 32s to work in OpenCV
        pnts1 = np.float32(pnts1)
        pnts2 = np.float32(pnts2)  
        
        return pnts1, pnts2
        
    def _mouse_click1(self,event,x,y,flags,param):
        """
        Callback function for mouse click event on image1 frame
        
        Places clicked points into x1_ and y1_points lists
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x1_points.append(x)
            self.y1_points.append(y)
            #Draw circle where clicked
            cv2.circle(self.img1,(x,y), 20, (255,255,255), -1)
            cv2.imshow('image1', self.img1)
    
    def _mouse_click2(self,event,x,y,flags,param):
        """
        Callback function for mouse click event on image2 frame
        
        Places clicked points into x2_ and y2_points lists
        """        
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x2_points.append(x)
            self.y2_points.append(y)
            #Draw circle where clicked
            cv2.circle(self.img2,(x,y), 20, (255,255,255), -1)
            cv2.imshow('image2', self.img2)
    
    def _subdirs(self):
        """
        Return list of all subdirectories under current directory containing
        the Manta 1 and Manta 2 images
        
        Return:
            -manta1_subdirs, manta2_subdirs (list<str>): Paths for all images
        """
        #Get list of all folders in the current directory
        manta1_subdirs = glob.glob(self.images_path + "/Manta 1/*.jpg")
        manta2_subdirs = glob.glob(self.images_path + "/Manta 2/*.jpg")
        
        return manta1_subdirs, manta2_subdirs
    
    def _sigint_handler(self, signum, frame):
        """
        Exit system if SIGINT
        """
        sys.exit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        