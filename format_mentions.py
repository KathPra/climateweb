import csv
import uuid

tweets_file = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/tweet_attributes_final.csv" # contains only relevant tweets, no filtering needed
formatted_mentions_file = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/formatted_mentions_final.csv"

with open(tweets_file, mode='r', encoding='utf-8') as infile, open(formatted_mentions_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)

    # read the header
    header = next(reader)

    # change column names to "id", "reply_id", "tweet_id", "created_at", "text"
    #print("Original header:", header)
    new_header = ["mention_id","conversation_id", "mention"]
    writer.writerow(new_header)

    for row in reader:
        # copy from the original row
        id = row["conversation_id"]
        text = row["text"]
        mention_id = uuid.uuid4()
        mentions = [word for word in text.split() if word.startswith('@')]
        for mention in mentions:
            mention = mention.strip('.,!?;:"()[]{}')
            mention = mention.split("http")[0]  # remove URLs if any
            mention = mention.split("#")[0]  # remove hashtags if any
            if mention.__contains__('@'):
                mentions_faulty = mention.split('@')
                for m in mentions_faulty:
                    if len(m) > 1:
                        m = m.strip('@')
                        writer.writerow([mention_id, id, m])
            else:
                if len(mention) > 1:
                    writer.writerow([mention_id, id, mention[1:]])  # remove '@' from the mention