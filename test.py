import cv2
import sys
import logging as log
import datetime as dt
from time import sleep

fromFile = sys.argv[1]

videoPath = "videoplayback.mp4"
faceCascPath = "haarcascade_frontalface_default.xml"
smileCascPath = "haarcascade_smile.xml"
eyeCascPath = "haarcascade_eye.xml"

faceCascade = cv2.CascadeClassifier(faceCascPath)
# smileCascade = cv2.CascadeClassifier(smileCascPath)
eyeCascade = cv2.CascadeClassifier(eyeCascPath)

if fromFile == 'fromFile':
    video_capture = cv2.VideoCapture(videoPath)

    while (video_capture.isOpened()):
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, frame = video_capture.read()

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            eyes = eyeCascade.detectMultiScale(roi_gray)

            for (ex, ey, ew, eh) in eyes:
                newx = ex + x
                newy = ey + y


                # crop_out = cv2.rectangle(ex, ey, ew, eh)

                print ex, ey, ew, eh

                roi_eye = frame[y:newy + eh, x:newx + ew]

                print roi_eye

                roi_eye = cv2.GaussianBlur(roi_eye, (23, 23), 30)

                print roi_eye

                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
                frame[y:newy + eh, x:newx + ex] = roi_eye


        # Display the resulting frame
        cv2.imshow('Video', frame)
    video_capture.release()
    cv2.destroyAllWindows()
else:
    log.basicConfig(filename='webcam.log', level=log.INFO)

    video_capture = cv2.VideoCapture(0)
    anterior = 0

    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(5)
            pass

        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            eyes = eyeCascade.detectMultiScale(roi_gray)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

        if anterior != len(faces):
            anterior = len(faces)
            log.info("faces: " + str(len(faces)) + " at " + str(dt.datetime.now()))

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Display the resulting frame
        cv2.imshow('Video', frame)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
