import requests
import json



def getUnfinishedProblem(teamid):
    url = 'http://47.102.118.1:8089/api/team/problem/'+str(teamid)
    probInfo = requests.get(url)
    return probInfo.json()
if __name__ == '__main__':
    print('interface.py')

    probInfo = getUnfinishedProblem(40)
    print(len(probInfo))
    for info in probInfo:
        print(info['uuid'])
