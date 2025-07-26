import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import os

MY_EMAIL = os.environ["FROM_EMAIL_ADDRESS"]
PASSWORD = os.environ["FROM_EMAIL_PASSWORD"]
product_url = "https://ubranesklep.pl/produkt/7854/spodnie-nico-kokos"
size = "S"

response = requests.get(product_url)
html = response.text

soup = BeautifulSoup(html, "html.parser")
option = soup.select_one("select#inventory_id > option")
title = soup.select_one("article.article-product > h1")

msg = EmailMessage()
msg["From"] = MY_EMAIL
msg["To"] = "klaudiaorasinska@gmail.com"

def send_mail_product_not_available(msg):
    msg["Subject"]= "Produkt został usunięty!"
    msg.set_content(f"Produkt na który czekasz {product_url} został usunięty ze strony :(")
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.send_message(msg=msg)

def send_mail_product_available(msg):
    msg["Subject"]  = "Produkt znów dostępny!"
    msg.set_content(f"Produkt na który czekasz {title.text} w rozmiarze {size} znów jest dostępny w sprzedaży!<3\nLINK: {product_url}")
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.send_message(msg=msg)

def send_mail_size_not_available(msg):
    msg["Subject"] = "Produkt nie jest dostępny w tym rozmiarze!"
    msg.set_content(f"Produkt na który czekasz {title.text} nie jest dostępny w rozmiarze {size}.\nLINK: {product_url}")
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.send_message(msg=msg)


if title is not None:
    if option is not None:
        if size not in option.text:
            send_mail_product_available(msg)
        else:
            send_mail_size_not_available(msg)
    else:
         send_mail_product_available(msg)
else:
    send_mail_product_not_available(msg)








