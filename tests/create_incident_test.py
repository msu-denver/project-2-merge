'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s):
Description: Project 2 - Create Incident Test
'''

import unittest, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class createIncidentTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:5000/')

    def testCreateIncident(self):
        signinButton = self.browser.find_elements(By.TAG_NAME, 'button')[0]
        signinButton.click()
        id = self.browser.find_element(By.ID, 'id')
        self.assertIsNotNone(id)
        id.send_keys('Logan')
        passwd = self.browser.find_element(By.ID, 'password')
        self.assertIsNotNone(passwd)
        passwd.send_keys('Logan670')
        submit = self.browser.find_element(By.ID, 'submit')
        submit.click()
        createIncidentButton = self.browser.find_elements(By.TAG_NAME, 'form')[11]
        createIncidentButton.click()
        year = self.browser.find_element(By.ID, 'date')
        self.assertIsNotNone(year)
        year.send_keys('10.11.2024')
        actor = self.browser.find_element(By.ID, 'actor')
        self.assertIsNotNone(actor)
        actor.send_keys('Undetermined')
        organization = self.browser.find_element(By.ID, 'organization')
        self.assertIsNotNone(organization)
        organization.send_keys('Undetermined')
        submit = self.browser.find_element(By.ID, 'submit')
        submit.click()

if __name__ == '__main__':
    unittest.main()