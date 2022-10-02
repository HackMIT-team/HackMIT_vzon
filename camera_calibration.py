import numpy as np
import cv2 
import glob
import os











def get_corner_point():

    
    good_images = 0
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("img")
    img_counter=0
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob('opencv_frame_*.jpeg')
    run = True 
    while run:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame") 
                break
        
            img_name = "open_cv_{}.jpeg".format(img_counter)
            img_counter+=1
            cv2.imwrite(img_name, frame)
            print("__________________________________________________________________________________________________")
            print('Reading frame')
            print("__________________________________________________________________________________________________")
            img = cv2.imread(img_name)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            ret_1, corners = cv2.findChessboardCorners(gray, (7,6), None)
            if ret_1 == True and good_images<14:
                good_images+=1
                print("###############################################################################################")
                print('Found a frame for calibration , {} more to go'.format(14-good_images))
                print ("Displaying calibration output..............")
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners)
                # Draw and display the corners
                cv2.drawChessboardCorners(img, (7,6), corners2, ret_1)
                cv2.imshow('img', img)
                cv2.waitKey(5000)
                
                print("###############################################################################################")
            try:
                os.remove(img_name)
            except:
                continue
                
            if good_images>=14:
                try:
                    f= open('intrinsicNew.npy','wb')
                    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
                    np.save(f,mtx)
                    print("Camera calibration completed succesfully")
                    f.close()
                except:
                    pass
                run = False
            
            
    cv2.destroyAllWindows()

get_corner_point()