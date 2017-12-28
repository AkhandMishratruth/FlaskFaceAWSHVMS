# Author : Julien Simon <julien@julien.org>, 29/10/2016
# Disclaimer : this is for educational purposes only.
# If this script destroys your infrastructure, sets your car on fire
# or breaks your marriage, it's all your fault, not mine.

import boto3, time

def copyLocalFileToS3(filename, bucketName):
    boto3.client('s3').upload_file(filename, bucketName, filename)
t1 = time.time()
copyLocalFileToS3("shj.jpg", "tempReco")
t2=time.time()
print "Uploading time " + str(t2-t1)