import requests
from PIL import Image
import base64
import json

def getQuestionJsonFile(url):
    r = requests.get(url)
    return r.json()
# 读取答案json文件
def readAnswerJsonFile(filePath):
    with open(filePath,'r') as jsonFile:
        dict = json.load(jsonFile)
    return dict

def writeImage(filePath, base64Image):
    image = base64.b64decode(base64Image)
    with open(filePath,'wb') as fileObject:
        fileObject.write(image)

def cutImage(image,filePath):
    for y in range(3):
        for x in range(3):
            box = (x*300,y*300,(x+1)*300,(y+1)*300)
            cropImage = image.crop(box)
            cropImage.save(filePath+'/'+str(y*3+x+1)+'.jpg')


#dict = readAnswerJsonFile('./test.json')
#writeImage('./1.jpg',dict['img'])
#image = Image.open('./1.jpg')
#cutImage(image,'./source')

#image = Image.open('./target/A_ (2).jpg')
#cutImage(image,'./target/A')

