import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import os

MY_EMAIL = os.environ["FROM_EMAIL_ADDRESS"]
PASSWORD = os.environ["FROM_EMAIL_PASSWORD"]
product_url = "https://ubranesklep.pl/produkt/7854/spodnie-nico-kokos"
size = "Rozmiar - S"

try:
    response = requests.get(product_url)
    response.raise_for_status()
    html = response.text
except Exception as e:
    print(f"Błąd przy pobieraniu strony: {e}")

soup = BeautifulSoup(html, "html.parser")
options = soup.select("select#inventory_id > option")
sizes = [opt.text for opt in options]
title = soup.select_one("article.article-product > h1")

def send_mail(subject, content):
    msg = EmailMessage()
    msg["From"] = MY_EMAIL
    msg["To"] = "klaudiaorasinska@gmail.com"
    msg["Subject"]= subject
    msg.set_content(content)
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.send_message(msg=msg)

if title is not None:
    if options is not None:
        if size not in sizes:
            send_mail("Produkt znów dostępny!", f"Produkt na który czekasz {title.text} w rozmiarze {size} znów jest dostępny w sprzedaży!<3\nLINK: {product_url}")
        else:
            send_mail("Produkt nie jest dostępny w tym rozmiarze!", f"Produkt na który czekasz {title.text} nie jest dostępny w rozmiarze {size}.\nLINK: {product_url}")
    else:
         send_mail("Produkt znów dostępny!", f"Produkt na który czekasz {title.text} w rozmiarze {size} znów jest dostępny w sprzedaży!<3\nLINK: {product_url}")
else:
    send_mail("Produkt został usunięty!", f"Produkt na który czekasz {product_url} został usunięty ze strony :(")








