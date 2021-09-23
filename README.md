# shelter-pet-tweeter
About: 
A simple Twitter automation that tweets details about a single pet that is being housed at the local animal shelter I work with, Cincinnati Animal CARES. I scrape the data from petango, save it locally, and then randomly pick an animal to feature as my "Pet of the Day". My hope is to be able to make this tweet from my account (@leankeuisine on Twitter) once a day at noon. 

Scheduling using CRON for Mac:
This took some learning on my end, as I had experience automating using Window Taskscheduler, but I found that for Macs, the simplest way to schedule was using CRON (with no GUi :( ).
Here is the command in order to tweet daily at noon, as well as output to a log file for debugging: 
0 12 * * * /usr/bin/python3 /Users/linakaval/Documents/Github/shelter-pet-tweeter/pet_of_the_day.py >> /tmp/out.log 2>&1


Other Notes:
This requires the creation of a separate Python module called "auth_credentials.py", where the Twitter API credentials such as consumer key and access tokens are stored. I simply have a function called twitter() that returns the consumer key, consumer secret, access token, and access token secret as a dictionary, which I reference within pet_of_the_day.py
