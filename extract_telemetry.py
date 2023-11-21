# https://codereview.stackexchange.com/questions/237653/print-numbers-from-video-frames-to-console-using-pytesseract


import pytesseract
import cv2

# Video URL
VIDEO_NAME = "ift2.mp4"
extractVideo = cv2.VideoCapture(VIDEO_NAME)
FRAME_COUNT = extractVideo.get(cv2.CAP_PROP_FRAME_COUNT)
reading, frame = extractVideo.read()

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Frame Number / Rate 
currFrame = 0
STOP_FRAME = 0  # for testing.  Set to 0 if you want to process the whole video

# Do you want to get a data point for every frame or one each second?
#FRAME_RATE = int(extractVideo.get(cv2.CAP_PROP_FPS))  # One point per second(ish)
FRAME_RATE = 1 # One point per frame


# Output File
outFile = open((VIDEO_NAME+".csv"), "w")
outFile.write("Booster_Speed, Ship_Speed, Booster_Altitude, Ship_Altitude, T_Plus, Frame\n")

while reading:
    currFrame += 1
    
    #Terminate early (for testing)
    if (STOP_FRAME != 0 and currFrame > STOP_FRAME):
        outFile.close()
        break

    if (currFrame % FRAME_RATE != 0):
        continue
    
    print("Processing frame: " + str(currFrame) + "/" + str(FRAME_COUNT), end='\r')

    extractVideo.set(1, currFrame)
    reading, frame = extractVideo.read()

    # y1:y2, x1:x2
    bspeed = frame[906:944, 353:519]
    baltitude = frame[943:985, 353:519]    
    sspeed = frame[906:946, 1528:1704]
    saltitude = frame[943:985, 1528:1682]
    tplus = frame[938:992, 900:1071]

    # Write speed
    outText = pytesseract.image_to_string(bspeed, config="--psm 7 -c tessedit_char_whitelist=0123456789") + ","
    outText += pytesseract.image_to_string(sspeed, config="--psm 7 -c tessedit_char_whitelist=0123456789") + ","
    outText += pytesseract.image_to_string(baltitude, config="--psm 7 -c tessedit_char_whitelist=0123456789") + ","
    outText += pytesseract.image_to_string(saltitude, config="--psm 7 -c tessedit_char_whitelist=0123456789") + ","
    outText += pytesseract.image_to_string(tplus, config="--psm 7 -c tessedit_char_whitelist=0123456789:") + ","
    outFile.write(outText.replace("\n", "") + str(currFrame) + "\n")

print("", flush=True)
print("Done processing frames")
outFile.close()
