import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import os

MY_EMAIL = os.environ["FROM_EMAIL_ADDRESS"]
PASSWORD = os.environ["FROM_EMAIL_PASSWORD"]
product_url = "https://ubranesklep.pl/produkt/7740/spodnie-nico"
size = "S"

response = requests.get(product_url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

option = soup.select_one("select#inventory_id > option")


msg = EmailMessage()
msg["Subject"] = "Produkt znów dostępny!"
msg["From"] = MY_EMAIL
msg["To"] = "klaudiaorasinska@gmail.com"
msg.set_content(f"Produkt na który czekasz w rozmiarze {size} znów jest dostępny w sprzedaży!<3\nLINK: {product_url}")

if not option or size not in option:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.send_message(
            from_addr=MY_EMAIL,
            to_addrs="klaudiaorasinska@gmail.com",
            msg=msg)





