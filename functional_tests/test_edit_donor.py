from selenium.webdriver.common.keys import Keys

from receipt_generator.models import Donor
from .base import FunctionalTest

class EditDonorTest(FunctionalTest):

    def delete_whole_field(self, element):
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.BACKSPACE)
    
    def test_edit_a_donor(self):

        # Create new donor - inherited from base.py
        self.create_donor()
        
        # Check for success message
        self.wait_for(lambda: self.assertIn(
            'successfully saved', self.browser.find_element_by_class_name('alert-success').text)
        )
        donor_id = str(Donor.objects.filter(first_name='Testo')[0].id)

        # Go to the edit page for the donor
        self.browser.find_element_by_id('edit_' + donor_id).click()
        self.wait_for(lambda:
            self.assertIn('Edit donor', self.browser.find_element_by_tag_name('h1').text)
        )
        self.assertIn('Testo', self.browser.find_element_by_id('id_first_name').get_attribute('value'))
        self.assertIn('Testerson', self.browser.find_element_by_id('id_last_name').get_attribute('value'))
        self.assertIn('1 Test Street\nTest Town\nTest State', self.browser.find_element_by_id('id_address').get_attribute('value'))
        self.assertIn('test@email.com', self.browser.find_element_by_id('id_email').get_attribute('value'))

        # Change the data
        self.delete_whole_field(self.browser.find_element_by_id('id_first_name'))
        self.browser.find_element_by_id('id_first_name').send_keys('Pesto')
        
        self.delete_whole_field(self.browser.find_element_by_id('id_last_name'))
        self.browser.find_element_by_id('id_last_name').send_keys('Peterson')

        self.delete_whole_field(self.browser.find_element_by_id('id_address'))
        self.browser.find_element_by_id('id_address').send_keys('USA')

        self.delete_whole_field(self.browser.find_element_by_id('id_email'))
        self.browser.find_element_by_id('id_email').send_keys('pesto@email.com')
        self.browser.find_element_by_class_name('btn-success').click()

        # Assertions
        self.wait_for(lambda: self.assertIn(
            'Successfully saved', self.browser.find_element_by_class_name('alert-success').text)
        )
        self.assertIn('Pesto', self.browser.find_element_by_id('id_first_name').get_attribute('value'))
        self.assertIn('Peterson', self.browser.find_element_by_id('id_last_name').get_attribute('value'))
        self.assertIn('USA', self.browser.find_element_by_id('id_address').get_attribute('value'))
        self.assertIn('pesto@email.com', self.browser.find_element_by_id('id_email').get_attribute('value'))