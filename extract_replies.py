# conda env: env_r
import csv
import os
import re

year = "2020"
csv_path = f"/ceph/lprasse/ClimateVisions/RDS_replies/processed/eng_replies_{year}_final.csv"
target_path = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/replies_{year}.csv"
rel_tweets_file = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/climatetv_complete.txt"

# process to have a set of tweet_ids
with open(rel_tweets_file, "r") as i:
    rel_tweets = i.readlines()
#print(rel_tweets[:5])
rel_tweets = [os.path.basename(l).split("_")[1] for l in rel_tweets]
#print(rel_tweets[:5])
#['1192801066099888131', '1198902767269634048', '1199694371110707200', '1195510596046856192', '1195447601627385857']
rel_tweets = set(rel_tweets)
print(len(rel_tweets)) # 2,412,535

count = 0

# read csv
with open(csv_path, "r") as f, open(target_path, "w") as o:
    input_csv = csv.DictReader(f, delimiter=";", quotechar='"')
    # write header
    o.write("tweet_id;created_at;org_tweet;reply_author;tweet_author;mentions;quoted_tweet;reply_text;reply_id\n")
    for line in input_csv:
        ## extract tweet_id and skip if not relevant
        tweet_id = line["conversation_id"]

        ## extract date
        date = line["created_at"]
        ## extract referenced tweets
        tweet_refs = line["referenced_tweets"]
        num_refs = tweet_refs.count("id")
        quoted_tweet = "NA"
        if "type:" in tweet_refs:
            org_tweet = tweet_refs.split("id:")[-1]
        elif num_refs == 2: # verified max 2 entries
            reply_loc = tweet_refs[tweet_refs.find(":replied_to")-1]
            org_tweet = tweet_refs.split("id"+str(reply_loc)+":")[-1].split(",")[0]
            if "quoted" in tweet_refs: # verified only other type of relation
                if reply_loc != num_refs:
                    quote_loc = "1"
                else:
                    quote_loc = "2"
                quoted_tweet = tweet_refs.split("id"+str(quote_loc)+":")[-1].split(",")[0]
        #print(quoted_tweet)
        #print(org_tweet)

        ## extract author of reply
        reply_author = line["author_id"]

        ## extract author of tweet
        tweet_author = line["in_reply_to_user_id"]

        if tweet_id in rel_tweets or org_tweet in rel_tweets:
            count += 1
        else:
            continue
        
        ## extract reply id
        reply_id = line["id"]

        ## find mentions
        mentions = []
        text = line["text"]
        num_mentions = text.count("@")
        mentions = re.findall(r"@(\w+)", text)
        mentions = [m[m.find("@")+1:] for m in mentions]
        mentions = [m for m in mentions if len(m)>3 or len(m)<17] # requirement 3 > username > 16 # https://help.x.com/en/managing-your-account/x-username-rules
                    
        mentions = list(set(mentions))

        # write to file
        o.write(f"{tweet_id};{date};{org_tweet};{reply_author};{tweet_author};{','.join(mentions)};{quoted_tweet};{text};{reply_id}\n")

