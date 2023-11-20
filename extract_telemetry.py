# https://codereview.stackexchange.com/questions/237653/print-numbers-from-video-frames-to-console-using-pytesseract

import pytesseract
import cv2

# Video URL
VIDEO_NAME = "ift2.mp4"
EXTRACT_VIDEO = cv2.VideoCapture(VIDEO_NAME)
FRAME_COUNT = EXTRACT_VIDEO.get(cv2.CAP_PROP_FRAME_COUNT)
FPS = EXTRACT_VIDEO.get(cv2.CAP_PROP_FPS)
READING, IMG = EXTRACT_VIDEO.read()

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Frame Number / Rate 
CURR_FRAME = 0
STOP_FRAME = 1050
# To save time, set frame rate to process one per second, set to 29.  If not, set to 1
FRAMERATE = 1

# Output File
outfile = open((VIDEO_NAME+".csv"), "w")
outfile.write("Booster_Speed, Ship_Speed, Booster_Altitude, Ship_Altitude, T_Plus, Frame\n")

while READING:
    CURR_FRAME += 1
    
    # Terminate early (for testing)
    # if (CURR_FRAME > STOP_FRAME):
    #     outfile.close()
    #     break

    if (CURR_FRAME % FRAMERATE != 0):
        continue
    
    print(str(CURR_FRAME) + "/" + str(FRAME_COUNT))

    EXTRACT_VIDEO.set(1, CURR_FRAME)
    READING, IMG = EXTRACT_VIDEO.read()
    RET, FRAME = EXTRACT_VIDEO.read()

    # y1:y2, x1:x2
    bspeed = FRAME[906:944, 353:519]
    baltitude = FRAME[943:985, 353:519]
    
    sspeed = FRAME[906:946, 1528:1704]
    saltitude = FRAME[943:985, 1528:1682]

    tplus = FRAME[938:992, 900:1071]


    # Write speed
    outtext = pytesseract.image_to_string(bspeed, config="--psm 7 -c tessedit_char_whitelist=0123456789")
    outfile.write(outtext.replace("\n", "") + ",")
    
    outtext = pytesseract.image_to_string(sspeed, config="--psm 7 -c tessedit_char_whitelist=0123456789")
    outfile.write(outtext.replace("\n", "") + ",")

    # Write altitude
    outtext = pytesseract.image_to_string(baltitude, config="--psm 7 -c tessedit_char_whitelist=0123456789")
    outfile.write(outtext.replace("\n", "") + ",")

    outtext = pytesseract.image_to_string(saltitude, config="--psm 7 -c tessedit_char_whitelist=0123456789")
    outfile.write(outtext.replace("\n", "") + ",")


    # Write tplus time
    outtext = pytesseract.image_to_string(tplus, config="--psm 7 -c tessedit_char_whitelist=0123456789:")
    outfile.write(outtext.replace("\n", "") + ",")

    # Write current frame
    outfile.write(str(CURR_FRAME) + "\n")


outfile.close()
