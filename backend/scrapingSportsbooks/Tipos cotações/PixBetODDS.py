import os
import re
import time
from time import sleep
import bs4
from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer

add_printer(1)


def obter_dataframe(query=""):
    df = pd.DataFrame()
    while df.empty:
        df = get_df(
            driver,
            By,
            WebDriverWait,
            expected_conditions,
            queryselector=query,
        )
    return df


# df.loc[df.aa_innerText.str.contains('Curry|Raphinha', na = False, regex= True)]

driver = Driver(uc=True)
driver.get("https://pix.bet.br/sports")

pasta = r'\odds_pixbet'
os.makedirs(pasta, exist_ok=True)

while True:
    try:
        df = obter_dataframe('div.eventlist_eu_fe_EventItemDesktop_wrapper')
        df
        df1 = (df.aa_innerHTML.apply(bs4.BeautifulSoup).apply(
            lambda soup: [x.text.strip() for x in soup.find_all('span', class_='eventlist_eu_fe_EventInfo_teamNameText')] + [
                                                                                                                                x.text.strip()
                                                                                                                                for
                                                                                                                                x
                                                                                                                                in
                                                                                                                                soup.find_all(
                                                                                                                                    'span',
                                                                                                                                    class_='eventlist_eu_fe_Selection_odds')][
                                                                                                                            :3]).apply(
            lambda q: q if len(q) == 5 else pd.NA).dropna().apply(
            lambda x: x if all([re.match(r'^|\d+\.\d+$', y) for y in x[2:]]) else pd.NA).dropna().apply(pd.Series)).rename(
            columns={0: 'Time1_nome', 1: 'Time2_nome', 2: 'Time1', 3: 'Empate', 4: 'Time2'}).astype(
            {'Time1': 'Float64', 'Empate': 'Float64', 'Time2': 'Float64'}).reset_index(drop=True)
        nome_arquivo = os.path.join(pasta, str(time.time()) + '.csv')
        print(nome_arquivo)
        df1.to_csv(nome_arquivo, index = False)
    except Exception as e:
        print(e)