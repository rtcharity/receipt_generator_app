from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from receipt_generator.models import Donation
from .base import FunctionalTest

class CreateDonationTest(FunctionalTest):

    def test_create_a_new_donor(self):
        self.create_charity()
        self.create_donor()
        self.wait_for(
            self.browser.find_element_by_id('add_donation').click()
        )
        # Create new donation
        self.wait_for(lambda:
            Select(self.browser.find_element_by_id('id_charity')).select_by_visible_text('Test Charity')
        )
        self.browser.find_element_by_id('proceed')
        self.wait_for(lambda:
            Select(self.browser.find_element_by_id('id_donor')).select_by_visible_text('Testo Testerson')
        )
        self.browser.find_element_by_class_name('form-control flatpickr-input form-control input').click()
        eighth_day_listed = self.browser.find_element_by_class_name('dayContainer')[7]
        eighth_day_listed.click()
        self.browser.find_element_by_id('id_amount').send_keys('56789')
        Select(self.browser.find_element_by_id('id_currency')).select_by_visible_text('USD')
        self.browser.find_element_by_id('save').click()

        # Check for success message
        self.wait_for(lambda: self.assertIn(
            'Successfully saved new donation info', self.browser.find_element_by_class_name('alert alert-success').text)
        )
        
        # Donation is on list of donations
        self.browser.find_element_by_id('list_donors').click()
        donation = Donation.objects.filter(amount=56789)[0]
        self.wait_for(lambda:
            self.assertIn(donation.date_received, self.browser.find_element_by_id('date_' + str(donation.id).text))
        )
        self.assertIn(donation.donor, self.browser.find_element_by_id('donor_' + str(donation.id)).text)
        self.assertIn(donation.charity, self.browser.find_element_by_id('charity_' + str(donation.id)).text)
        self.assertIn(donation.amount, self.browser.find_element_by_id('amount_' + str(donation.id)).text)
        self.assertIn(donation.currency, self.browser.find_element_by_id('currency_' + str(donation.id)).text)
        self.assertIn('(None)', self.browser.find_element_by_id('earmark_' + str(donation.id)).text)

        # Donor view displays with all data
        self.browser.find_element_by_id('view_' + donation.id).click()
        self.wait_for(lambda:
            self.assertIn('View donation', self.browser.find_element_by_tag_name('h1').text)
        )
        self.assertIn(donation.date_received, self.browser.find_element_by_id('date_' + str(donation.id)).text)
        self.assertIn(donation.donor, self.browser.find_element_by_id('donor_' + str(donation.id)).text)
        self.assertIn(donation.charity, self.browser.find_element_by_id('charity_' + str(donation.id)).text)
        self.assertIn(donation.amount, self.browser.find_element_by_id('amount_' + str(donation.id)).text)
        self.assertIn(donation.currency, self.browser.find_element_by_id('currency_' + str(donation.id)).text)
        self.assertIn('(None)', self.browser.find_element_by_id('earmark_' + str(donation.id)).text)