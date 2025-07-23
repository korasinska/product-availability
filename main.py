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
print(title)

msg = EmailMessage()
msg["From"] = MY_EMAIL
msg["To"] = "klaudiaorasinska@gmail.com"

try:
    subject = "Produkt znów dostępny!"
    msg.set_content(f"Produkt na który czekasz {title.text} w rozmiarze {size} znów jest dostępny w sprzedaży!<3\nLINK: {product_url}")
except AttributeError:
    subject = "Produkt został usunięty!"
    msg.set_content(f"Produkt na który czekasz {product_url} został usunięty ze strony :(")

msg["Subject"] = subject

if not option or size not in option:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.send_message(
            from_addr=MY_EMAIL,
            to_addrs="klaudiaorasinska@gmail.com",
            msg=msg)




