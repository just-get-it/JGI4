from django.conf import settings
import pdfkit
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
                    word-spacing: normal;
                    position: relative; 
                    margin: 0 auto; 
                    color: #001028;
                    background: #ffffff; 
                    font-family: Arial, sans-serif; 
                    font-size: 12px; 
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
                    margin-right: 10px;
                    width:
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
                        <img src="./logo.png">
                            <h3>Rental Order Bill</h3>
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
    order_det = '<div id="project"><div><span>RENTAL ORDER ID:</span> &nbsp; ' + str(currOrder.id) + ' </div><div><span>PAYMENT : </span>'+ currOrder.payment_method  +'</div><div><span>CLIENT: </span>'+ currOrder.customer.name  +'</div><div><span>ADDRESS: </span> '+ odItems[0].shipping_address.shipping_address + ', ' + odItems[0].shipping_address.state  + ', ' + odItems[0].shipping_address.city  + ' - ' + odItems[0].shipping_address.pin_code  + '.</div><div><span>DATE: </span> '+ currOrder.date_rental_placed.strftime("%m/%d/%Y, %H:%M") +'</div></div>'
    table_header = """</header>
                        <main>
                        <table>
                            <thead>
                            <tr>
                                <th class="desc">PRODUCT</th>
                                <th class="service">SELLER</th>
                                <th class="service">START DATE</th>
                                <th class="service">END DATE</th>
                                <th>SIZE COLOR</th>
                                <th>QUANTITY</th>
                                <th>TOTAL SECURITY DEPOSIT</th>
                                <th>TOTAL CHARGES</th>
                            </tr>
                            </thead>
                            <tbody>"""
    bill_html = temp_start + order_det + table_header
    for item in odItems:
        if not item.is_Cancelled:
            bill_html += '<tr><td class="desc">'+ item.product.title +'</td><td class="service">'+ item.product.seller.name +'</td><td class="service">'+ item.start_date.strftime("%m/%d/%Y") +'</td><td class="service">'+ item.end_date.strftime("%m/%d/%Y") +'</td><td ><p style="display:inline; text-align:center">'+ str(item.size_color_quantity.size)+'<span style="background:'+item.size_color_quantity.color+'; margin-left:5px; height: 15px; border: 2px solid black; border-radius:50%; width:15px; display:inline-block;"> </span> </p>'+'</td><td class="qty">' + str(item.quantity) +'</td><td class="total">Rs.'+ str(item.get_total_price()) +'</td><td class="total">Rs.'+ str(item.get_total_amount()) +'</td></tr>'
        else:
            bill_html += '<tr style="text-decoration:line-through;"><td class="desc" >'+ item.product.title +'</td><td class="service">'+ item.product.seller.name +'</td><td class="service">'+ item.start_date.strftime("%m/%d/%Y") +'</td><td class="service">'+ item.end_date.strftime("%m/%d/%Y") +'</td><td ><p style="display:inline; text-align:center">'+ str(item.size_color_quantity.size)+'<span style="background:'+item.size_color_quantity.color+'; margin-left:5px; height: 15px; border: 2px solid black; border-radius:50%; width:15px; display:inline-block;"> </span> </p>'+'</td><td class="qty">' + str(item.quantity) +'</td><td class="total">Rs.'+ str(item.get_total_price()) +'</td><td class="total">Rs.'+ str(item.get_total_amount()) +'</td></tr>'
    # here mov is 10000
    if currOrder.chargable_amount < 10000 and currOrder.is_Cancelled == False:
        bill_html += '<tr><td colspan="8">Delivery Charges*: Rs. 101</td></tr>'
    
    bill_html += '<tr><td colspan="8">TOTAL CHARGEABLE AMOUNT: Rs. '+ str(currOrder.chargable_amount) +'</td></tr>'
    bill_html += '<tr style="border-top: 1px solid grey;"><td colspan="8">TOTAL SECURITY PAYABLE AMOUNT: Rs. '+ str(currOrder.security_amount) +'</td></tr>'
    bill_html += '<tr style="border-top: 1px solid grey;"><td colspan="8">REFUNDABLE AMOUNT: Rs. '+ str(currOrder.get_refund_amount()) +'</td></tr>'
    bill_html += temp_end
    if os.path.exists(settings.MEDIA_ROOT+ '\local\rental\invoices\RentBill_' + str(currOrder.id) + '.pdf'):
            os.remove(settings.MEDIA_ROOT+'\local\rental\invoices\RentBill_' + str(currOrder.id) + '.pdf')
    # file=open(settings.MEDIA_ROOT + '\\RentBill_' + str(currOrder.id) + '.pdf','w+b')
    # pisa_status = pisa.CreatePDF(
    #     bill_html,
    #     dest=file)
    
    # file.close()
    path = os.path.join(settings.MEDIA_ROOT+ '\local\rental\invoices\RentBill_' + str(currOrder.id) + '.pdf')
    pdfkit.from_string(bill_html, settings.MEDIA_ROOT+'\\RentBill_' + str(currOrder.id) + '.pdf')
    currOrder.invoice.save('RentBill_' + str(currOrder.id) + '.pdf', File(open(settings.MEDIA_ROOT + '\\RentBill_' + str(currOrder.id) + '.pdf', "rb")))
    currOrder.save()
    os.remove(settings.MEDIA_ROOT + '\\RentBill_' + str(currOrder.id) + '.pdf')