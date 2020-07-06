import requests
from bs4 import BeautifulSoup
import smtplib
import time
import datetime
from csv import writer
import os

URL = 'https://www.beatsbydre.com/ca/headphones'


headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


# headphones class
class Headphones:
    """
    headphones
    """
    title: str
    price: float
    wish_price: float

    def __init__(self, title: str, price: float, wish_price: float) -> None:

        self.title = title
        self.wish_price = wish_price
        self.price = price

    def __str__(self):
        return '{} for {}'.format(self.title, self.price)


def check_price():
    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, 'html.parser')

    headphones_list = []

    # get the title and price of each headphone
    for i in soup1.find_all("div", class_="content"):
        title = i.find('h2').get_text()
        price = float(i.find('div', class_='price-holder').get_text().strip()[1:])

        # add the new headphone to list of headphones and wish price depending on headphone
        if title == 'Solo Pro':
            headphones_list.append(Headphones(title, price, 350.00))
        elif title == 'Beats Studio3 Wireless':
            headphones_list.append(Headphones(title, price, 375.00))
        elif title == 'Beats Solo3 Wireless':
            headphones_list.append(Headphones(title, price, 225.00))
        elif title == 'Beats EP':
            headphones_list.append(Headphones(title, price, 100.00))
        elif title == 'Beats Pro':
            headphones_list.append(Headphones(title, price, 400.00))


    # create a list of all the preset wish prices

    #wish_prices = \
       # [350.00,       375.00,                225.00,         100.00,   400.00]
    # Solo Pro | BeatsStudio3Wireless | BeatsSolo3Wireless | Beats EP | BeatsPro

    # add the preset wish prices to the headphones objects in list
    # for i in range(len(headphones_list)):
    #     headphones_list[i].wish_price = wish_prices[i]

    # append to csv
    with open("/Users/stephanmotha/Documents/pythonProjects/beatsScraper/beats_prices.csv", 'a') as csv_file:
        filesize = os.path.getsize("/Users/stephanmotha/Documents/pythonProjects/beatsScraper/beats_prices.csv")

        csv_writer = writer(csv_file)
        headings = ['Name', "Price ($CAD)", "Wish Price (%CAD)", "Date"]

        # if file is empty add the headings, else add empty row
        if filesize == 0:
            csv_writer.writerow(headings)
        else:
            csv_writer.writerow([])

        # add row for all the headphones in the list
        for i in headphones_list:  # 5
            csv_writer.writerow([i.title, i.price, i.wish_price, datetime.datetime.now()])

    # print all the headphone objects
    for i in headphones_list:
        print(i)

    # check if any prices are below or equal to any wish prices
    for i in headphones_list:
        if i.price <= i.wish_price:
            send_mail(i.title)


def send_mail(title: str):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('stephan.motha26@gmail.com', 'thevin1002')

    subject = 'The Price for {} Headphones Dropped!'.format(title)

    body = 'https://www.beatsbydre.com/ca/headphones'
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'stephan.motha26@gmail.com',
        'aminishrimp@live.ca',
        msg

     )

    print("EMAIL SENT")

    server.quit()


while True:
    check_price()
    time.sleep(86400)
