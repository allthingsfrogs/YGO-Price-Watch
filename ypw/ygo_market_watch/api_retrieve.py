#from urllib.request import Request, urlopen
import requests
from ygo_market_watch.models import Card
from django.core.files.base import ContentFile
from datetime import datetime

#get card info from YugiohPrices API using card's name, store in DB
def fetch_card_info(card_name):

    url = f'http://yugiohprices.com/api/get_card_prices/{card_name}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for item in data['data']:
            price_data = item.get('price_data', {})
            prices = price_data.get('data', {}).get('prices', {})
            high_price = prices.get('high', 0.0) 
            low_price = prices.get('low', 0.0)
            average = prices.get('average', 0.0)
            shift = prices.get('shift', 0.0)
            shift_3 = prices.get('shift_3', 0.0)
            shift_7 = prices.get('shift_7', 0.0)
            shift_30 = prices.get('shift_30', 0.0)
            shift_90 = prices.get('shift_90', 0.0)
            shift_180 = prices.get('shift_180', 0.0)
            shift_365 = prices.get('shift_365', 0.0)
            updated_at = prices.get('updated_at', '2013-07-19 21:07:11 -0600')

            Card.objects.create(
            Card_name = card_name,
            name_of_set = item.get('name'),
            print_tag = item.get('print_tag'),
            rarity = item.get('rarity'),
            high_price = high_price,
            low_price = low_price,
            average_price = average,
            shift = shift,
            shift_3 = shift_3,
            shift_7 = shift_7,
            shift_30 = shift_30,
            shift_90 = shift_90,
            shift_180 = shift_180,
            shift_365 = shift_365,
            updated_at = updated_at,
            )   
         
        print('Card info fetched and saved successfully')
    else:
        print('Failed to fetch card info')
        
#get card info from YugiohPrices API using card's tag, store in DB
def fetch_card_print_tag(print_tag):

    url = f'http://yugiohprices.com/api/price_for_print_tag/{print_tag}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        card_data = data.get('data', {})
        if card_data:
            name = card_data.get('name')
            price_data = card_data.get('price_data', {})
            if price_data:
                set_info = price_data.get('data', {})
                if set_info:
                    prices = set_info.get('prices', {})
                    high_price = prices.get('high', 0.0)
                    low_price = prices.get('low', 0.0)
                    average = prices.get('average', 0.0)
                    shift = prices.get('shift', 0.0)
                    shift_3 = prices.get('shift_3', 0.0)
                    shift_7 = prices.get('shift_7', 0.0)
                    shift_30 = prices.get('shift_30', 0.0)
                    shift_90 = prices.get('shift_90', 0.0)
                    shift_180 = prices.get('shift_180', 0.0)
                    shift_365 = prices.get('shift_365', 0.0)
                    updated_at_str = prices.get('updated_at', '2013-11-14 13:12:06 -0700')

                    # Convert the updated_at string to a datetime object
                    updated_at = datetime.strptime(updated_at_str, '%Y-%m-%d %H:%M:%S %z')

                    Card.objects.create(
                        Card_name=name,
                        name_of_set=set_info.get('name'),
                        print_tag=set_info.get('print_tag'),
                        rarity=set_info.get('rarity'),
                        high_price=high_price,
                        low_price=low_price,
                        average_price=average,
                        shift=shift,
                        shift_3=shift_3,
                        shift_7=shift_7,
                        shift_30=shift_30,
                        shift_90=shift_90,
                        shift_180=shift_180,
                        shift_365=shift_365,
                        updated_at=updated_at,
                    )

                    print('Card info fetched and saved successfully')
                else:
                    print('Failed to fetch set info')
            else:
                print('Failed to fetch price data')
        else:
            print('Failed to fetch card data')
    else:
        print('Failed to fetch card info')

def fetch_card_image(card_name):
    #check if the card image is in DB 
    card = Card.objects.filter(Card_name__icontains=card_name).first()

    #if it doesnt exist or if the image field is empty, use API call to put card/image in DB
    if card is None or not card.card_image:
        #put card in DB
        fetch_card_info(card_name)

    #rest of code puts image in DB
    url = f'http://yugiohprices.com/api/card_image/{card_name}'
    response = requests.get(url)
    #save it do DB, return image data so it can pass it to variable in views.getUserCard
    if response.status_code == 200:
        card = Card.objects.filter(Card_name__icontains=card_name).first()
        if card:
            card.card_image.save(f'{card_name}_image.jpeg', ContentFile(response.content), save=True)
            image_url = card.card_image.url
            return image_url
    #####
    #check if card is using default image, if it is then save, if not then just retrieve image url for the card    
    #####