from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime    

from django import forms
from django.shortcuts import get_object_or_404

from django.conf import settings
from .models import Donation, Receipt
from service_objects.services import Service


class CreateReceipt(Service):
    donation_pk = forms.CharField()
    
    def process(self):
        donation_pk = self.cleaned_data['donation_pk']
        donation = get_object_or_404(Donation, pk=donation_pk)

        receipt_pdf_file_name = self.__generate_receipt_pdf(donation)

        receipt = Receipt(
            donation = donation,
            receipt_pdf = receipt_pdf_file_name
            )
            
        receipt.save()
        
        self.__send_email(receipt)
        
        return receipt
        
    def __generate_receipt_pdf(self, donation):
        print()
        
        width, height = letter
        file_path = settings.BASE_DIR + '/projectname/media/' + Receipt.STORAGE_DIR_NAME + '/'
        file_name = '-'.join('-'.join([
            donation.donor.last_name,
            donation.charity.name,
            'receipt',
            datetime.datetime.now().strftime("%m%d%y%H%M%S"),
            ]).split(' ')) + '.pdf'
        myCanvas = canvas.Canvas(file_path + file_name, pagesize=letter)

        formatted_date_today = datetime.datetime.now().strftime("%m/%d/%Y")
        myCanvas.drawString(100, 200, formatted_date_today)
        
        from reportlab.lib.utils import ImageReader
        from reportlab.lib.utils import Image as PilImage
        
        logo = donation.charity.logo
        
        img = ImageReader(logo)
        orig_width, orig_height = img.getSize()
        aspect = orig_height / orig_width
        desired_width = 200
        desired_height = 200 * aspect
        myCanvas.drawInlineImage(PilImage.open(logo), 100, 500, width=desired_width, height=desired_height)
        myCanvas.showPage()
        myCanvas.save()

        return file_name
        
    def __send_email(self, receipt):
        email_address = receipt.donation.donor.email
        print('I will email this receipt to ' + email_address)