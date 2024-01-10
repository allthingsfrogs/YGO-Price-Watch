import requests
from ygo_market_watch.models import Card
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .api_retrieve import fetch_card_info, fetch_card_print_tag, fetch_card_image
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
#from django.db.models import Q

def start_page(request):
#get data for all cards, pass into template for start_page
    #data_from_database = Card.objects.all()
    
    #get data for cards marked as favorite, dispaly on home page
    data_from_database = Card.objects.filter(is_favorite=True)
    context = {'data': data_from_database}
    template = loader.get_template('ygo_market_watch/start_page.html')
    return HttpResponse(template.render(context, request))

#calls script in api_retrieve.py to fetch card info from API database, using card's name
@csrf_exempt
def getCardAPI(self, card_name): #was "user_card"
    result = fetch_card_info(card_name)
    return HttpResponse('Card info updated.')


#calls script in api_retrieve.py to fetch card info from API database, using print_tag
@csrf_exempt
def getCardTagAPI(self, print_tag):
    result = fetch_card_print_tag(print_tag)
    return HttpResponse('Card info updated.')


@csrf_exempt
def getFavCards(request):
    # Query DB to get all cards user has favorited (is_favorite=True)
    favorite_cards = Card.objects.filter(is_favorite=True)
    # Pass queried cards to the template
    context2 = {'favorite_cards': favorite_cards}
    return render(request, 'ygo_market_watch/start_page.html', context=context2)


#calls script in api_retrieve.py to fetch card image
@csrf_exempt
def getImageAPI(self, card_name):
    result = fetch_card_image(card_name)
    return HttpResponse('Card info updated.')


# instead of constanly calling api, we can periodically use getCardAPI to update DB
def getUserCard(request):
    query = request.GET.get('q')
    card_name = ''
    #check current time vs updated time on object, update price depending on desired time 
    if query:
        #check if user searched by print_tag and if this exists in DB, pass to HMTL
        if Card.objects.filter(print_tag = query).exists():
            card_object = Card.objects.filter(print_tag = query)
            inter = card_object.first()
            card_name = inter.Card_name
        #check if user searched by card_name and if this exists in DB, pass to HTML
        elif Card.objects.filter(Card_name__icontains=query).exists():
            card_object = Card.objects.filter(Card_name__icontains=query)
            card_name = query
        
        #if it doesnt exist in DB, check how user queried for card and use API call to put into DB
        #THEN gather data to pass to HTML through context
        else:
            #if user queried via print tag
            if all(char.isupper() or char.isdigit() or char == '-' for char in query):
                fetch_card_print_tag(query)
                card_object = Card.objects.filter(print_tag = query)
                inter = card_object.first()
                card_name = inter.Card_name
            #if user queried via card name
            else:
                fetch_card_info(query)
                card_object = Card.objects.filter(Card_name__icontains = query)
                card_name = query
    else:
        card_object = None

    #get image data, pass into HTML context along with card object
    image = fetch_card_image(card_name)
    context = {
        'card' : card_object,
        'card_name' : card_name,
        'card_image' : image      
    }
    return render(request, 'ygo_market_watch/search_result.html', context=context)


def makeFavCard(request):
    if request.method == 'POST':
        print_tag = request.POST.get('print_tag', '')
        card_object = get_object_or_404(Card, print_tag = print_tag)
        # Toggle the is_favorite boolean field
        card_object.is_favorite = not card_object.is_favorite
        card_object.save()

    return HttpResponseRedirect(reverse('start_page'))