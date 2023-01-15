import cv2
import serial

# To capture video from webcam.
cap = cv2.VideoCapture(0)

com_port_rover = ""
com_port_imu = ""
baudrate = 9600

rover_arduino = serial.Serial(com_port_rover, baudrate, timeout=1)
imu = serial.Serial(com_port_imu, baudrate, timeout=1)

#Print Initial Frame size/property
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

cap.set(3, 1280)
cap.set(4, 720)

#Print Frame Size after capping
print(cap.get(3))
print(cap.get(4))

def parse_angle_from_IMUdata(data):
    return data

def get_rotations_from_image(x, y, distanceOfTheObject):
    rightArrowCount = 0
    leftArrowCount = 0

    # If distance is more than 1.5m

    if distanceOfTheObject > 1.5: #1.5 in meter

        #Draw point for visualize
        cv2.circle(img, (x,y), 1, (255, 0, 255), 5)

        #Put text for better understanding
        cv2.putText(img, "Turn Right 5 Degree", (885, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 255), 1, cv2.LINE_AA, False)
        cv2.putText(img, "Turn Right 15 Degree", (1100, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 255), 1, cv2.LINE_AA, False)
        cv2.putText(img, "Turn Left 5 Degree", (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 255), 1, cv2.LINE_AA, False)
        cv2.putText(img, "Turn Left 15 Degree", (35, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 255), 1, cv2.LINE_AA, False)


        #Conditions
        if x <= 215 and x >= 0:
            print("Rotate Left 15 Degree")
            return 15, "ccw"
        elif x<=430 and x> 215:
            print("Rotate Left 5 Degree")
            return 5, "ccw"
        elif x >= 1065 and x <= 1280:   #Replace x with right top value Y
            print("Rotate Right 15 Degree")
            return 15, "cw"
        elif x < 1065 and x >= 850:     #Replace x with right top value Y
            print("Rotate Right 5 Degree")
            return 5, "cw"
        elif 430 < x < 850:
            print("Go Straight")
            return 0, "forward"
        else:
            print("Keep rotating right in very slow speed")
            #after completing a full 360 degree rotation, the rover will move forward 1m and then rotate 360 degree again.
            return 0, "not found"


    elif distanceOfTheObject > 1 and distanceOfTheObject < 1.5:     #in meter
         #go forward for 50 cm
         #Give a pause of 10 second
         #Detect camera orientation
        #if right arrow:
        rightArrowCount +=1
        if rightArrowCount == 1:
            print("Rotate Right 90 degree")
            #Rotate 90 degree Right
            #Go forward 1m
            return 90, "cw"
        if leftArrowCount == 1:
            print("Rotate Left 90 degree")
            #Rotate 90 degree Left
            # Go forward 1m
            return 90, "ccw"

def rotate(degrees, direction):
    state = True
    current_angle = parse_angle_from_IMUdata(imu.readline())
    while state:
        new_current_angle = parse_angle_from_IMUdata(imu.readline())
        if new_current_angle > current_angle + degrees - 2 and new_current_angle < current_angle + degrees + 2:
            rover_arduino.write(bytes("stop", "utf-8"))
            state = False
        else:
            #rover_arduino.write(bytes(str(degrees) + "|" + direction, "utf-8"))
            rover_arduino.write(bytes(direction, "utf-8"))


while True:
    # Read the frame
    _, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    #faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw the rectangle around each face
    #for (x, y, w, h) in faces:
        #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #Draw Lines for screen separation
    cv2.line(img, (215, 0), (215, 720), (255, 0, 0), 1)
    cv2.line(img, (430, 0), (430, 720), (255, 210, 0), 1)
    cv2.line(img, (1065, 0), (1065, 720), (255, 0, 0), 1)
    cv2.line(img, (850, 0), (850, 720), (255, 210, 0), 1)

##########################################################################################################

    #DETECT OBJECT HERE AND BRING THE CENTER Upper left point of the object as X and the upper right point as Y
    #Initially Put Custom X & Y for tesing
    x= 150
    y = 220
    distanceOfTheObject = 3

    degrees, dir = get_rotations_from_image(x, y, distanceOfTheObject)
    rotate(degrees, dir)

        #Display
    cv2.imshow('img', img)

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release the VideoCapture object
cap.release()
