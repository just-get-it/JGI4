from django.conf import settings
from xhtml2pdf import pisa
from django.core.files import File
import os

def sub_bill(bill,subOrder,orders,odItems ):
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

    if subOrder.payment_method == "prepaid":
        temp_end = '''  
                        <tr>
                            <th colspan=5>
                                <h6>Final Amount deducted: </h6> Rs. '''+str(bill.final_amount)+'''
                            </th>
                        </tr>
                        </tbody>
                        </table>
                        </main>
                        <footer>
                        Invoice was created on a computer and is valid without the signature and seal.
                        <hr>
                        </footer>
                    </body>
                    </html>'''
    else:
        temp_end = '''  
                    <tr>
                        <th colspan=5>
                            <h6>Final Amount to be paid: </h6> Rs. '''+str(bill.final_amount)+'''
                        </th>
                    </tr>
                    </tbody>
                    </table>
                    </main>
                    <footer>
                    Invoice was created on a computer and is valid without the signature and seal.
                    <hr>
                    </footer>
                </body>
                </html>'''
   
    i=0
    bill_html=temp_start
    order_det = '<div id="project"><div><span>SUB ORDER ID: </span>' + str(subOrder.id) + '</div><div><span>PAYMENT : </span>'+ subOrder.payment_method  +'</div><div><span>CLIENT: </span>'+ subOrder.customer.name  +'</div><div><span>ADDRESS: </span> '+ odItems[0][0].shipping_address.shipping_address + ', ' + odItems[0][0].shipping_address.state  + ', ' + odItems[0][0].shipping_address.city  + ' - ' + odItems[0][0].shipping_address.pin_code  + '.</div></div>'
    bill_html += order_det
    while(i<len(orders)):
       
        table_header = """</header>
                        <main>
                        <table>
                            <thead>
                            <tr>
                                <th colspan=5> Order ID -"""+ str(orders[i].id) +""" </th>
                            </tr>
                            <tr>
                                <td colspan=5> <div><span>DATE: </span> """+ orders[i].date_order_placed.strftime("%m/%d/%Y, %H:%M") +"""</div> </td>
                            </tr>
                            <tr>
                                <th class="desc">PRODUCT</th>
                                <th class="service">SELLER</th>
                                <th>SIZE</th>
                                <th>QUANTITY</th>
                                <th>TOTAL</th>
                            </tr>
                            </thead>
                            <tbody>"""
        bill_html += table_header
        item = odItems[i]
        for obj in item:
            if not obj.is_Cancelled:
                bill_html += '<tr><td class="desc">'+ obj.product_name +'</td><td class="service">'+ obj.seller_name +'</td><td class="unit">'+ obj.size_name +'</td><td class="qty">' + str(obj.quantity) +'</td><td class="total">Rs.'+ str(obj.total) +'</td></tr>'
            else:
                bill_html += '<tr style="text-decoration:line-through;"><td class="desc" >'+ obj.product_name +'</td><td class="service">'+ obj.seller_name +'</td><td class="unit">'+ obj.size_name +'</td><td class="qty">' + str(obj.quantity) +'</td><td class="total">Rs.'+ str(obj.total) +'</td></tr>'
        # here mov is 10000
        if orders[i].total < 10000 and orders[i].is_Cancelled == False:
            bill_html += '<tr><td colspan="3"></td><td>Delivery Charges*:</td><td class="total">Rs. 101</td></tr>'
        bill_html += '<tr style="border-top: 1px solid grey;"><td colspan="3"></td><td>TOTAL:</td><td class="total">Rs. '+ str(orders[i].total) +'</td></tr>'
        i=i+1
    bill_html += temp_end
    if os.path.exists(settings.MEDIA_ROOT+ '\local\subscriptions\invoices\Bill_' + str(bill.id) + '.pdf'):
            os.remove(settings.MEDIA_ROOT+'\local\subscriptions\invoices\Bill_' + str(bill.id) + '.pdf')
    file=open(settings.MEDIA_ROOT + '\\Bill_' + str(bill.id) + '.pdf','w+b')
    pisa_status = pisa.CreatePDF(
        bill_html,
        dest=file)
    file.close()
    print("bill created")
    bill.bill.save('Bill_' + str(bill.id) + '.pdf', File(open(settings.MEDIA_ROOT + '\\Bill_' + str(bill.id) + '.pdf', "rb")))
    bill.save()
    print("bill saved")
    os.remove(settings.MEDIA_ROOT + '\\Bill_' + str(bill.id) + '.pdf')