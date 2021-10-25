import DC_DELIVERY_LIBRARY as dc
import time

start_time = time.perf_counter()

ORDNUM_EMAILS_QTY_NAME = dc.nlFile_to_List('ORDNUM_EMAILS_QTY_NAME.txt')
product_list = dc.nlFile_to_List('LIST_MASTER.txt')
api_key = 'SENDGRIDAPIKEY'
from_email = "FROMEMAIL"
bcc_email = "BCCEMAIL"
dict25, dict50, dict100, dict200 = {}, {}, {}, {}
starting_qty = len(product_list)
product_name = "PRODUCTNAME"

#sorts order details into dictionaries based on quantity with key being order number and value being a tuple of email, name
for i in ORDNUM_EMAILS_QTY_NAME:
    quantity_text = i[2]
    if "25" in quantity_text:
        dict25[i[0]] = (i[1], i[3])
    if "50" in quantity_text:
        dict50[i[0]] = (i[1], i[3])
    if "100" in quantity_text:
        dict100[i[0]] = (i[1], i[3])
    if "200" in quantity_text:
        dict200[i[0]] = (i[1], i[3])

total_products_needed = len(dict25)*25 + len(dict50)*50 + len(dict100)*100 + len(dict200)*200
if total_products_needed > starting_qty:
    raise Exception("Not enough products to be delivered! Total products needed is: " +str(total_products_needed) +" products. Products list contains only: " + str(len(product_list)) + " products.")

#deliver orders:
for i in dict25:
    delivery_products = dc.pull_products(product_list, "LIST_DELIVERY.txt", 25)
    dc.send_Email(api_key, from_email, dict25[i][0], dict25[i][1], i, product_name, 25, bcc_email, delivery_products)
    time.sleep(1)
for i in dict50:
    delivery_products = dc.pull_products(product_list, "LIST_DELIVERY.txt", 50)
    dc.send_Email(api_key, from_email, dict50[i][0], dict50[i][1], i, product_name, 50, bcc_email, delivery_products)
    time.sleep(1)
for i in dict100:
    delivery_products = dc.pull_products(product_list, "LIST_DELIVERY.txt", 100)
    dc.send_Email(api_key, from_email, dict100[i][0], dict100[i][1], i, product_name, 100, bcc_email, delivery_products)
    time.sleep(1)
for i in dict200:
    delivery_products = dc.pull_products(product_list, "LIST_DELIVERY.txt", 200)
    dc.send_Email(api_key, from_email, dict200[i][0], dict200[i][1], i, product_name, 200, bcc_email, delivery_products)
    time.sleep(1)

dc.list_to_file(product_list, "LIST_REMAINING.txt")

remaining_qty = len(product_list)
end_time = time.perf_counter() - start_time

print("Delivery complete! " + str(starting_qty - remaining_qty) + " out of " + str(starting_qty) + " products have been delivered in " + str(end_time) + "s! The remaining " + str(remaining_qty) + " products are stored in LIST_REMAINING.txt")
