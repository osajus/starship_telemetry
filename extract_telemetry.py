# https://codereview.stackexchange.com/questions/237653/print-numbers-from-video-frames-to-console-using-pytesseract


import pytesseract
import cv2
import time
import multiprocessing as mp
import re

startTime = time.time()

# Video URL
VIDEO_NAME = "ift2.mp4"
extractVideo = cv2.VideoCapture(VIDEO_NAME)
FRAME_COUNT = extractVideo.get(cv2.CAP_PROP_FRAME_COUNT)
reading, frame = extractVideo.read()

# How many parallel processes to use
PARALLEL_PROCESSES = 10

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Frame Number / Rate 
START_FRAME = 0
STOP_FRAME = FRAME_COUNT  # for testing.  Set to 'FRAME_COUNT' if you want to process the whole video

# Do you want to get a data point for every frame or one each second?
#FRAME_RATE = extractVideo.get(cv2.CAP_PROP_FPS)  # One point per second(ish)
FRAME_RATE = 1 # One point per frame

frameList = list(range(START_FRAME, int(STOP_FRAME), int(FRAME_RATE)))

# Output File
outFile = open(((re.sub(r'\.\S+','',VIDEO_NAME)) +".csv"), "w")
outFile.write("Booster_Speed, Ship_Speed, Booster_Altitude, Ship_Altitude, T_Plus, Frame\n")


def process_frame(currFrame):
    # Open the specified frame
    extractVideo.set(1, currFrame)
    reading, frame = extractVideo.read()

    # Bounding boxes for telemetry locations. Format: y1:y2, x1:x2
    bspeed = frame[906:944, 353:519]
    baltitude = frame[943:985, 353:519]    
    sspeed = frame[906:946, 1528:1704]
    saltitude = frame[943:985, 1528:1682]
    tplus = frame[938:992, 900:1071]

    # Generate line of telemetry for CSV
    outText = pytesseract.image_to_string(bspeed, config="--psm 7 -c tessedit_char_whitelist=0123456789") + ","
    outText += pytesseract.image_to_string(sspeed, config="--psm 7 -c tessedit_char_whitelist=0123456789") + ","
    outText += pytesseract.image_to_string(baltitude, config="--psm 7 -c tessedit_char_whitelist=0123456789") + ","
    outText += pytesseract.image_to_string(saltitude, config="--psm 7 -c tessedit_char_whitelist=0123456789") + ","
    outText += pytesseract.image_to_string(tplus, config="--psm 7 -c tessedit_char_whitelist=0123456789:") + ","
    retText = outText.replace("\n", "") + str(currFrame) + "\n"
    return retText



if __name__ == '__main__':  
    print("Processing every", int(FRAME_RATE), "frames, from", START_FRAME, "to", int(STOP_FRAME), "with", PARALLEL_PROCESSES, "Processes:")

    # Add each frame to processor pool
    with mp.Pool(processes=PARALLEL_PROCESSES) as pool:
        results = pool.map(process_frame, frameList)
 
    # Output results to file
    for result in results:
        outFile.write(result)

    # Once everything is done, alert and give runtime statistics
    endTime = time.time()
    print("Done processing frames.  Time(sec): ", round(endTime-startTime,2))
    outFile.close()
