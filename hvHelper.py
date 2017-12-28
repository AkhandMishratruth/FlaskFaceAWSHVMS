import os, boto3, time, sys, requests, yaml

appId = os.environ.get("appId")
appKey = os.environ.get("appKey")

baseUrl = "http://54.208.145.18"

def formData(filePaths):
    files = {}
    fileName = os.path.basename(os.path.normpath(filePaths))
    #print "_________________________"
    #print filePaths
    #print fileName
    files[fileName] = open(filePaths, 'rb')
    return files

def faceRecognize(imagePaths, groupId, batchSize):
    """Uploading facecrops and recognizing face"""
    url = baseUrl + "/v2/photo/recognize"
    response = None
    imagePathsBatch = []
    '''
    for i in xrange((len(imagePaths) + batchSize - 1) / batchSize):
        if (i + 1) * batchSize > len(imagePaths):
            imagePathsBatch = imagePaths[i * batchSize:]
        else:
            imagePathsBatch = imagePaths[i * batchSize: (i + 1) * batchSize]
            
        uploadingStart=time.time()
        sys.stdout.write("\r Uploading " +
                         str(i + 1) + "/" +
                         str((len(imagePaths) + batchSize - 1) / batchSize) +
                         " batches")
        sys.stdout.flush()
        '''
    batchedFiles = formData(imagePaths)
    batchedFiles["appId"] = (None, appId)
    batchedFiles["appKey"] = (None, appKey)
    batchedFiles["groupId"] = (None, groupId)
        
    #print "batchedFiles\n" + str(batchedFiles)

    #print batchedFiles["appId"]
    #print batchedFiles["appKey"]
    #print batchedFiles["groupId"]
    res = requests.post(url, files=batchedFiles)
        
    uploadingEnds = time.time()
        
    closeFiles(batchedFiles)
    res = yaml.safe_load(res.text)
    if res["status"] != "success":
        return res
    if not response:
        response = res
    else:
        response["result"].extend(res["result"])
    #print "\n time taken "+str(uploadingEnds - uploadingStart)
    return response

def getFacePaths(basePath):
    facePaths = [os.path.join(basePath, imageFile)
                 for imageFile in os.listdir(basePath)
                 if imageFile.endswith(".jpg")]
    return facePaths

def closeFiles(files):
    for fileName in files:
        #checking if object is of file type, i.e. had method close
        if hasattr(files[fileName], 'close'):
            files[fileName].close()
