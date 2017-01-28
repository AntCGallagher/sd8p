#from communications.communications import Comms

"""
This script will be used to run a few trials to test the robot's functionalities.
"""
if __name__ == "__main__" :
    inp = ""
    while inp != "END":
        inp = raw_input("Trial to run:")
        if inp == "":
            inp = lastinp
        else:
            lastinp = inp
        if inp == "1":
            print "1 running"
        elif inp == "2":
            print "2 running"
