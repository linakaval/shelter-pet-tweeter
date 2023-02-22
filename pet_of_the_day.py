import requests
from bs4 import BeautifulSoup
import random
import tweepy
import os
import sys
import time
import smtplib
sys.path.append("/Users/linakaval/Documents/Github/")
import auth_credentials #module with credentials

DOG_URL = 'https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals2.aspx?species=dog&gender=All&agegroup=All&location=&site=&onhold=All&orderby=ID&colnum=5&authkey=ho44bl6bmphbs21iior7k671v2gh2cf8r70636k2i7rcvs1br0&recAmount=&detailsInPopup=Yes&featuredPet=Include&stageID='
CAT_URL = 'https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals2.aspx?species=cat&gender=All&agegroup=All&location=&site=&onhold=All&orderby=ID&colnum=5&authkey=ho44bl6bmphbs21iior7k671v2gh2cf8r70636k2i7rcvs1br0&recAmount=&detailsInPopup=Yes&featuredPet=Include&stageID='
OTHER_URL = 'https://ws.pxetango.com/webservices/adoptablesearch/wsAdoptableAnimals2.aspx?species=other&gender=All&agegroup=All&location=&site=&onhold=All&orderby=ID&colnum=5&authkey=ho44bl6bmphbs21iior7k671v2gh2cf8r70636k2i7rcvs1br0&recAmount=&detailsInPopup=Yes&featuredPet=Include&stageID='

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
    cred = auth_credentials.twitter()

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(cred['CONSUMER_KEY'], cred['CONSUMER_SECRET'])
    auth.set_access_token(cred['ACCESS_TOKEN'], cred['ACCESS_TOKEN_SECRET'])

    # Create API object
    api = tweepy.API(auth)
    current_animals = []
    tempPic = 'temp_pic.jpg'

    #get all available dogs, cats, and other animal profiles
    getAnimals(DOG_URL, current_animals)
    getAnimals(CAT_URL, current_animals)
    getAnimals(OTHER_URL, current_animals)

    #select random pet from list
    randomPet = current_animals[random.randint(0, len(current_animals))]

    #new request created to save image chunk locally
    with requests.Session() as s:
        pic = requests.get(randomPet[5], stream=True)
        if pic.status_code == 200:
            with open(tempPic, 'wb') as image:
                for chunk in pic.iter_content():
                    image.write(chunk)
            #upload image to twitter, returns media_id to link to tweet
            media_id = api.chunked_upload(tempPic).media_id
            #create tweet and send
            api.update_status(status='CACHS Pet of the Day\nName: {}\nSpecies: {}\nGender: {}\nBreed: {}\nAge: {}\nAdopt this cute {} today!'.format(randomPet[0], randomPet[1], randomPet[2], randomPet[3], randomPet[4], randomPet[1].lower()), media_ids=[media_id])
        os.remove(tempPic)
    #print(randomPet)

    
if __name__ == "__main__":
    try:
        main()
    except:
        #Email Lina if tweeter breaks
        print("There was an error with sending tweet. Emailing Lina.")
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        cred = auth_credentials.gmail()
        s.login(cred['USER'], cred['PASSWORD'])
        message = "Check your pet tweeter, something broke"
        s.sendmail(cred['USER'], cred['USER'], message)
        s.quit()