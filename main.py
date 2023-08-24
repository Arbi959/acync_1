import requests
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd

url = 'https://fanfics.me/fandom46/heroes'
# response = requests.get(url).text
# # with open('index.html', 'w', encoding='utf-8') as file:
# #     file.write(response.text)
with open('index.html', 'r', encoding='utf-8') as file:
    response = file.read()
soup = BeautifulSoup(response, 'lxml')
page_url = soup.find('div', class_='paginator').find_all('a')[1]['href'].split('=')[0]+'='
count_page = soup.find('div', class_='paginator').find_all('a')[-1].text
# print('https://fanfics.me' + page_url)
# print(count_page)
# for i in range(1, int(count_page) + 1):
for i in range(1,2):

    result_url = 'https://fanfics.me' + page_url + str(i)
    print(result_url)
    response = requests.get(result_url).text
    # with open('index2.html', 'w', encoding='utf-8') as file:
    #     file.write(response)
    # with open('index2.html', 'r', encoding='utf-8') as file:
    #     response = file.read()
    soup = BeautifulSoup(response, 'lxml')
    products = soup.find_all('div', class_='hero_item_detailed')
    product_brand_list =[]
    product_notes_list =[]
    product_likes_list =[]
    for a in products:
        brand = a.find('p').find('a').text
        print(brand)
        notes = a.find_all('p', class_='text')[-1].text.strip()
        print(notes)
        likes = a.find('p', class_='text small light').find_all('span')[0].text.strip()
        print(likes)
        product_brand_list.append(brand)
        product_notes_list.append(notes)
        product_likes_list.append(likes)

    df = pd.DataFrame({'brand': product_brand_list,
                        'notes': product_notes_list,
                        'likes': product_likes_list})
    df.to_csv('result.csv', mode='a', index=False, header=True)
    print(f'[*] Parsing stranici {i}/{count_page}')
    time.sleep(3)
df = pd.read_csv('result.csv')
print(df)