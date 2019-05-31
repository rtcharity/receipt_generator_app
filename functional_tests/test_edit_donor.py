from selenium.webdriver.common.keys import Keys

from receipt_generator.models import Donor
from .base import FunctionalTest

class EditDonorTest(FunctionalTest):        
    
    def test_edit_a_donor(self):
        field_ids = ['id_first_name', 'id_last_name', 'id_address', 'id_email']

        # Create new donor - inherited from base.py
        donor_original_details = self.create_donor()
        
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
        i = 0
        for field_id in field_ids:
            self.assertIn(
                donor_original_details[i],
                self.browser.find_element_by_id(field_id).get_attribute('value')
            )
            i += 1

        # Change the data
        new_donor_details = ['Pesto', 'Peterson', 'USA', 'pesto@email.com']
        i = 0
        for field_id in field_ids:
            element = self.browser.find_element_by_id(field_id)
            element.send_keys(Keys.CONTROL, 'a')
            element.send_keys(Keys.BACKSPACE)
            element.send_keys(new_donor_details[i])
            i += 1
        self.browser.find_element_by_class_name('btn-success').click()

        # Assertions
        self.wait_for(lambda: self.assertIn(
            'Successfully saved', self.browser.find_element_by_class_name('alert-success').text)
        )
        i = 0
        for field_id in field_ids:    
            self.assertIn(
                new_donor_details[i],
                self.browser.find_element_by_id(field_id).get_attribute('value')
            )
            i += 1