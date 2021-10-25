import sendgrid
import os
from sendgrid.helpers.mail import *
import base64
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)


def nlFile_to_List(filename):
    """
    Assumes: filename is a txt file containing elements on each line. 
    Returns: if there is one element per line, a list of each element
    if there are multiple elements per line seperated by tab, a list of the tuples of the elements in filename
    """
    with open(filename) as f:
        elements_list = f.readlines()
    if len(elements_list) == 0:
        raise Exception("This is an empty file")
    for i in range(len(elements_list[:])):
        elements_list[i] = elements_list[i].strip()
    if "\t" in elements_list[0]:
        for i in range(len(elements_list[:])):
            elements_list[i] = tuple(elements_list[i].split("\t"))
    return(elements_list)

def list_to_file(list, filename):
    """
    Assumes a list and a file name
    Clears file and adds each element of list to a new line of the file
    """
    textfile = open(filename, "w")
    for i in list:
        textfile.write(i+"\n")
    textfile.close()
      
def pull_products(products_list, delivery_products_filename, quantity):
    """Assumes products_list (list) a list of products
    quantity (integer) number of products being delievered
    delivery_products_filename (string) name of file where delivery products will be stored
    Creates a list of products to be delivered, then deletes them from the master list
    Returns: name of txt file where delivery proxies are stored
    """
    delivery_products = products_list[0:quantity]
    del products_list[0:quantity]
    list_to_file(delivery_products, delivery_products_filename)
    return delivery_products_filename

def send_Email(api_key, from_email, to_email, name, order_number, product_name, quantity, bcc_email, products_list_filename):
    """Assumes: api_key (string) sendgrid api key
    from_email (string) from email address authorized on sendgrid 
    to_email (string) emailaddress
    name (string) name of customer
    order_number (string) order number
    quantity (int) number of proxies being delivered
    bcc_email (string) email address for bcc
    products_list_filename (string) file name of the products being delivered
    """
    sg = sendgrid.SendGridAPIClient(api_key)
    from_email = Email(from_email)
    to_email = To(to_email)
    subject = "Delivery! Order" + order_number
    content = Content("text/plain", "Hi " + name + "! Thank you for your purchase. Attached in the .txt file are your " + product_name + " x " + str(quantity) + ". You can copy them and start using them, but please also download the file and save it in a different place!")
    mail = Mail(from_email, to_email, subject, content)
    mail.add_bcc(bcc_email)
    with open(products_list_filename, 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()
    attachedFile = Attachment(FileContent(encoded_file), FileName(products_list_filename), FileType('application/txt'), Disposition('attachment'))
    mail.attachment = attachedFile
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)