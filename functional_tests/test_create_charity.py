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
        # Inherited set up method begins us at the homepage, logged in
        self.browser.find_element_by_id('admin_interface_link').click()
        self.wait_for(lambda:
            self.browser.find_element_by_xpath('//*[@id="content-main"]/div[2]/table/tbody/tr[1]/td[1]/a').click()
        )
        self.wait_for(lambda:
            self.browser.find_element_by_id('id_name')
        )

        # Input new data
        self.browser.find_element_by_id('id_name').send_keys('Test Charity')
        self.browser.find_element_by_id('id_address').send_keys('1 Oxford Street\nLondon')
        uploads_directory = os.path.join(os.path.dirname(__file__), 'files_for_testing_upload')
        self.browser.find_element_by_id('id_logo').send_keys(os.path.join(uploads_directory, 'RCF_logo.png'))
        self.browser.find_element_by_id('id_signature').send_keys(os.path.join(uploads_directory, 'john_smith_signature.png'))
        self.browser.find_element_by_id('id_registration').send_keys('0123456789')
        self.browser.find_element_by_id('id_email').send_keys('charity@email.com')
        self.browser.find_element_by_id('id_revenue_agency').send_keys('IRS')
        self.browser.find_element_by_id('id_revenue_agency').send_keys(Keys.ENTER)

        # Assert that the new data is saved and visible
        self.wait_for(lambda: self.assertIn(
            'The charity "Test Charity" was added successfully.',
            self.browser.find_element_by_class_name('success').text
            )
        )
        self.browser.find_element_by_xpath('//*[@id="container"]/ul/li/a').click()
        self.wait_for(lambda: self.assertIn(
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


