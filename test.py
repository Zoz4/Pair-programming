import json

def readJsonFile(file_path):
    with open(file_path,'r') as json_file:
        dict = json.load(json_file)
    return dict

dict = readJsonFile('.//test.json')

print(dict['426830571'])
print(dict['412038576'])
