import requests
from bs4 import BeautifulSoup
import random
import tweepy
import os
import sys
import time
sys.path.append("/Users/linakaval/Documents/Github/")
import example_auth_credentials #module with credentials

DOG_URL = 'https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals2.aspx?species=dog&gender=All&agegroup=All&location=&site=&onhold=All&orderby=ID&colnum=5&authkey=ho44bl6bmphbs21iior7k671v2gh2cf8r70636k2i7rcvs1br0&recAmount=&detailsInPopup=Yes&featuredPet=Include&stageID='
CAT_URL = 'https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals2.aspx?species=cat&gender=All&agegroup=All&location=&site=&onhold=All&orderby=ID&colnum=5&authkey=ho44bl6bmphbs21iior7k671v2gh2cf8r70636k2i7rcvs1br0&recAmount=&detailsInPopup=Yes&featuredPet=Include&stageID='
OTHER_URL = 'https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals2.aspx?species=other&gender=All&agegroup=All&location=&site=&onhold=All&orderby=ID&colnum=5&authkey=ho44bl6bmphbs21iior7k671v2gh2cf8r70636k2i7rcvs1br0&recAmount=&detailsInPopup=Yes&featuredPet=Include&stageID='

def getAnimals(url, animals):
    with requests.Session() as s:
        page = s.get(url)
        if page.status_code == 200:
            
            soup = BeautifulSoup(page.text, 'html.parser')
            divs  = soup.findAll("div", {'class': 'list-item'})
            #print(divs)

            for div in divs:
                name = div.find("div", {'class': 'list-animal-name'}).find('a').text
                species = div.find("div", {'class': 'list-anima-species'}).text
                sex = div.find("div", {'class': 'list-animal-sexSN'}).text
                breed = div.find("div", {'class': 'list-animal-breed'}).text
                age = div.find("div", {'class': 'list-animal-age'}).text
                picture = div.find("div", {'class': 'list-animal-photo-block'}).find("img")['src']
                #print(name, species, sex, breed, age)
                animals.append([name, species, sex, breed, age, picture])  


def main():
    cred = example_auth_credentials.twitter()

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(cred['CONSUMER_KEY'], cred['CONSUMER_SECRET'])
    auth.set_access_token(cred['ACCESS_TOKEN'], cred['ACCESS_TOKEN_SECRET'])

    # Create API object
    api = tweepy.API(auth)
    current_animals = []
    tempPic = 'temp_pic.jpg'

    getAnimals(DOG_URL, current_animals)
    getAnimals(CAT_URL, current_animals)
    getAnimals(OTHER_URL, current_animals)

    randomPet = current_animals[random.randint(0, len(current_animals))]

    with requests.Session() as s:
        pic = requests.get(randomPet[5], stream=True)
        if pic.status_code == 200:
            with open(tempPic, 'wb') as image:
                for chunk in pic.iter_content():
                    image.write(chunk)
            media_id = api.chunked_upload(tempPic).media_id
            api.update_status(status='CACHS Pet of the Day\nName: {}\nSpecies: {}\nGender: {}\nBreed: {}\nAge: {}\nAdopt this cute {} today!'.format(randomPet[0], randomPet[1], randomPet[2], randomPet[3], randomPet[4], randomPet[1].lower()), media_ids=[media_id])
        os.remove(tempPic)
    print(randomPet)

    
if __name__ == "__main__":
    main()