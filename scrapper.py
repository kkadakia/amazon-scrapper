import requests
from bs4 import BeautifulSoup
import smtplib
import time

# your amazon link
URL = 'your URL'

# send user-agent info
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}


def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    # to get the title of the product
    title = soup.find(id="productTitle").get_text()

    # gets the price of the product
    price = soup.find(id="priceblock_ourprice").get_text()

    # converts string to float
    converted_price = float(price[0:5])

    if converted_price < 'your desired number':
        send_email()


def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Extended HELO(EHLO) is an Extended Simple Mail Transfer Protocol(ESMTP) command sent by an email server
    # to identify itself while connecting to another email server to start the process of sending an email.
    server.ehlo()
    server.starttls()  # Turns existing insecure connection into a secure one
    server.ehlo()

    server.login('to@gmail.com', 'password')

    subject = 'Price fell down!'
    body = 'Check the amazon link %s' % URL

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'from@gmail.com',  # from email address
        'to@gmail.com',  # to email address
        msg
    )

    server.quit()


# checks every hour for change in the price
while True:
    check_price()
    time.sleep(60 * 60)

