import unittest
import time
import os

from django.test.utils import override_settings
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException

from receipt_generator.models import Charity

class FunctionalTest(StaticLiveServerTestCase):

    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')  
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        self.TEST_ADMIN = self.create_superuser()
        self.uploads_directory = os.path.join(os.path.dirname(__file__), 'files_for_testing_upload')
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    def create_superuser(self):
        User = get_user_model()
        number_of_users = User.objects.count()
        test_admin = User.objects.create_superuser(
            username='test_admin' + str(number_of_users + 1),
            password='test',
            email='test@test.com',
            )
        return test_admin
    
    def log_in_to_admin_side_of_site(self):
        # Go to home page
        self.browser.get(self.live_server_url)
        # Log in
        self.browser.find_element_by_id('admin_interface_link').click()
        self.browser.find_element_by_id('id_username').send_keys(self.TEST_ADMIN.username)
        password_input = self.browser.find_element_by_id('id_password')
        password_input.send_keys('test')
        password_input.send_keys(Keys.ENTER)
        self.wait_for(lambda:
            self.assertIn('WELCOME', self.browser.find_element_by_id('user-tools').text)
        )

    def wait_for(self, function):
        start_time = time.time()
        while True:
            try:
                return function()  
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    # Setting DEBUG to True prevents an error whereby
    # the admin site doesn't load any static files and raises an error.
    @override_settings(DEBUG=True)
    def create_charity(
        self,
        name='Test Charity',
        address='1 Oxford Street\nLondon',
        registration='0123456789',
        email='charity@email.com',
        revenue_agency='IRS',
    ):
        self.log_in_to_admin_side_of_site()
        
        # Click to add a charity
        self.wait_for(lambda:
            self.browser.find_element_by_xpath('//*[@id="content-main"]/div[2]/table/tbody/tr[1]/td[1]/a').click()
        )
        self.wait_for(lambda:
            self.browser.find_element_by_id('id_name')
        )

        # Input new data
        self.browser.find_element_by_id('id_name').send_keys(name)
        self.browser.find_element_by_id('id_address').send_keys(address)
        self.browser.find_element_by_id('id_logo').send_keys(os.path.join(self.uploads_directory, 'RCF_logo.png'))
        self.browser.find_element_by_id('id_signature').send_keys(os.path.join(self.uploads_directory, 'john_smith_signature.png'))
        self.browser.find_element_by_id('id_registration').send_keys(registration)
        self.browser.find_element_by_id('id_email').send_keys(email)
        self.browser.find_element_by_id('id_revenue_agency').send_keys(revenue_agency)
        self.browser.find_element_by_id('id_revenue_agency').send_keys(Keys.ENTER)

        return Charity.objects.last()

    def create_donor(
        self,
        first_name='Testo',
        last_name='Testerson',
        address='1 Test Street\nTest Town\nTest State',
        email='test@email.com',
    ):
        self.wait_for(lambda: self.browser.find_element_by_id('add_donor').click())
        # Create new donor
        self.wait_for(lambda: self.browser.find_element_by_id('id_first_name').send_keys(first_name))
        self.browser.find_element_by_id('id_last_name').send_keys(last_name)
        self.browser.find_element_by_id('id_address').send_keys(address)
        self.browser.find_element_by_id('id_email').send_keys(email)
        self.browser.find_element_by_id('id_email').send_keys(Keys.ENTER)

        return [first_name, last_name, address, email]

    def create_donation(
        self,
        charity='Test Charity',
        donor='Testo Testerson',
        nth_date=17,
        amount=56789,
        currency='USD',
    ):
        self.wait_for(lambda:
            self.browser.find_element_by_id('add_donation').click()
        )
        # Create new donation
        self.wait_for(lambda:
            Select(self.browser.find_element_by_id('id_charity')).select_by_visible_text(charity)
        )
        self.browser.find_element_by_id('proceed').click()
        self.wait_for(lambda:
            Select(self.browser.find_element_by_id('id_donor')).select_by_visible_text(donor)
        )
        self.browser.find_element_by_xpath('/html/body/div[1]/form/p[3]/input[2]').click() # Click the date_received input
        # Whatever happens to be the (n+1)th day on the calendar
        n_plus_oneth_day_listed = self.browser.find_elements_by_class_name('flatpickr-day')[nth_date]
        n_plus_oneth_day_listed.click()
        self.browser.find_element_by_id('id_amount').send_keys(str(amount))
        Select(self.browser.find_element_by_id('id_currency')).select_by_visible_text(currency)
        self.browser.find_element_by_id('save').click()
        