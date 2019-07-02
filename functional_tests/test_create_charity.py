from django.test.utils import override_settings
from django.conf import settings
from selenium.webdriver.common.keys import Keys
import os

from .base import FunctionalTest


class CreateCharityTest(FunctionalTest):
    
    # Setting DEBUG to True prevents an error whereby
    # the admin site doesn't load any static files and raises an error.
    @override_settings(DEBUG=True)
    def test_create_a_new_charity(self):
        # Inherited method from base.py navigates to the admin interface and creates a charity
        self.create_charity(log_out_admin=False)

        # Assert that the new data is saved and visible
        self.wait_for(lambda:
            self.browser.find_element_by_xpath('//*[@id="container"]/ul/li/a').click()
        )
        self.wait_for(lambda:
            self.assertIn(
                'Test Charity',
                self.browser.find_element_by_id('id_name').get_attribute('value')
            )
        )
        self.assertIn('1 Oxford Street\nLondon', self.browser.find_element_by_id('id_address').get_attribute('value'))
        self.assertIn('RCF_logo', self.browser.find_element_by_xpath('//*[@id="charity_form"]/div/fieldset/div[3]/div/p/a').text)
        self.assertIn('john_smith_signature', self.browser.find_element_by_xpath('//*[@id="charity_form"]/div/fieldset/div[4]/div/p/a').text)
        self.assertIn('0123456789', self.browser.find_element_by_id('id_registration').get_attribute('value'))
        self.assertIn('charity@email.com', self.browser.find_element_by_id('id_email').get_attribute('value'))
        self.assertIn('IRS', self.browser.find_element_by_id('id_revenue_agency').get_attribute('value'))


