import httplib, urllib, base64, sys, json
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'c13754db275c4f41a2448b612f3bb2fa',
}

conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

def detectFace(faceUrl):
	params = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender',
	})

	body = {}
	body['url'] =str(faceUrl)

	try:	    
                conn.request("POST", "/face/v1.0/detect?%s" % params,str(body), headers)
                response = conn.getresponse()
                data = response.read()
                parsedData = json.loads(data)
                print(parsedData[0]["faceAttributes"]["gender"])
                print(parsedData[0]["faceAttributes"]["age"])
                return parsedData[0]["faceId"]
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))
		print(faceUrl)

def identifyFace(faceId):
    params = ""
    personGroupId = 'inventopeople'

    body = {}
    body['faceIds'] = [str(faceId)]
    body['personGroupId'] = personGroupId
    body['maxNumOfCandidatesReturned'] = 1
    body['confidenceThreshold'] =  0.5

    #print(body)

    try:
        conn.request("POST", "/face/v1.0/identify?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        parsedData = json.loads(data)
        print(data)
        if(len(parsedData[0]["candidates"]) < 1):
            print("User is not found")
        
        return parsedData[0]["candidates"][0]
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

conn.close()

if __name__ == "__main__":
   faceId = detectFace('https://s3.amazonaws.com/tempReco/3.jpg')
   #print(faceId)
   identifyFace(faceId)
