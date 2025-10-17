import csv

year = "2019"

replies = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/replies_{year}.csv"
authors_file = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/author_mapping_{year}.csv"

# load author mapping
tweet_map = {} # mapping from tweet to author username
with open(authors_file, "r") as af:
    author_csv = csv.reader(af, delimiter=",", quotechar='"')
    for row in author_csv:
        #skip header
        if row[0] == "id":
            continue
        tweet_map[row[0]] = row[2]
print(f"Loaded {len(tweet_map)} tweet mappings.")

# verify replies
with open(replies, "r") as rf:
    reply_csv = csv.DictReader(rf, delimiter=";", quotechar='"')
    for row in reply_csv:
        tweet_id = row["tweet_id"]
        org_id = row["org_tweet"]
        
        #if tweet_id in tweet_map:
        #    print(tweet_map[tweet_id])
        #    print(row)
        #    break

        if org_id in tweet_map and org_id != tweet_id:
            print(tweet_map[org_id])
            print(row)
            break