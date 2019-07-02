import tweepy
import time
import pandas as panda
from twitter import Twitter
import itertools

import csv
API = Twitter().instance()
waitQuery = 100
waitTime = 2.0
engineBlow = 1
csvFile = open('statuses_jokowi.csv', 'w', encoding='utf-8')
csvWriter = csv.writer(csvFile)

def search() :
    global API, waitQuery, waitTime, engineBlow
    query = str(input("Search something : "))
    total_number = int(input("n : "))
    cursor = tweepy.Cursor(API.search, query + " -RT", tweet_mode = "extended", lang = "en").items()
    count = 0
    error = 0
    secondcount = 0
    idvalues = [0] * total_number
    while secondcount < total_number:
        try:
            c = next(cursor)
            count += 1
            if count % waitQuery == 0:
                time.sleep(waitTime)
        except tweepy.TweepError:
            print("Sleeping...")
            time.sleep(60 * engineBlow)
            c = next(cursor)
        except StopIteration:
            break

        try:
            text_val = c._json['full_text']
            text_val = str(text_val).lower()
            if "rt" not in text_val:
                if len(text_val) != 0:
                    secondcount += 1
                    csvWriter.writerow([secondcount,str(text_val)])
                    print("[INFO] Getting a tweet : " + str(secondcount) + " = " + text_val)
        except Exception as e:
            error += 1
            print('[EXCEPTION] Stream data: ' + str(e))

def status(who) :
    global API, waitQuery, waitTime, engineBlow
    statuses = API.user_timeline(screen_name= who)
    i = 0
    for status in tweepy.Cursor(API.user_timeline, screen_name=who, tweet_mode="extended").items():
        csvWriter.writerow([i ,str(status.full_text), status.created_at, status.retweet_count, status.favorite_count])
        print("Tweet ke-" + str(i) + " diambil : "+ str(status.full_text))
        i += 1
    print("Crawling tweet "+ who+ " selesai!")
    

def crawl():
    global API, waitQuery, waitTime, engineBlow
    query = str(input("Search something : "))
    total_number = int(input("n : "))
    cursor = tweepy.Cursor(API.get_user(screen_name="jokowi", cursor=-1)).items()
    count = 0
    error = 0
    secondcount = 0
    idvalues = [0] * total_number
    while secondcount < total_number:
        try:
            c = next(cursor)
            count += 1
            if count % waitQuery == 0:
                time.sleep(waitTime)
        except tweepy.TweepError:
            print("Sleeping...")
            time.sleep(60 * engineBlow)
            c = next(cursor)
        except StopIteration:
            break

        try:
            users = c._json['users']
            print(users)
            secondcount += 1
            csvWriter.writerow([secondcount,str(text_val)])
            print("[INFO] Getting a tweet : " + str(secondcount) + " = " + text_val)
        except Exception as e:
            error += 1
            print('[EXCEPTION] Stream data: ' + str(e))

def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page


def followers():

    followers = API.followers_ids(screen_name='jokowi')

    for page in paginate(followers, 100):
        results = API.lookup_users(user_ids=page)
        for result in results:
            print("mengambil data milik : "+ result.screen_name)
            # users = result._json['users']
            if result.location == "":
                csvWriter.writerow([result.id, result.name, result.screen_name, "NA"])
            else:
                csvWriter.writerow([result.id, result.name, result.screen_name, result.location])
        print("Halaman berikutnya")

    print("Crawling selesai")



status("jokowi")
# followers()