import requests
from bs4 import BeautifulSoup
import json
import csv

url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
    'accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
#
# req = requests.get(url, headers=headers)
# src = req.text
#  print(src)
#
# with open('index.html', 'w') as file:
#     file.write(src)
#
    # with open('index.html') as file:
    #     src = file.read()

# soup = BeautifulSoup(src, 'lxml')
# all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")
#
# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#     # print(f'{item_text}: {item_href}')
#
#     all_categories_dict[item_text] = item_href
#
# with open('all_categories_diet.json', 'w') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open('all_categories_diet.json') as file:
    all_categories = json.load(file)

# print(all_categories)

count = 0

for category_name, category_href in all_categories.items():

    if count == 0:
        rep = [',',' ','-', "'"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, '_')
        # print(category_name)

        req = requests.get(url=category_href, headers=headers)
        src = req.text

        with open(f'data/{count}_{category_name}.html', 'w') as file:
            file.write(src)

        with open(f'data/{count}_{category_name}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
        # print(table_head)
        products = table_head[0].text
        calories = table_head[1].text
        proteins = table_head[2].text
        fats = table_head[3].text
        carbohydrates = table_head[4].text
        # print(carbohydrates)

        with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    products,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

        products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

        for item in products_data:
            products_tds = item.find_all('td')

            title = products_tds[0].find('a').text
            # print(title)
            calories = products_tds[1].text
            proteins = products_tds[2].text
            fats = products_tds[3].text
            carbohydrates = products_tds[4].text

            # print(proteins)

            with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )


        count += 1