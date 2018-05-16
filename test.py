import aris_utils.file_info as file_info
import aris_utils.frame_info as frame_info
import aris_utils.error_description as err

testingFilePath = "/home/mghobria/Desktop/fish_tracking/sample.aris"

try:
    with open(testingFilePath, 'rb') as testFile:
        print("file loaded")
        print(testFile.read(4)[0])

except:
    print("Error Code: " + str(err.fileReadError[0]))
    print(err.fileReadError[1])
