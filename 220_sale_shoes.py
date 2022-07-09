import requests, json

def get_json():
    url = 'https://api.nike.com/cic/browse/v2?queryid=products&country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(0f64ecc7-d624-4e91-b171-b83a03dd8550%2C16633190-45e5-4830-a068-232ac7aea82c%2C5b21a62a-0503-400c-8336-3ccfbff2a684)%26anchor%3D0%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
    r = requests.get(url)

    with open('data/1.json', 'w', encoding='utf-8') as file:
        json.dump(r.json(), file, indent=4, ensure_ascii=False)

def get_pages_number():
    url = 'https://api.nike.com/cic/browse/v2?queryid=products&country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(0f64ecc7-d624-4e91-b171-b83a03dd8550%2C16633190-45e5-4830-a068-232ac7aea82c%2C5b21a62a-0503-400c-8336-3ccfbff2a684)%26anchor%3D0%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'

    r = requests.get(url)
    response = r.json()

    return response['data']['products']['pages']['totalPages']

def get_data():
    data = []
    count = 1
    last_page = get_pages_number() * 24 - 24

    for i in range(0, last_page + 1, 24):
        url = f'https://api.nike.com/cic/browse/v2?queryid=products&country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(0f64ecc7-d624-4e91-b171-b83a03dd8550%2C16633190-45e5-4830-a068-232ac7aea82c%2C5b21a62a-0503-400c-8336-3ccfbff2a684)%26anchor%3D{i}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'

        r = requests.get(url)
        JSON = r.json()

        products = JSON['data']['products']['products']

        for product in products:
            title = product['title']
            subtitle = product['subtitle']
            href = ('https://www.nike.com/' + product['url']).replace('{countryLang}/', '')

            main_color = []

            color_description = product['colorDescription']
            image = product['images']['portraitURL']
            sale_price = str(product['price']['currentPrice']) + ' $'
            full_price = str(product['price']['fullPrice']) + ' $'

            main_color.append({'1':{
                'color_description': color_description,
                'href': href,
                'image': image,
                'sale_price': sale_price,
                'full_price': full_price
            }})

            other_colorways = []
            colorway_num = 2

            for colorway in product['colorways']:
                color_description_colorway = colorway['colorDescription']
                image_colorway = colorway['images']['portraitURL']
                sale_price_colorway = str(colorway['price']['currentPrice']) + ' $'
                full_price_colorway = str(colorway['price']['fullPrice']) + ' $'

                other_colorways.append({f'{colorway_num}': {
                    'color_description': color_description_colorway,
                    'image': image_colorway,
                    'sale_price': sale_price_colorway,
                    'full_price': full_price_colorway
                }})

                colorway_num += 1

            data.append({
                'title': title,
                'subtitle': subtitle,
                'href': href,
                'colorways': main_color + other_colorways
            })

            print(f'Number {count} was completed!')
            count += 1

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    get_data()

if __name__ == '__main__':
    main()








