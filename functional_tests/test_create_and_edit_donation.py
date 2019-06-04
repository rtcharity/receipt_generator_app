from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from receipt_generator.models import Donation, Charity, Donor
from .base import FunctionalTest

class CreateAndEditDonationTest(FunctionalTest):

    def test_create_and_edit_a_new_donation(self):
        Charity.objects.create(
            name='Test Charity',
            address='1 Oxford Street\nLondon',
            registration='0123456789',
            email='charity@email.com',
            revenue_agency='IRS',
        )
        Charity.objects.create(
            name='Another Charity',
            address='1 Oxford Street\nLondon',
            registration='0123456789',
            email='another@email.com',
            revenue_agency='IRS',
        )
        Donor.objects.create(
            first_name='Testo',
            last_name='Testerson',
            address='1 Test Street\nTest Town\nTest State',
            email='test@email.com',
        )
        Donor.objects.create(
            first_name='Another',
            last_name='Donor',
            address='1 Test Street\nTest Town\nTest State',
            email='different@email.com',
        )
        
        # Inherited from base.py
        self.create_donation()

        # Check for success message
        self.wait_for(lambda: self.assertIn(
            'Successfully saved new donation info', self.browser.find_element_by_class_name('alert-success').text
            )
        )
        
        # Donation is on list of donations
        self.browser.find_element_by_id('list_donations').click()
        donation = Donation.objects.filter(amount=56789)[0]
        self.wait_for(lambda:
            self.assertIn(donation.date_received.strftime('%B %d, %Y'), self.browser.find_element_by_id('date_received_' + str(donation.id)).text)
        )
        self.assertIn(str(donation.donor), self.browser.find_element_by_id('donor_' + str(donation.id)).text)
        self.assertIn(str(donation.charity), self.browser.find_element_by_id('charity_' + str(donation.id)).text)
        self.assertIn(str(donation.amount), self.browser.find_element_by_id('amount_' + str(donation.id)).text)
        self.assertIn(str(donation.currency), self.browser.find_element_by_id('currency_' + str(donation.id)).text)
        self.assertIn('(None)', self.browser.find_element_by_id('earmark_' + str(donation.id)).text)

        # Donation view displays with all data
        self.browser.find_element_by_id('view_' + str(donation.id)).click()
        self.wait_for(lambda:
            self.assertIn('View donation', self.browser.find_element_by_tag_name('h1').text)
        )
        self.assertIn(donation.date_received.strftime('%B %d, %Y'), self.browser.find_element_by_id('date_received_' + str(donation.id)).text)
        self.assertIn(str(donation.donor), self.browser.find_element_by_id('donor_' + str(donation.id)).text)
        self.assertIn(str(donation.charity), self.browser.find_element_by_id('charity_' + str(donation.id)).text)
        self.assertIn(str(donation.amount), self.browser.find_element_by_id('amount_' + str(donation.id)).text)
        self.assertIn(str(donation.currency), self.browser.find_element_by_id('currency_' + str(donation.id)).text)
        self.assertIn('(None)', self.browser.find_element_by_id('earmark_' + str(donation.id)).text)

        # Go to edit page
        self.browser.find_element_by_class_name('btn-primary').click()

        # Edit the details
        self.wait_for(lambda:
            Select(self.browser.find_element_by_id('id_charity')).select_by_visible_text('Another Charity')
        )
        Select(self.browser.find_element_by_id('id_donor')).select_by_visible_text('Another Donor')
        self.browser.find_element_by_xpath('/html/body/div[1]/form/p[3]/input[2]').click() # date received
        nineteenth_day_listed = self.browser.find_elements_by_class_name('flatpickr-day')[18]
        nineteenth_day_listed.click()
        amount = self.browser.find_element_by_id('id_amount')
        amount.send_keys(Keys.CONTROL, 'a')
        amount.send_keys(Keys.BACKSPACE)
        amount.send_keys('321.19')
        Select(self.browser.find_element_by_id('id_currency')).select_by_visible_text('CAD')
        self.browser.find_element_by_id('id_other_earmark').send_keys('Special New Earmark')
        self.browser.find_element_by_class_name('btn-success').click()

        # Assertions
        self.wait_for(lambda: self.assertIn(
            'Successfully saved new donation info', self.browser.find_element_by_class_name('alert-success').text
            )
        )
        donation = Donation.objects.filter(amount=321.19)[0]
        self.assertIn('View donation', self.browser.find_element_by_tag_name('h1').text)
        self.assertIn(donation.date_received.strftime('%B %d, %Y'), self.browser.find_element_by_id('date_received_' + str(donation.id)).text)
        self.assertIn('Another Donor', self.browser.find_element_by_id('donor_' + str(donation.id)).text)
        self.assertIn('Another Charity', self.browser.find_element_by_id('charity_' + str(donation.id)).text)
        self.assertIn('321.19', self.browser.find_element_by_id('amount_' + str(donation.id)).text)
        self.assertIn('CAD', self.browser.find_element_by_id('currency_' + str(donation.id)).text)
        self.assertIn('Special New Earmark', self.browser.find_element_by_id('earmark_' + str(donation.id)).text)

