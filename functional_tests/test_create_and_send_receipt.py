from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from django.core import mail
from django.test.utils import override_settings

from receipt_generator.models import Donation, Receipt
from .base import FunctionalTest

@override_settings(EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend')
class CreateAndEditDonationTest(FunctionalTest):

    def test_create_and_edit_a_new_donation(self):
        self.create_charity()
        self.browser.get(self.live_server_url)
        self.create_charity(name='Another Charity', email='another@email.com')
        self.browser.get(self.live_server_url)
        self.create_donor()
        self.browser.get(self.live_server_url)
        self.create_donor(first_name='Another', last_name='Donor', email='different@email.com')
        self.wait_for(lambda:
            self.browser.find_element_by_id('add_donation').click()
        )
        # Create new donation
        self.wait_for(lambda:
            Select(self.browser.find_element_by_id('id_charity')).select_by_visible_text('Test Charity')
        )
        self.browser.find_element_by_id('proceed').click()
        self.wait_for(lambda:
            Select(self.browser.find_element_by_id('id_donor')).select_by_visible_text('Testo Testerson')
        )
        self.browser.find_element_by_xpath('/html/body/div[1]/form/p[3]/input[2]').click() # Click the date_received input
        eighteenth_day_listed = self.browser.find_elements_by_class_name('flatpickr-day')[17]
        eighteenth_day_listed.click()
        self.browser.find_element_by_id('id_amount').send_keys('56789')
        Select(self.browser.find_element_by_id('id_currency')).select_by_visible_text('USD')
        self.browser.find_element_by_id('save').click()

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

        # Go to the view donation page
        self.browser.find_element_by_id('view_' + str(donation.id)).click()
        original_number_of_receipts = Receipt.objects.count()
        original_number_of_emails = len(mail.outbox)

        # Click the generate and send receipt button
        self.wait_for(lambda:
            self.browser.find_element_by_class_name('btn-success').click()
        )
        self.wait_for(lambda:
            self.assertIn('Receipt generated and sent', self.browser.find_element_by_class_name('alert-success').text)
        )

        # Assertions
        self.assertEquals((Receipt.objects.count() - original_number_of_receipts), 1)
        self.assertEquals((len(mail.outbox) - original_number_of_emails), 1)
        receipt = Receipt.objects.filter(donation=donation)
        email = mail.outbox[0]
        self.assertEquals(email.subject, 'Your donation tax receipt [automated email]')
        self.assertIn(('Dear %s,<br/><br/>Please find attached your donation receipt for tax purposes.' % donation.donor.first_name), email.body)
        self.assertEquals(email.from_email, 'automatic@rtcharity.org')
        self.assertIn(donation.donor.email, email.to)
        self.assertEqual(len(email.attachments), 1)



