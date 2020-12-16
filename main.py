from Extract_frames import video
from image_processing import process, sort
from config import Config

import os



vid = video('Video/1min.mp4')

for frame in video:
    extracted_values = process(frame)
    sorted_extract = sort(extracted_values)

    if os.path.isfile('output/values.csv'):
        os.system('rm output/values.csv')
    os.system('touch output/values.csv')

    with open('output/values.csv', 'a') as file:
        file.write(sorted_extract)


#main code will be looping through the frames of the video
#Then, get each frame, call function that applies filters and
#returns the values that are needed in the right format
#Then calls a function that will print the thing onto csv? not too sure :)
#Perform stuff
