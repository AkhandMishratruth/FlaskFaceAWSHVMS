import boto3
import io
import os
from PIL import Image

def search(imagePath):
    
    ACCESS_KEY = os.environ.get("ACCESS_KEY_AWS")
    SECRET_KEY = os.environ.get("SECRET_KEY_AWS")

    print(ACCESS_KEY, SECRET_KEY)
    rekognition = boto3.client('rekognition', region_name='us-east-1',aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    image = Image.open(imagePath)
    stream = io.BytesIO()
    image.save(stream,format="JPEG")
    image_binary = stream.getvalue()

    response = rekognition.search_faces_by_image(
            CollectionId='InventoPeople',
            Image={'Bytes':image_binary}                                       
            )
        
    for match in response['FaceMatches']:
        #print (match['Face']['FaceId'],match['Face']['Confidence'])
        #print (match['Face']['ImageId'])

        face = dynamodb.get_item(
            TableName='FaceToName',  
            Key={'RekognitionId': {'S': match['Face']['FaceId']}}
            )
        
        if 'Item' in face:
            return face['Item']['FullName']['S']
        else:
            return 'no match found in person lookup'