import json
import hashlib
import requests
import os
from dotenv import load_dotenv
from multiprocessing.dummy import Pool as ThreadPool


def main():
    load_dotenv()
    data = readFile(os.getenv('INPUT_PATH'))
    pool = ThreadPool(2)
    processedData = pool.map(processData, data)
    outputPath = os.getenv('OUTPUT_PATH')
    writeToFile(outputPath, processedData)


def processData(obj):
    processedEvent = {}
    type = getActionType(obj['action'])
    ip = hashIP(obj['action'])
    country = getCountry(obj['action'])
    latency = getLatency(obj['action'])
    siteName = getSiteName(obj['action'])
    processedEvent['topic'] = 'SITE_ANALYTICS'
    processedEvent['timestamp'] = obj['timestamp']
    processedEvent['siteId'] = obj['siteId']
    processedEvent['create_type'] = type[0]
    processedEvent['publish_type'] = type[1]
    processedEvent['unpublish_type'] = type[2]
    processedEvent['update_type'] = type[3]
    processedEvent['visit_type'] = type[4]
    processedEvent['clientIpAddressHash'] = ip
    processedEvent['country'] = country
    processedEvent['latencyMs'] = latency
    processedEvent['siteName'] = siteName
    return processedEvent


def readFile(path):
    data = []
    with open(path) as file:
        for jsonObj in file:
            dic = json.loads(jsonObj)
            if dic['topic'] == 'SITE_EVENT':
                data.append(dic)
    return data


def writeToFile(path,listOfDictionaries):
    with open(path, 'w') as f:
        for line in listOfDictionaries:
            json.dump(line, f)
            f.write('\n')


def getActionType(action):
    oneHotArray = [0, 0, 0, 0, 0]
    type = action['type']
    if isinstance(type, str):
        if type == 'CREATE':
            oneHotArray = [1, 0, 0, 0, 0]
        elif type == 'PUBLISH':
            oneHotArray = [0, 1, 0, 0, 0]
        elif type == 'UNPUBLISH':
            oneHotArray = [0, 0, 1, 0, 0]
        elif 'UPDATE' in type:
            oneHotArray = [0, 0, 0, 1, 0]
        elif type == 'VISIT':
            oneHotArray = [0, 0, 0, 0, 1]
        else:
            return oneHotArray
    else:
        return oneHotArray
    return oneHotArray


def hashIP(action):
    if 'clientIpAddress' in action:
        return hashlib.sha256(action['clientIpAddress'].encode('utf-8')).hexdigest()
    else:
        return ''


def getCountry(action):
    if 'clientIpAddress' in action and action['clientIpAddress'] != '':
        ip = action['clientIpAddress']
        headers = {
            'x-api-key': os.getenv('API_KEY'),
            'Accept': 'application/json'
        }
        response = requests.get(os.getenv('API_URL') + ip,
                                headers=headers)
        jsonData = json.loads(response.text)
        return jsonData['countryCode']
    else:
        return ''


def getLatency(action):
    if 'latencyMs' in action:
        if isinstance(action['latencyMs'], int):
            return action['latencyMs']
        else:
            return ''
    else:
        return ''


def getSiteName(action):
    if 'siteName' in action:
        if isinstance(action['siteName'], str):
            return action['siteName']
        else:
            return ''
    else:
        return ''


if __name__ == "__main__":
    main()
