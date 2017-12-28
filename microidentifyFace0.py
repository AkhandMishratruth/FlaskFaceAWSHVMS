import httplib, urllib, base64, sys, json, os

subscription_key_MS = os.environ.get("subscription_key_MS")
headers1 = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key_MS,
}

headers2 = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key_MS,
}

conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

def detectFace(faceUri):
    params = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender',
    })

    body = open(faceUri, 'rb')

    try:        
        conn.request("POST", "/face/v1.0/detect?%s" % params,body, headers1)
        response = conn.getresponse()
        data = response.read()
        #print data
        parsedData = json.loads(data)

        #print(parsedData[0]["faceAttributes"]["gender"])
        #print(parsedData[0]["faceAttributes"]["age"])
        return parsedData[0]
    except Exception as e:
        #print("[Errno {0}] {1}".format(e.errno, e.strerror))
        print(e)
        
def identifyFace(faceId):
    params = urllib.urlencode({
    'personGroupId': 'inventopeople',
})
    personGroupId = 'inventopeople'

    body = {}
    body['faceIds'] = [str(faceId)]
    body['personGroupId'] = personGroupId
    body['maxNumOfCandidatesReturned'] = 1
    body['confidenceThreshold'] =  0.5

    #print(body)

    try:
        conn.request("POST", "/face/v1.0/identify?%s" % params, str(body), headers2)
        response = conn.getresponse()
        data = response.read()
        parsedData = json.loads(data)
        #print(data)
        return data
        if(len(parsedData[0]["candidates"]) < 1):
            #print("User is not found")
            return "User is not found"
        
        return parsedData[0]["candidates"][0]
    except Exception as e:
        #print("[Errno {0}] {1}".format(e.errno, e.strerror))

	conn.close()