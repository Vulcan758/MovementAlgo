import cv2

# To capture video from webcam.
cap = cv2.VideoCapture(0)

#Print Initial Frame size/property
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

cap.set(3, 1280)
cap.set(4, 720)

#Print Frame Size after capping
print(cap.get(3))
print(cap.get(4))
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
    cv2.line(img, (215, 0), (215, 720), (255, 0, 0), 3)
    cv2.line(img, (430, 0), (430, 720), (255, 210, 0), 3)
    cv2.line(img, (1065, 0), (1065, 720), (255, 0, 0), 3)
    cv2.line(img, (850, 0), (850, 720), (255, 210, 0), 3)

##########################################################################################################

    #DETECT OBJECT HERE AND BRING THE CENTER Upper left point of the object as X and the upper right point as Y
    #Initially Put Custom X & Y for tesing
    x= -1500
    y = 220
    #Draw point for visualize
    cv2.circle(img, (x,y), 1, (255, 0, 255), 5)

    #Conditions
    if x <= 215 and x >= 0:
        print("Rotate Left 15 Degree")
    elif x<=430 and x> 215:
        print("Rotate :eft 5 Degree")
    elif x >= 1065 and x <= 1280:   #Replace x with right top value Y
        print("Rotate Right 15 Degree")
    elif x < 1065 and x >= 850:     #Replace x with right top value Y
        print("Rotate Right 5 Degree")
    elif x > 430 and x < 850:
        print("Go Straight")
    else:
        print("Keep rotating right in very slow speed")




    #Put text for better understanding
    cv2.putText(img, "Turn Right 5 Degree", (885, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 255), 1, cv2.LINE_AA, False)
    cv2.putText(img, "Turn Right 15 Degree", (1100, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 255), 1, cv2.LINE_AA, False)
    cv2.putText(img, "Turn Left 5 Degree", (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 255), 1, cv2.LINE_AA, False)
    cv2.putText(img, "Turn Left 15 Degree", (35, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 255), 1, cv2.LINE_AA, False)
    # Display
    cv2.imshow('img', img)

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release the VideoCapture object
cap.release()