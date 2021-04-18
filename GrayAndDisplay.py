import threading, cv2, base64, queue
import numpy as np
from QueueClass import queueClass


def extractFrames(fileName, extractionFrames, maxFramesToLoad=9999):
    
    count = 0 # Initialize frame count
    vidcap = cv2.VideoCapture(fileName) # Opens video file
    success,image = vidcap.read() # This reads first image
    print('Reading frame: ' , count, ' ', success) 
    
    while success and count < maxFramesToLoad:
        extractionFrames.put(image) # This adds the frame to the buffer
        success,image = vidcap.read() 
        print('Reading frame: ' , count, ' ', success)
        count += 1 # Adding to the count

    print('Frame extraction complete')
    extractionFrames.markEnd()


def convertToGrayScale(extractionFrames, conversionFrames):
    count = 0
    while True and count < 72:
        print('Converting frame: ', count)
        frame = extractionFrames.get() # Attain the frames
        if frame == 'end': # If we see the mark
            break # Exits the loop

        greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY ) # Frames to grey
        conversionFrames.put(greyFrame) # Puts in the queue
        count += 1 # Increments

    print('Frame Conversion complete')
    conversionFrames.markEnd()


def displayFrames(inputBuf):
    count = 0
    while True:
        frame = inputBuf.get() # Gets a frame
        if frame == 'end':
            break # End the while loop

        print('Displaying frame: ', count)
        cv2.imshow('Video', frame) # Show the frame image
        if cv2.waitKey(42) and 0xFF == ord('q'): # Wait for 42 ms
            break
        count += 1

    print('Finished Displaying')
    cv2.destroyAllWindows()


file_name = 'clip.mp4' # This is the file name that we will be using to read and display
extractionQueue = queueClass() # Creating the extraction queue by using the queue class
conversionQueue = queueClass() # Creating the conversion queue by using the queue class


#extract and convert
extractThread = threading.Thread(target = extractFrames, args = (file_name, extractionQueue, 72)) # Threading for extraction frames
conversionThread = threading.Thread(target = convertToGrayScale, args = (extractionQueue, conversionQueue)) # Threading to convert the extracted frames

# Display the converted frames
displayThread = threading.Thread(target = displayFrames, args = (conversionQueue,)) # Threading to display frames


# Begin the thread
extractThread.start()
conversionThread.start()
displayThread.start()
