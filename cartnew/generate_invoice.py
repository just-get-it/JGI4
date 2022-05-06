from django.conf import settings
from xhtml2pdf import pisa
from django.core.files import File
import os

def invoice(currOrder,odItems ):
    bill_html = ''
    temp_start = '''<html lang="en">
                    <head>
                    <style type="text/css">
                        .clearfix:after{
                    content: "";
                    display: table;
                    clear: both;
                    }

                    a {
                    color: #5D6975;
                    text-decoration: underline;
                    }

                    body {
                    position: relative; 
                    margin: 0 auto; 
                    color: #001028;
                    background: #FFFFFF; 
                    font-family: Arial, sans-serif; 
                    font-size: 10px; 
                    font-family: Arial;
                    }

                    header {
                    padding: 10px 0;
                    margin-bottom: 30px;
                    }

                    #logo {
                    text-align: center;
                    margin-bottom: 10px;
                    }

                    #logo img {
                    width: 90px;
                    }

                    h1 {
                    border-top: 1px solid  #5D6975;
                    border-bottom: 1px solid  #5D6975;
                    color: #5D6975;
                    font-size: 2.4em;
                    line-height: 1.4em;
                    font-weight: normal;
                    text-align: center;
                    margin: 0 0 20px 0;
                    background: url(dimension.png);
                    }

                    #project {
                    float: left;
                    }

                    #project span {
                    color: #5D6975;
                    text-align: right;
                    width: 52px;
                    margin-right: 10px;
                    display: inline-block;
                    font-size: 0.8em;
                    }

                    #company {
                    float: right;
                    text-align: right;
                    }

                    #project div,
                    #company div {
                    white-space: nowrap;        
                    }

                    table {
                    width: 100%;
                    border-collapse: collapse;
                    border-spacing: 0;
                    margin-bottom: 20px;
                    }

                    table tr:nth-child(2n-1) td {
                    background: #F5F5F5;
                    }

                    table th,
                    table td {
                    text-align: center;
                    }

                    table th {
                    padding: 5px 20px;
                    color: #5D6975;
                    border-bottom: 1px solid #C1CED9;
                    white-space: nowrap;        
                    font-weight: normal;
                    }

                    table .service,
                    table .desc {
                    text-align: left;
                    }

                    table td {
                    padding: 10px;
                    text-align: right;
                    }

                    table td.service,
                    table td.desc {
                    vertical-align: top;
                    }

                    table td.grand {
                    border-top: 1px solid #5D6975;;
                    }

                    #notices .notice {
                    color: #5D6975;
                    font-size: 1.2em;
                    }

                    footer {
                    color: #5D6975;
                    width: 100%;
                    height: 30px;
                    position: absolute;
                    bottom: 0;
                    border-top: 1px solid #C1CED9;
                    padding: 8px 0;
                    text-align: center;
                    }
                    </style>
                    </head>
                    <body>
                        <header class="clearfix">
                        <div id="logo">
                            <h3>Order Bill</h3>
                        </div>
                        <div id="company" class="clearfix">
                            <div>Just Get It</div>
                            <div>38, 10th Cross, 24th Main,<br/> Agara, sector-1, HSR Layout,<br/> Bangalore, Karnataka 560102</div>
                            <div><a href="mailto:support@justgetit.in">support@justgetit.in</a></div>
                        </div>'''

    temp_end = '''</tbody>
                    </table>
                    </main>
                    <footer>
                    Invoice was created on a computer and is valid without the signature and seal.
                    <hr>
                    </footer>
                </body>
                </html>'''
    order_det = '<div id="project"><div><span>ORDER ID: </span>' + str(currOrder.id) + '</div><div><span>PAYMENT : </span>'+ currOrder.payment_method  +'</div><div><span>CLIENT: </span>'+ currOrder.customer.name  +'</div><div><span>ADDRESS: </span> '+ odItems[0].shipping_address.shipping_address + ', ' + odItems[0].shipping_address.state  + ', ' + odItems[0].shipping_address.city  + ' - ' + odItems[0].shipping_address.pin_code  + '.</div><div><span>DATE: </span> '+ currOrder.date_order_placed.strftime("%m/%d/%Y, %H:%M") +'</div></div>'
    table_header = """</header>
                        <main>
                        <table>
                            <thead>
                            <tr>
                                <th class="desc">PRODUCT</th>
                                <th class="service">SELLER</th>
                                <th>SIZE</th>
                                <th>QUANTITY</th>
                                <th>TOTAL</th>
                            </tr>
                            </thead>
                            <tbody>"""
    bill_html = temp_start + order_det + table_header
    for item in odItems:
        if not item.is_Cancelled:
            bill_html += '<tr><td class="desc">'+ item.product_name +'</td><td class="service">'+ item.seller_name +'</td><td class="unit">'+ item.size_name +'</td><td class="qty">' + str(item.quantity) +'</td><td class="total">Rs.'+ str(item.total) +'</td></tr>'
        else:
            bill_html += '<tr style="text-decoration:line-through;"><td class="desc" >'+ item.product_name +'</td><td class="service">'+ item.seller_name +'</td><td class="unit">'+ item.size_name +'</td><td class="qty">' + str(item.quantity) +'</td><td class="total">Rs.'+ str(item.total) +'</td></tr>'
    # here mov is 10000
    if currOrder.total < 10000 and currOrder.is_Cancelled == False:
        bill_html += '<tr><td colspan="3"></td><td>Delivery Charges*:</td><td class="total">Rs. 101</td></tr>'
    bill_html += '<tr style="border-top: 1px solid grey;"><td colspan="3"></td><td>TOTAL:</td><td class="total">Rs. '+ str(currOrder.total) +'</td></tr>'
    bill_html += temp_end
    if os.path.exists(settings.MEDIA_ROOT+ '\local\orders\invoices\Bill_' + str(currOrder.id) + '.pdf'):
            os.remove(settings.MEDIA_ROOT+'\local\orders\invoices\Bill_' + str(currOrder.id) + '.pdf')
    file=open(settings.MEDIA_ROOT + '\\Bill_' + str(currOrder.id) + '.pdf','w+b')
    pisa_status = pisa.CreatePDF(
        bill_html,
        dest=file)
    file.close()
    currOrder.invoice.save('Bill_' + str(currOrder.id) + '.pdf', File(open(settings.MEDIA_ROOT + '\\Bill_' + str(currOrder.id) + '.pdf', "rb")))
    currOrder.save()
    os.remove(settings.MEDIA_ROOT + '\\Bill_' + str(currOrder.id) + '.pdf')