import unittest
import os
from dotenv import load_dotenv
import requests
from src.main import getActionType, getLatency, getSiteName


load_dotenv()


class TestAPI(unittest.TestCase):
    def testAPI(self):
        headers = {
            'x-api-key': os.getenv('API_KEY'),
            'Accept': 'application/json'
        }
        ip = "29.19.66.49"
        response = requests.get(os.getenv('API_URL') + ip, headers=headers)
        self.assertEqual(response.status_code, 200)

    def testAPIWithInavlidIpString(self):
        headers = {
            'x-api-key': os.getenv('API_KEY'),
            'Accept': 'application/json'
        }
        ip = "string"
        response = requests.get(os.getenv('API_URL') + ip, headers=headers)
        self.assertEqual(response.status_code, 400)

    def testAPIWithInvalidIpInteger(self):
        headers = {
            'x-api-key': os.getenv('API_KEY'),
            'Accept': 'application/json'
        }
        ip = "12345678"
        response = requests.get(os.getenv('API_URL') + ip, headers=headers)
        self.assertEqual(response.status_code, 400)


class TestGetActionType(unittest.TestCase):
    def testGetActionTypeVisit(self):
        action = {"type": "VISIT", "clientIpAddress": "134.236.139.19", "latencyMs": 41}
        actual = getActionType(action)
        expected = [0, 0, 0, 0, 1]
        self.assertEqual(actual, expected)

    def testGetActionTypeCreate(self):
        action = {"type": "CREATE", "email": "Alexzander.Bins@yahoo.com", "plan": "ENTERPRISE"}
        actual = getActionType(action)
        expected = [1, 0, 0, 0, 0]
        self.assertEqual(actual, expected)

    def testGetActionTypePublish(self):
        action = {"type": "PUBLISH"}
        actual = getActionType(action)
        expected = [0, 1, 0, 0, 0]
        self.assertEqual(actual, expected)

    def testGetActionTypeUnpublish(self):
        action = {"type": "UNPUBLISH"}
        actual = getActionType(action)
        expected = [0, 0, 1, 0, 0]
        self.assertEqual(actual, expected)
        
    def testGetActionTypeUpdate(self):
        action = {"type": "UPDATE_SITE_NAME", "siteName": "roscoe.biz"}
        actual = getActionType(action)
        expected = [0, 0, 0, 1, 0]
        self.assertEqual(actual, expected)

    def testGetActionTypeInvalidType(self):
        action = {"type": "READ", "siteName": "roscoe.biz"}
        actual = getActionType(action)
        expected = [0, 0, 0, 0, 0]
        self.assertEqual(actual, expected)

    def testGetActionTypeEmptyType(self):
        action = {"type": "", "siteName": "roscoe.biz"}
        actual = getActionType(action)
        expected = [0, 0, 0, 0, 0]
        self.assertEqual(actual, expected)

    def testGetActionTypeNonStringVal(self):
        action = {"type": 2, "siteName": "roscoe.biz"}
        actual = getActionType(action)
        expected = [0, 0, 0, 0, 0]
        self.assertEqual(actual, expected)


class TestGetLatency(unittest.TestCase):
    def testGetLatency(self):
        action = {"type": "VISIT", "clientIpAddress": "194.54.109.58", "latencyMs": 13}
        actual = getLatency(action)
        expected = 13
        self.assertEqual(actual, expected)

    def testGetLatencyEmptyVal(self):
        action = {"type": "VISIT", "clientIpAddress": "194.54.109.58", "latencyMs": ""}
        actual = getLatency(action)
        expected = ''
        self.assertEqual(actual, expected)

    def testGetLatencyNonIntVal(self):
        action = {"type": "VISIT", "clientIpAddress": "194.54.109.58", "latencyMs": "string"}
        actual = getLatency(action)
        expected = ''
        self.assertEqual(actual, expected)


class TestGetSiteName(unittest.TestCase):
    def testGetSiteName(self):
        action = {"type": "UPDATE_SITE_NAME", "siteName": "roscoe.biz"}
        actual = getSiteName(action)
        expected = 'roscoe.biz'
        self.assertEqual(actual, expected)

    def testGetSiteNameEmptyVal(self):
        action = {"type": "UPDATE_SITE_NAME", "siteName": ""}
        actual = getSiteName(action)
        expected = ''
        self.assertEqual(actual, expected)

    def testGetSiteNameNonStringVal(self):
        action = {"type": "UPDATE_SITE_NAME", "siteName": 3464}
        actual = getSiteName(action)
        expected = ''
        self.assertEqual(actual, expected)
