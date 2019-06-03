import datetime

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from django.core import mail
from django.test.utils import override_settings

from receipt_generator.models import Donation, Receipt, Donor, Charity
from .base import FunctionalTest

@override_settings(EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend')
class CreateAndSendReceiptTest(FunctionalTest):

    def test_create_and_send_receipt_as_email_attachment(self):
        self.create_charity()
        self.browser.get(self.live_server_url)
        test_charity = self.create_charity(
            name='Another Charity',
            email='another@email.com',
        )
        testo_donor = Donor.objects.create(
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
        donation = Donation.objects.create(
            charity=test_charity,
            donor=testo_donor,
            date_received=datetime.date(2019, 1, 1),
            amount=56789,
            currency='USD',
        )
        self.browser.get(self.live_server_url)
        self.wait_for(lambda:
            self.browser.find_element_by_id('list_donations').click()
        )
    
        # Go to the donation view page
        self.wait_for(lambda:
            self.browser.find_element_by_id('view_' + str(donation.id)).click()
        )

        self.assertIn(str(donation.donor), self.browser.find_element_by_id('donor_' + str(donation.id)).text)
        self.assertIn(str(donation.charity), self.browser.find_element_by_id('charity_' + str(donation.id)).text)
        self.assertIn(str(donation.amount), self.browser.find_element_by_id('amount_' + str(donation.id)).text)
        self.assertIn(str(donation.currency), self.browser.find_element_by_id('currency_' + str(donation.id)).text)
        self.assertIn('(None)', self.browser.find_element_by_id('earmark_' + str(donation.id)).text)

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
        receipt = Receipt.objects.filter(donation=donation)[0]
        email = mail.outbox[0]
        self.assertEquals(email.subject, 'Your donation tax receipt [automated email]')
        self.assertIn(('Dear %s,<br/><br/>Please find attached your donation receipt for tax purposes.' % donation.donor.first_name), email.body)
        self.assertEquals(email.from_email, 'automatic@rtcharity.org')
        self.assertIn(donation.donor.email, email.to)
        self.assertEqual(len(email.attachments), 1)



