Some tips to help navigate the bizare world of vision.

-- visionwrapper.py

    Contains (so far) the main class for executing vision. 
    A lot of funcitonality needs to be implemented for logic and
    object determination, refer to TODO comments.

-- findHSV.py <pitch> <color>
    
    In calibrations.json adjustments to various camera settings will be saved for <pitch> and <color>
    so that tracker can locate <color> object(s).

    If a new color needs to be added, copy-paste one of the colors in calibrations.json and change the name, then
    launch the program and adjust settings.

    NOTE: according to manual, blur value have to be odd...

-- vision.py
    
    Currently the main class for viewing all tracking and calibrated result. Namely <Camera> object handles the camera
    capture and returns calibrated frame.

-- preprocessing/distortion/undistort.py
    
    File for fixing camera distortion. Simply launch it after specifying the 
    txt file where to save the data and file, where the images are stored.
    Then use tools.get_radial_data(pitch, filename) to get the data. There
    is a function in vision.py->Camera class called fix_radial_distortion,
    that uses the data.

-- vision/calibrate.py <pitch>

    Calibrate camera cropping. Not used.

-- vision/perspective_calibrate.py <pitch>

    Fix perspective of the camera and save it to calibrations/perspective.json.
    Function in vision->Camera uses it in function fix_perspective(frame).
    To use, start the program by givin pitch number as argument, then place 
    four points starting fromtop left and going clockwise. Each point will be stretched
    to the corner.

-- vision/my_tracker.py <pitch>

    Some object detection features bundled together to get a generic detector
    which can detect multiple color multiple objects. Pass a color array to
    MyTracker along with calibration file, that contains colour calibrations 
    for that pitch. Color calibration plays the main role in ability to
    detect objects. MyTracker.get_points() returns points saved after
    MyTracker.track(frame) is executed. Points are returned in a dictionary 
    fashion -> {'red' => [(1,2), (5,6)]} would mean that two objects
    of red color were found in (x,y) position relative to the frame.

-- vision/test_tracker.py <pitch>
    
    Object detection using group 8 method. Plate areas are detected by combining several 
    colour masks and color gradients are measured to determine robot team, group, position 
    and direction. Main method test_tracker.get_world_state(image) returns a dictionary of 
    the form:

    {'ball': {'center': (0, 0), 'radius': 0, 'direction':(0,0)}, 'robots': []}
    
    where eatch robot:

    {'center': (cx, cy), 'angle': angle, 'team': team, 'group': group}

    NOTE: color masks depend on each other. Violet and red masks combine into one ball
    mask, but violet mask often includes pink, so robot plate masks are subtracted from ball mask.
    Because of that, non of robot plate calibrations ('plate','pink') can include the ball in them.
