from selenium.webdriver.common.keys import Keys

from receipt_generator.models import Donor
from .base import FunctionalTest

class CreateDonorTest(FunctionalTest):
    
    def test_create_a_new_donor(self):
        self.browser.find_element_by_id('add_donor').click()
        # Create new donor
        self.wait_for(lambda: self.browser.find_element_by_id('id_first_name').send_keys('Testo'))
        self.browser.find_element_by_id('id_last_name').send_keys('Testerson')
        self.browser.find_element_by_id('id_address').send_keys('1 Test Street\nTest Town\nTest State')
        self.browser.find_element_by_id('id_email').send_keys('test@email.com')
        self.browser.find_element_by_id('id_email').send_keys(Keys.ENTER)
        
        # Donor appears on list of donors
        self.wait_for(lambda: self.browser.find_element_by_id('list_donors').click())
        donor_id = str(Donor.objects.filter(first_name='Testo')[0].id)
        self.wait_for(lambda:
            self.assertIn('Testo Testerson', self.browser.find_element_by_id('name_' + donor_id).text)
        )
        self.assertIn('test@email.com', self.browser.find_element_by_id('email_' + donor_id).text)
        # Donor view displays with all data
        self.browser.find_element_by_id('view_' + donor_id).click()
        self.wait_for(lambda:
            self.assertIn('View donor', self.browser.find_element_by_tag_name('h1').text)
        )
        self.assertIn('Testo', self.browser.find_element_by_id('id_first_name').get_attribute('value'))
        self.assertIn('Testerson', self.browser.find_element_by_id('id_last_name').get_attribute('value'))
        self.assertIn('1 Test Street\nTest Town\nTest State', self.browser.find_element_by_id('id_address').get_attribute('value'))
        self.assertIn('test@email.com', self.browser.find_element_by_id('id_email').get_attribute('value'))