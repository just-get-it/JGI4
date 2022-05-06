from django.conf import settings
from xhtml2pdf import pisa
from django.core.files import File
import os


def invoice():
    print("runs")
    bill_html = '<h1>Hello world!</h1>'

    
    
    file=open('Bill_7.pdf','w+b')
    pisa_status = pisa.CreatePDF(
        bill_html,
        dest=file)
    file.close()

invoice()