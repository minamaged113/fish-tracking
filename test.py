import aris_utils.file_info as file_info

import aris_utils.error_description as err

testingFilePath = "/home/mghobria/Desktop/fish_tracking/sample.aris"

file1 = file_info.ARIS_File(testingFilePath)
version = file1.fileVersion()
print(version)
