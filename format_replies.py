import csv
import pickle

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

all_tweet_ids = tweet_ids_2019.union(tweet_ids_2020).union(tweet_ids_2021).union(tweet_ids_2022)


replies_file = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/replies_translated.csv"
formatted_replies_file = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/formatted_replies_final.csv"

with open(replies_file, mode='r', encoding='utf-8') as infile, open(formatted_replies_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # read the header
    header = next(reader)

    # change column names to "id", "reply_id", "tweet_id", "created_at", "text"
    new_header = ["tweet_replay_id", "reply_id", "conversation_id", "created_at", "text"]
    writer.writerow(new_header)

    for row in reader:
        # if the conversation id is within our dataset
        if row[2] in all_tweet_ids:
            # copy from the original row
            writer.writerow(row)