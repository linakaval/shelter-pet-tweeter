# shelter-pet-tweeter
About: 
A simple Twitter automation that tweets details about a single pet that is being housed at the local animal shelter I work with, Cincinnati Animal CARES. I scrape the data from petango, save it locally, and then randomly pick an animal to feature as my "Pet of the Day". My hope is to be able to make this tweet from my account (@leankeuisine on Twitter) once a day at noon. 

Other Notes:
This requires the creation of a separate Python module called "auth_credentials.py", where the Twitter API credentials such as consumer key and access tokens are stored. I simply have a function called twitter() that returns the consumer key, consumer secret, access token, and access token secret as a dictionary, which I reference within pet_of_the_day.py
