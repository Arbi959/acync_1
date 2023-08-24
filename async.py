import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import aiohttp
import asyncio

product_brand_list = []
# product_notes_list = []
product_likes_list = []
async def get_page_data(session, edit_page, number_page):

    result_page = edit_page + str(number_page)
    async with session.get(url=result_page) as response:
        response_text = await response.text()
    # # with open('index2.html', 'w', encoding='utf-8') as file:
    # #     file.write(response)
    # with open('index2.html', 'r', encoding='utf-8') as file:
    #     response = file.read()
        soup = BeautifulSoup(response_text, 'lxml')
        products = soup.find_all('div', class_='hero_item_detailed')

        for a in products:
            brand = a.find('p').find('a').text
            likes = a.find('p', class_='text small light').find_all('span')[0].text.strip()
            product_brand_list.append(brand)
            product_likes_list.append(likes)
    print(f'[*] Obrabotanno stranic{number_page}')

async def gather_data():
    url = 'https://fanfics.me/fandom46/heroes'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)


        soup = BeautifulSoup(await response.text(), 'lxml')
        page_url = soup.find('div', class_='paginator').find_all('a')[1]['href'].split('=')[0] + '='
        count_page = soup.find('div', class_='paginator').find_all('a')[-1].text
        edit_page = 'https://www.audible.com' + page_url
        tasks = []
        for i in range(1, int(count_page) + 1):
            task = asyncio.create_task(get_page_data(session, edit_page, i))
            tasks.append(task)
        await asyncio.gather(*tasks)

def main():
    print('main')
    asyncio.run(gather_data())
    print('end main')
    df = pd.DataFrame({'brand': product_brand_list,
                       'price': product_likes_list})
    df.to_csv('result.csv', mode='a', index=False, header=True)

if __name__ == '__main__':
    main()
