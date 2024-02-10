# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas as pd

LOGGER = get_logger(__name__)

def get_hakan():
    r = rq.get('https://www.hakandoviz.com/canli-veri/')
    soup = BeautifulSoup(r.content, 'html.parser')
    rows = soup.select('tbody tr')
    row = next((element for element in rows if "USD/TRY" in element.text),None)
    hakan_bid = row.find('span', class_='USD/TRY buy').text.strip().replace(',','.')
    hakan_ask = row.find('span', class_='USD/TRY sell').text.strip().replace(',','.')
    return ['Hakan Döviz', hakan_bid, hakan_ask]
    
def get_nadir():
    r1=rq.get('https://www.nadirdoviz.com/mobil/')
    soup1 = BeautifulSoup(r1.content, 'html.parser')
    rows1 = soup1.select('tbody tr')
    row1 = next((element for element in rows1 if "USD/TL" in element.text),None)
    nadir = row1.find_all('td',class_='fadg')
    nadir_bid =nadir[0].text.strip().replace(',','.')
    nadir_ask =nadir[1].text.strip().replace(',','.')
    return ['Nadir Döviz',nadir_bid, nadir_ask]

def get_atlas():
    r2=rq.get('http://www.atlasdoviz.com/')
    soup2 = BeautifulSoup(r2.content, 'html.parser')
    rows2 = soup2.find('div', class_='arka').text.strip()
    atlas = re.split(r'\D+', rows2)
    atlas_bid = atlas[1]+'.'+atlas[2]
    atlas_ask = atlas[3]+'.'+atlas[4]
    return ['Atlas Döviz', atlas_bid, atlas_ask]

def get_all():
    df = pd.DataFrame(columns=pd.Index(['Büro','Alış','Satış']), index=None)
    df.loc[0]=get_hakan()
    df.loc[1]=get_atlas()
    df.loc[2]=get_nadir()
    df = df.set_index('Büro')
    return df



def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )
    df = get_all()
    print(df)
    st.write(df)

    st.sidebar.success("")

    st.markdown('')


if __name__ == "__main__":
    run()
