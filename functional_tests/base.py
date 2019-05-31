from django.test.utils import override_settings
from django.conf import settings

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.auth import get_user_model
import unittest
import time
import os

class FunctionalTest(StaticLiveServerTestCase):

    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')  
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        self.TEST_ADMIN = self.create_superuser()
        self.log_in_as_admin()

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
    
    def log_in_as_admin(self):
        # Go to home page
        self.browser.get(self.live_server_url)
        # Log in
        self.browser.find_element_by_id('id_username').send_keys(self.TEST_ADMIN.username)
        password_input = self.browser.find_element_by_id('id_password')
        password_input.send_keys('test')
        password_input.send_keys(Keys.ENTER)
        self.wait_for(lambda:
            self.assertIn('Welcome', self.browser.find_element_by_tag_name('h1').text)
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
        # set up method begins us at the homepage, logged in
        self.browser.find_element_by_id('admin_interface_link').click()
        self.wait_for(lambda:
            self.browser.find_element_by_xpath('//*[@id="content-main"]/div[2]/table/tbody/tr[1]/td[1]/a').click()
        )
        self.wait_for(lambda:
            self.browser.find_element_by_id('id_name')
        )

        # Input new data
        self.browser.find_element_by_id('id_name').send_keys(name)
        self.browser.find_element_by_id('id_address').send_keys(address)
        uploads_directory = os.path.join(os.path.dirname(__file__), 'files_for_testing_upload')
        self.browser.find_element_by_id('id_logo').send_keys(os.path.join(uploads_directory, 'RCF_logo.png'))
        self.browser.find_element_by_id('id_signature').send_keys(os.path.join(uploads_directory, 'john_smith_signature.png'))
        self.browser.find_element_by_id('id_registration').send_keys(registration)
        self.browser.find_element_by_id('id_email').send_keys(email)
        self.browser.find_element_by_id('id_revenue_agency').send_keys(revenue_agency)
        self.browser.find_element_by_id('id_revenue_agency').send_keys(Keys.ENTER)

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
        
    
    # def wait_for_row_in_list_table(self, row_text):
    #     start_time = time.time()
    #     while True:
    #         try:
    #             table = self.browser.find_element_by_id('id_list_table')
    #             rows = table.find_elements_by_tag_name('tr')
    #             self.assertIn(row_text, [row.text for row in rows])
    #             return
    #         except (WebDriverException, AssertionError) as e:
    #             if (time.time() - start_time) > self.MAX_WAIT:
    #                 raise e
    #             else:
    #                 time.sleep(0.5)
    
    # def test_layout_and_styling(self):
    #     # Edith goes to the home page
    #     self.browser.get(self.live_server_url)
    #     self.browser.set_window_size(1024, 768)

    #     # She notices the input box is off-center
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     self.assertAlmostEqual(
    #         inputbox.location['x'] + inputbox.size['width'] / 2,
    #         266,
    #         delta=10
    #     )

    # def test_can_start_a_list_and_retrieve_it_later(self):
    #     # Edith has heard about a cool new online to-do app. She goes
    #     # to check out its homepage
    #     self.browser.get(self.live_server_url) # instead of hardcoding localhost 8000

    #     # She notices the page title and header mention to-do lists
    #     self.assertIn('To-Do', self.browser.title)
    #     header_text = self.browser.find_element_by_tag_name('h1').text # This find method is provided by selenium
    #     self.assertIn('To-Do', header_text)
        
    #     # She is invited to enter a to-do item straight away
    #     inputbox = self.browser.find_element_by_id('id_new_item')  
    #     self.assertEqual(
    #         inputbox.get_attribute('placeholder'),
    #         'Enter a to-do item'
    #     )

    #     # She types "Buy peacock feathers" into a text box (Edith's hobby
    #     # is tying fly-fishing lures)
    #     inputbox.send_keys('Buy peacock feathers')
    #     inputbox.send_keys(Keys.ENTER)


    #     # When she hits enter, the page updates, and now the page lists
    #     # "1: Buy peacock feathers" as an item in a to-do list
    #     self.wait_for_row_in_list_table('1: Buy peacock feathers')

    #     # There is still a text box inviting her to add another item. She
    #     # enters "Use peacock feathers to make a fly" (Edith is very
    #     # methodical)
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     inputbox.send_keys('Use peacock feathers to make a fly')
    #     inputbox.send_keys(Keys.ENTER)

    #     # The page updates again, and now shows both items on her list
    #     self.wait_for_row_in_list_table('1: Buy peacock feathers')
    #     self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

    #     # Satisfied, she goes back to sleep

    # def test_multiple_users_can_start_lists_at_different_urls(self):
    #     # Edith starts a new to-do list
    #     self.browser.get(self.live_server_url)
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     inputbox.send_keys('Buy peacock feathers')
    #     inputbox.send_keys(Keys.ENTER)
    #     self.wait_for_row_in_list_table('1: Buy peacock feathers')

    #     # She notices that her list has a unique URL
    #     edith_list_url = self.browser.current_url
    #     self.assertRegex(edith_list_url, '/lists/.+')

    #     #  Now a new user, Francis, comes along to the site.

    #     ## We use a new browser session to make sure that no information
    #     ## of Edith's is coming through from cookies etc
    #     self.browser.quit()
    #     self.browser = webdriver.Firefox()

    #     # Francis visits the home page.  There is no sign of Edith's
    #     # list
    #     self.browser.get(self.live_server_url)
    #     page_text = self.browser.find_element_by_tag_name('body').text
    #     self.assertNotIn('Buy peacock feathers', page_text)
    #     self.assertNotIn('make a fly', page_text)

    #     # Francis starts a new list by entering a new item. He
    #     # is less interesting than Edith...
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     inputbox.send_keys('Buy milk')
    #     inputbox.send_keys(Keys.ENTER)
    #     self.wait_for_row_in_list_table('1: Buy milk')

    #     # Francis gets his own unique URL
    #     francis_list_url = self.browser.current_url
    #     self.assertRegex(francis_list_url, '/lists/.+')
    #     self.assertNotEqual(francis_list_url, edith_list_url)

    #     # Again, there is no trace of Edith's list
    #     page_text = self.browser.find_element_by_tag_name('body').text
    #     self.assertNotIn('Buy peacock feathers', page_text)
    #     self.assertIn('Buy milk', page_text)

    #     # Satisfied, they both go back to sleep