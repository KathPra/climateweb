import csv

tweet_infos = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/tweet_attributes_final.csv"
label_infos = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/image_labels.csv"
climatetv_final = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/climatetv_complete.txt"

outfile = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/tweets_final.csv"

## load required tweet ids
tweet_id_set = set()
with open(climatetv_final, "r", encoding='utf-8') as cf:
    for line in cf:
        tweet_id_set.add(line.strip().split("_")[1])
print(f"Total relevant tweets: {len(tweet_id_set)}") # 2,412,535

# load tweet infos
tweet_dict = {}
with open(tweet_infos, "r", encoding='utf-8') as tf:
    tweet_csv = csv.DictReader(tf, delimiter=",", quotechar='"')
    for row in tweet_csv:
        tweet_id = row["conversation_id"]
        if tweet_id in tweet_id_set:
            tweet_dict[tweet_id] = row
print(f"Loaded {len(tweet_dict)} tweets.") # 2,412,535

# load labels
with open(label_infos, "r", encoding='utf-8') as lf:
    label_csv = csv.DictReader(lf, delimiter=",", quotechar='"')
    for row in label_csv:
        img_id = row["image_id"]
        if img_id in tweet_dict:
            tweet_dict[img_id].update(row)

# save
with open(outfile, "w", encoding='utf-8', newline='') as of:
    fieldnames = list(tweet_dict[next(iter(tweet_dict))].keys())
    writer = csv.DictWriter(of, fieldnames=fieldnames, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for tweet_id in tweet_dict:
        writer.writerow(tweet_dict[tweet_id])