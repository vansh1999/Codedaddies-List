from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models
# Create your views here.


BASE_CRAGSLIST_URL = 'https://github.com/search?q={}&type=Users'
# BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):

    return render(request , 'base.html')

def new_search(request):

    search = request.POST.get('search')
    final_url = BASE_CRAGSLIST_URL.format(quote_plus(search))
    models.Search.objects.create(search=search)
    response = requests.get(final_url)
    data = response.text

    print(final_url)
    soup = BeautifulSoup(data , features='html.parser')

    users = soup.find("div", {"id": "user_search_results"})
    list_get = users.find("div", {"class": "user-list"})

    user_list = list_get.find_all(class_="user-list-item")

    # user_name = [name.find(class_="f4").get_text() for name in user_list]
    # user_title = [title.find(class_="f5").get_text() for title in user_list]
    final_posting = []

    for post in user_list:

        # user_name = post.find(class_ = "f4").get_text()
        # user_title = post.find(class_ = "f5").get_text()
        # # print(user_name)
        if post.find(class_ = "f4"):
            user_name = post.find(class_="f4").get_text()
        else:
            user_name = search

        if post.find(class_ = "f5"):
            user_title = post.find(class_="f5").get_text()
        else:
            user_title = search



        final_posting.append((user_name , user_title))



    stuff_for_frontend = {

        'search' : search ,
        'final_posting' : final_posting,
        'final_url' : final_url,


    }

    return render(request , 'my_app/new_search.html' , stuff_for_frontend)

