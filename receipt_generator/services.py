from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.utils import Image as PilImage

import datetime    


from django import forms
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Donation, Receipt
from service_objects.services import Service


class CreateReceipt(Service):
    donation_pk = forms.CharField()
    
    def process(self):
        donation_pk = self.cleaned_data['donation_pk']
        donation = get_object_or_404(Donation, pk=donation_pk)

        (full_receipt_file_path, receipt_pdf_file_name) = self.__generate_receipt_pdf(donation)

        receipt = Receipt.objects.create(
            donation = donation,
            receipt_pdf = receipt_pdf_file_name
            )
                    
        recipients_list = [donation.donor.email]
        from_email = settings.DEFAULT_FROM_EMAIL
        self.__send_email(receipt, full_receipt_file_path, recipients_list, from_email)
        
        return receipt
        
    def __generate_receipt_pdf(self, donation):
        showFrameBoundaries = 0 #Set to 1 for debugging formatting, 0 for invisible

        width, height = letter
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="RightAligned", alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name="CenterAligned", alignment=TA_CENTER))
        leading = 24
        styles.add(ParagraphStyle(name="NormalWithGap", leading=leading))
        styles.add(ParagraphStyle(name="RightAlignedWithGap", alignment=TA_RIGHT, leading=leading))
        styleN = styles["Normal"]
        styleH = styles["Heading1"]
        styleR = styles["RightAligned"]
        styleC = styles["CenterAligned"]
        styleNwithGap = styles["NormalWithGap"]
        styleRwithGap = styles["RightAlignedWithGap"]
        file_path = settings.BASE_DIR + '/projectname/media/' + Receipt.STORAGE_DIR_NAME + '/'
        unique_receipt_number = "%s%d%d" % (datetime.datetime.now().strftime("%m%d%y%H%M%S"), donation.id, donation.donor.id)
        file_name = '-'.join('-'.join([
            donation.donor.last_name,
            donation.charity.name,
            'receipt',
            unique_receipt_number,
            ]).split(' ')) + '.pdf'
        charity = donation.charity
        donor = donation.donor

        formatted_date_today = datetime.datetime.now().strftime("%m/%d/%Y")
        myCanvas = Canvas(file_path + file_name, pagesize=letter)
        currency_symbols = {'CAD': '$', 'USD': '$'}
        donation_amount_with_currency = "%s%s" % (currency_symbols[donation.currency], donation.amount)

        top_story = []
        top_story.append(Paragraph("Official donation receipt for income tax purposes", styleH))
        top_story.append(self.process_image(charity.logo, new_width=2.5*inch, hAlign='CENTER'))
        
        top_frame = Frame(inch, 8.5*inch, 6*inch, 1.5*inch, showBoundary=showFrameBoundaries)
        top_frame.addFromList(top_story, myCanvas)
        
        left_story = []
        left_story.append(Paragraph("<b>%s</b>" % charity.name, styleNwithGap))
        self.add_address_to_story(charity.address, left_story, styleN, styleNwithGap)
        left_story.append(Paragraph("<b>Registration number</b>: %s" % charity.registration, styleNwithGap))
        left_story.append(Paragraph("<b>Signature</b>:", styleN))
        left_story.append(self.process_image(charity.signature, new_width=inch, hAlign='LEFT'))

        left_frame = Frame(
            inch, #x
            4*inch, #y at bottom
            3*inch, #width
            4*inch, #height
            showBoundary=showFrameBoundaries)
        left_frame.addFromList(left_story, myCanvas)
        
        right_story = []
        right_story.append(Paragraph("<b>Receipt</b> #%s" % unique_receipt_number, styleRwithGap))
        right_story.append(Paragraph("<b>Date Issued</b>: %s" % formatted_date_today, styleRwithGap))
        right_story.append(Paragraph("<b>Location issued</b>: %s" % "not sure", styleRwithGap))
        right_story.append(Paragraph("<b>Donor</b>: %s" % donor, styleRwithGap))
        right_story.append(Paragraph("<b>Address</b>:", styleR))
        self.add_address_to_story(donor.address, right_story, styleR, styleRwithGap)
        right_story.append(Paragraph("<b>Date of Donation</b>: %s" % donation.date_received, styleRwithGap))
        right_story.append(Paragraph("<b>Amount</b>: %s" % donation_amount_with_currency, styleRwithGap))
        right_story.append(Paragraph("<b>Tax-Deductible Amount</b>: %s" % donation_amount_with_currency, styleRwithGap))
        
        right_frame = Frame(4*inch, 4*inch, 3*inch, 4*inch, showBoundary=showFrameBoundaries)
        right_frame.addFromList(right_story, myCanvas)
        
        bottom_story = []
        if charity.revenue_agency == 'CRA':
            revenue_notice = "<b>Canada Revenue Agency</b> - canada.ca/charities-giving"
        elif charity.revenue_agency == 'IRS':
            revenue_notice = "<b>Internal Revenue Service</b> - www.irs.gov"
        bottom_story.append(Paragraph(revenue_notice, styleC))
        bottom_story.append(Paragraph("Notice: No Goods Or Services Were Provided In Return For This Gift", styleC))
        bottom_frame = Frame(inch, 2*inch, 6*inch, 2*inch, showBoundary=showFrameBoundaries)
        bottom_frame.addFromList(bottom_story, myCanvas)
        
        myCanvas.showPage()
        myCanvas.save()

        return (file_path + file_name, file_name)
        
    def add_address_to_story(self, address, story, style, style_with_gap):
        address_as_list = str(address).split("\n")
        for index, line in enumerate(address_as_list):
            if index == len(address_as_list) - 1:
                story.append(Paragraph(line, style_with_gap))
            else:
                story.append(Paragraph(line, style))
            
    def process_image(self, image, new_width, hAlign):
        orig_width, orig_height = ImageReader(image).getSize()
        aspect = orig_height / orig_width
        new_height = new_width * aspect
        return Image(image, width=new_width, height=new_height, hAlign=hAlign)
        
    def __send_email(self, receipt, file_path, recipients, from_email):
        body = "Dear %s,<br/><br/>Please find attached your donation receipt for tax purposes.<br/><br/>To ensure you keep receiving these receipts, add this address to your email whitelist." % receipt.donation.donor.first_name
        msg = EmailMessage('Your donation tax receipt [automated email]', body, from_email, recipients)
        msg.content_subtype = "html"  
        msg.attach_file(file_path)
        msg.send()
    