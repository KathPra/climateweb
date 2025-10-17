import csv
import pickle

tweet_file1 = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/eng_2019_final.csv"
tweet_file2 = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/eng_2020_final.csv"
tweet_file3 = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/eng_2021_final.csv"
tweet_file4 = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/eng_2022_final.csv"

# relevant tweets for ClimateTV
climatetv_final = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/climatetv_complete.txt"

## load required tweet ids
tweet_dict = dict()
with open(climatetv_final, "r", encoding='utf-8') as cf:
    for line in cf:
        tweet_dict[line.strip().split("_")[1]] = line.strip()  # tweet_id: image_id
print(f"Total relevant tweets: {len(tweet_dict)}") # 2,412,535


# prep ouptut file
formatted_tweets_file = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/tweet_attributes_final.csv"
counter_twids = 0
with open(tweet_file1, mode='r', encoding='utf-8') as infile, open(formatted_tweets_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter=';')
    writer = csv.writer(outfile)

    # read the header
    header = next(reader)
    print("Original header:", header.keys())
    # change column names to "id", "reply_id", "tweet_id", "created_at", "text"
    new_header = ["conversation_id", "created_at", "text", "like_count", "retweet_count", "quote_count", "reply_count", "image_id"]
    writer.writerow(new_header)

    for row in reader:
        # copy from the original row
        if row["id"] in tweet_dict:  # filter for relevant tweets
            writer.writerow([row["id"], row["created_at"], row["text"], row["like_count"], row["retweet_count"], row["quote_count"], row["reply_count"], tweet_dict[row["id"]]])
            counter_twids += 1
            tweet_dict.pop(row["id"])  # remove to save memory
print("Relevant tweets in 2019:", counter_twids)
    

## append other years
with open(tweet_file2, mode='r', encoding='utf-8') as infile, open(formatted_tweets_file, mode='a', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter=';')
    writer = csv.writer(outfile)

    # read the header
    header = next(reader)
    #print("Original header:", header)
    # change column names to "id", "reply_id", "tweet_id", "created_at", "text"
    new_header = ["conversation_id", "text", "like_count", "retweet_count", "quote_count", "reply_count", "image_id"]
    #writer.writerow(new_header)

    for row in reader:
        # copy from the original row
        if row["id"] in tweet_dict:  # filter for relevant tweets
            writer.writerow([row["id"], row["text"], row["like_count"], row["retweet_count"], row["quote_count"], row["reply_count"], tweet_dict[row["id"]]])
            counter_twids += 1
            tweet_dict.pop(row["id"])  # remove to save memory
print("Relevant tweets in 2019 and 2020:", counter_twids)

with open(tweet_file3, mode='r', encoding='utf-8') as infile, open(formatted_tweets_file, mode='a', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter=';')
    writer = csv.writer(outfile)

    # read the header
    header = next(reader)
    #print("Original header:", header)
    # change column names to "id", "reply_id", "tweet_id", "created_at", "text"
    new_header = ["conversation_id", "text", "like_count", "retweet_count", "quote_count", "reply_count", "image_id"]
    #writer.writerow(new_header)

    for row in reader:
        if row["id"] in tweet_dict:  # filter for relevant tweets
            # copy from the original row
            writer.writerow([row["id"], row["text"], row["like_count"], row["retweet_count"], row["quote_count"], row["reply_count"], tweet_dict[row["id"]]])
            counter_twids += 1
            tweet_dict.pop(row["id"])  # remove to save memory
print("Relevant tweets in 2019,2020, and 2021:", counter_twids)

with open(tweet_file4, mode='r', encoding='utf-8') as infile, open(formatted_tweets_file, mode='a', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter=';')
    writer = csv.writer(outfile)

    # read the header
    header = next(reader)
    #print("Original header:", header)
    # change column names to "id", "reply_id", "tweet_id", "created_at", "text"
    new_header = ["conversation_id", "text", "like_count", "retweet_count", "quote_count", "reply_count", "image_id"]
    #writer.writerow(new_header)

    for row in reader:
        if row["id"] in tweet_dict:  # filter for relevant tweets
            # copy from the original row
            writer.writerow([row["id"], row["text"], row["like_count"], row["retweet_count"], row["quote_count"], row["reply_count"], tweet_dict[row["id"]]])
            counter_twids += 1
            tweet_dict.pop(row["id"])


    print("Relevant tweets in 2019, 2020,2021 and 2022:", counter_twids) # 2,412,533
    for twid in tweet_dict:
        writer.writerow([twid, "", "", "", "", "", tweet_dict[twid]])
        counter_twids += 1
print("Total relevant tweets written:", counter_twids) # 2,412,535
