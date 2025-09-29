import csv
import glob
import pickle
import pandas as pd
import tqdm
import uuid
import re

year = "2019"

## load list of users mentioned in tweets
mentions = pd.read_csv(f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/formatted_mentions_final.csv")
author_names = set(mentions['mention'].tolist())

## read list of tweet ids in the nsfw-cleaned climatetv set
if year == "2019":
    # some images have no links
    url_2019_all = pickle.load(open("/ceph/lprasse/ClimateVisions/IMG_urls/final_IMG_urls_2019_all.pkl", "rb"))
    tweet_ids = {t.split("/")[-1].replace(".jpg","").split("_")[1] for t in url_2019_all}

else: 
    tweet_ids = glob.glob(f"/ceph/lprasse/ClimateVisions/Images/ClimateTV/{year}/*/*.jpg")
    tweet_ids = [t.split("/")[-1].replace(".jpg","") for t in tweet_ids]
    tweet_ids = [t.split("_")[1] for t in tweet_ids]
    tweet_ids = set(tweet_ids)

print("Number of tweet ids in the safe climatetv set in ", year, ": ", len(tweet_ids)) # 2019: 707,438

# read tweet info for all posts in the selected year
with open(f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/eng_{year}_final.csv", mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile, delimiter=';')
    #print(next(reader))

    media_dict = {}
    for row in reader:
        media = row['media_keys']
        tweet_id = row['conversation_id']
        # if tweet is not relevant, skip
        if tweet_id not in tweet_ids:
            continue
        for m in media.split(","):
            media_dict[m] = tweet_id

print("Medias posted in ", year , ": ",len(media_dict)) # 2019: 834,494
#print(author_names)

author_files = glob.glob(f"/ceph/lprasse/ClimateVisions/RDS_urls/processed/backup/*{year}*.pkl")
print("Number for files to read:" , len(author_files)) # 2019: 365

tweet_authors = {}

found = 0
not_found = 0
for file in tqdm.tqdm(author_files):
    author_infos = {}
    author_mentions = {}
    # read pkl file
    with open(file, mode='rb') as infile:
        author_single = pickle.load(infile)
    #print column names (pandas dataframe)
    #print(author_single.columns)
    """
    ['user', 'name', 'username', 'location', 'verified', 'description', 'id',
       'lang', 'geo', 'referenced_tweets', 'reply_settings', 'created_at',
       'text', 'source', 'retweet_count', 'reply_count', 'like_count',
       'quote_count', 'attachments', 'hashtags', 'public_metrics',
       'link_image', 'url_image', 'link_type', 'view_count', 'tweetURL', 'day',
       'month', 'year', 'date', 'user_engagement']
    """
    # convert to dictionary
    author_infos = author_single.to_dict(orient='records')
    #print(author_infos[0])
    #print(len(author_infos))
    for u in author_infos:
        medias_tweeted = u['attachments']
        if medias_tweeted in media_dict:
            tweet_id = media_dict[medias_tweeted]
            tweet_authors[tweet_id] = {"name": u['name'], "username": u['username'],"location": u['location'],"verified": u['verified'],"description": u['description']}
        elif u['username'] in author_names:
            author_mentions[u["username"]] = {"name": u['name'], "username": u['username'],"location": u['location'],"verified": u['verified'],"description": u['description']}

print("Found medias: ", len(tweet_authors)) # 2019: 706,732


# create output file 1: mapping tweets to authors
formatted_authors_file = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/author_mapping_{year}.csv"
with open(formatted_authors_file, mode='w', encoding='utf-8', newline='') as outfile:

    # create the header
    headers = ['id','username']
    writer = csv.writer(outfile)
    writer.writerow(headers)

    for tid, infos in tweet_authors.items():
        infos_formatted = infos['description'].replace('\n', ' ').replace('\r', ' ').replace(',', ';')
        if infos_formatted is None:
            infos_formatted = "n/a"
        loc_formatted = infos['location']
        if loc_formatted is None:
            loc_formatted = "n/a"

        writer.writerow([tid, infos['name'], infos['username'], loc_formatted, infos['verified'], infos_formatted])


# create output file 2: author attributes (username is key)
formatted_authors_file = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/author_attributes_{year}.csv"
author_set = set()
with open(formatted_authors_file, mode='w', encoding='utf-8', newline='') as outfile:

    # create the header
    headers = ['author_id','name', 'username', 'location', 'verified', 'description']
    writer = csv.writer(outfile)
    writer.writerow(headers)

    for infos in tweet_authors.values():
        # only add each author once
        if infos['username'] in author_set:
            continue
        # format the description and location to avoid new lines and commas
        name_formatted = infos['name'].replace('\n', ' ').replace('\r', ' ').replace(',', ';')
        infos_formatted = infos['description'].replace('\n', ' ').replace('\r', ' ').replace(',', ';')
        if infos_formatted is None:
            infos_formatted = "n/a"
        elif len(infos_formatted)<1:
            infos_formatted = "n/a"
        loc_formatted = infos['location']
        if loc_formatted is None:
            loc_formatted = "n/a"
        else:
            loc_formatted = loc_formatted.replace('\n', ' ').replace('\r', ' ').replace(',', ';')
        # create a unique id
        uid = uuid.uuid4()
        # write to file
        writer.writerow([uid, name_formatted, infos['username'], loc_formatted, infos['verified'], infos_formatted])
        # add author to processed authors
        author_set.add(infos['username'])

    for infos in author_mentions.values():
        # only add each author once
        if infos['username'] in author_set:
            continue
        # format the description and location to avoid new lines and commas
        name_formatted = infos['name'].replace('\n', ' ').replace('\r', ' ').replace(',', ';')
        infos_formatted = infos['description'].replace('\n', ' ').replace('\r', ' ').replace(',', ';')
        if infos_formatted is None:
            infos_formatted = "n/a"
        elif len(infos_formatted)<1:
            infos_formatted = "n/a"
        loc_formatted = infos['location']
        if loc_formatted is None:
            loc_formatted = "n/a"
        else:
            loc_formatted = loc_formatted.replace('\n', ' ').replace('\r', ' ').replace(',', ';')
        # create a unique id
        uid = uuid.uuid4()
        # write to file
        writer.writerow([uid, name_formatted, infos['username'], loc_formatted, infos['verified'], infos_formatted])
        # add author to processed authors
        author_set.add(infos['username'])
print("Total unique authors: ", len(author_set)) # 2019: 217,191