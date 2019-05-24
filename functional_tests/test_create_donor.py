from django.test.utils import override_settings
from django.conf import settings
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class CreateDonorTest(FunctionalTest):
    
    def test_create_a_new_donor(self):
       pass