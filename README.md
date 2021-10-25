# Email-Delivery
Program helpful in emailing a unique list of a master list of unique items, like gift card codes, discount codes, accounts, emails, etc. to individuals.

# How to Use
To start, you must have a SendGrid API key and an authorized domain or sender email. If you do not have either one, please go to https://sendgrid.com/.

Once you have obtained your SendGrid API key and your sender email, you can add them to DC_DELIVERY_SCRIPT.py. The variable that holds your API key is called "api_key" and the variable that holds your sender email is called "from_email". You also have to add an email to bcc under the variable "bcc_email" and the product name under the variable "product_name"

Input each respective Order Number, Email, Quantity, and Name in each row separated by tab. An easy way to ensure you have the right format is to put the information into 4 columns in Excel and then copy and pasting into ORDNUM_EMAILS_QTY_NAME.txt. ***Please make sure you do not have an empty row in this file***

Input the products that need to be delivered in LIST_MASTER.txt. There should be one product per row. The default quantities of products to be delivered are 25, 50, 100, and 200. You can add new quantities by initializing a new dictionary and change the quantities by editing the if statements in the first for loop in DC_DELIVERY_SCRIPT.py.

***Make sure to save the .txt files after editing them to ensure changes go through***
