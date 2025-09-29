import csv
import pickle

tweet_file1 = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/eng_2019_final.csv"
tweet_file2 = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/eng_2020_final.csv"
tweet_file3 = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/eng_2021_final.csv"
tweet_file4 = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/eng_2022_final.csv"

# relevant tweets for ClimateTV
url_2019_all = pickle.load(open("/ceph/lprasse/ClimateVisions/IMG_urls/final_IMG_urls_2019_all.pkl", "rb"))
tweet_ids_2019 = {t.split("/")[-1].replace(".jpg","").split("_")[1] for t in url_2019_all}
print(len(tweet_ids_2019))
url_2020_all = pickle.load(open("/ceph/lprasse/ClimateVisions/IMG_urls/final_IMG_urls_2020_all.pkl", "rb"))
tweet_ids_2020 = {t.split("/")[-1].replace(".jpg","").split("_")[1] for t in url_2020_all}
print(len(tweet_ids_2020))
url_2021_all = pickle.load(open("/ceph/lprasse/ClimateVisions/IMG_urls/final_IMG_urls_2021_all.pkl", "rb"))
tweet_ids_2021 = {t.split("/")[-1].replace(".jpg","").split("_")[1] for t in url_2021_all}
print(len(tweet_ids_2021))
url_2022_all = pickle.load(open("/ceph/lprasse/ClimateVisions/IMG_urls/final_IMG_urls_2022_all.pkl", "rb"))
tweet_ids_2022 = {t.split("/")[-1].replace(".jpg","").split("_")[1] for t in url_2022_all}
print(len(tweet_ids_2022))

# prep ouptut file
formatted_tweets_file = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/tweet_attributes_final.csv"
counter_twids = 0
with open(tweet_file1, mode='r', encoding='utf-8') as infile, open(formatted_tweets_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter=';')
    writer = csv.writer(outfile)

    # read the header
    header = next(reader)
    #print("Original header:", header)
    # change column names to "id", "reply_id", "tweet_id", "created_at", "text"
    new_header = ["conversation_id", "created_at", "text", "like_count", "retweet_count", "quote_count", "reply_count"]
    writer.writerow(new_header)

    for row in reader:
        # copy from the original row
        if row["id"] in tweet_ids_2019:  # filter for relevant tweets
            writer.writerow([row["id"], row["created_at"], row["text"], row["like_count"], row["retweet_count"], row["quote_count"], row["reply_count"]])
            counter_twids += 1
            tweet_ids_2019.remove(row["id"])
print("Relevant tweets in 2019:", counter_twids)
    

## append other years
with open(tweet_file2, mode='r', encoding='utf-8') as infile, open(formatted_tweets_file, mode='a', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter=';')
    writer = csv.writer(outfile)

    # read the header
    header = next(reader)
    #print("Original header:", header)
    # change column names to "id", "reply_id", "tweet_id", "created_at", "text"
    new_header = ["conversation_id", "text", "like_count", "retweet_count", "quote_count", "reply_count"]
    #writer.writerow(new_header)

    for row in reader:
        # copy from the original row
        if row["id"] in tweet_ids_2020:  # filter for relevant tweets
            writer.writerow([row["id"], row["text"], row["like_count"], row["retweet_count"], row["quote_count"], row["reply_count"]])
            counter_twids += 1
            tweet_ids_2020.remove(row["id"])
print("Relevant tweets in 2019 and 2020:", counter_twids)

with open(tweet_file3, mode='r', encoding='utf-8') as infile, open(formatted_tweets_file, mode='a', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter=';')
    writer = csv.writer(outfile)

    # read the header
    header = next(reader)
    #print("Original header:", header)
    # change column names to "id", "reply_id", "tweet_id", "created_at", "text"
    new_header = ["conversation_id", "text", "like_count", "retweet_count", "quote_count", "reply_count"]
    #writer.writerow(new_header)

    for row in reader:
        if row["id"] in tweet_ids_2021:  # filter for relevant tweets
            # copy from the original row
            writer.writerow([row["id"], row["text"], row["like_count"], row["retweet_count"], row["quote_count"], row["reply_count"]])
            counter_twids += 1
            tweet_ids_2021.remove(row["id"])
print("Relevant tweets in 2019,2020, and 2021:", counter_twids)

with open(tweet_file4, mode='r', encoding='utf-8') as infile, open(formatted_tweets_file, mode='a', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter=';')
    writer = csv.writer(outfile)

    # read the header
    header = next(reader)
    #print("Original header:", header)
    # change column names to "id", "reply_id", "tweet_id", "created_at", "text"
    new_header = ["conversation_id", "text", "like_count", "retweet_count", "quote_count", "reply_count"]
    #writer.writerow(new_header)

    for row in reader:
        if row["id"] in tweet_ids_2022:  # filter for relevant tweets
            # copy from the original row
            writer.writerow([row["id"], row["text"], row["like_count"], row["retweet_count"], row["quote_count"], row["reply_count"]])
            counter_twids += 1
            tweet_ids_2022.remove(row["id"])
print("Relevant tweets in 2019, 2020,2021 and 2022:", counter_twids)