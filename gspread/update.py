import re
import time

from urllib.request import urlopen

import gspread

from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

coolpc_url = 'http://www.coolpc.com.tw/evaluate.php'
ram_text = '記憶體 RAM'

auth_json_path = 'auth.json'

gss_scopes = ['https://spreadsheets.google.com/feeds']
spreadsheet_key_path = 'spreadsheet_key'


def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,
                                                                   scopes)
    return gspread.authorize(credentials)


def get_cheapest(url, text):
    with urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'lxml')

    cheapest_price = cheapest_item = None

    re_price = re.compile(r'\$(\d+)')
    root = soup.find('td', text=re.compile(text)).parent

    for option in root.find_all('option', text=re_price):
        item = option.text.strip()
        price = int(re_price.search(item).group(1))
        if cheapest_price is None or price < cheapest_price:
            cheapest_price = price
            cheapest_item = item

    return (cheapest_item, cheapest_price)


def update_sheet(gss_client, key, today, item, price):
    wks = gss_client.open_by_key(key)
    sheet = wks.sheet1
    sheet.insert_row([today, item, price], 2)


if __name__ == '__main__':
    (cheapest_item, cheapest_price) = get_cheapest(coolpc_url, ram_text)
    if cheapest_price is not None:
        today = time.strftime("%c")
        gss_client = auth_gss_client(auth_json_path, gss_scopes)
        with open(spreadsheet_key_path) as f:
            spreadsheet_key = f.read().strip()
        update_sheet(gss_client, spreadsheet_key, today, cheapest_item,
                     cheapest_price)
