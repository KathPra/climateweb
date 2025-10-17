import csv

years = ["2019","2020","2021","2022"]


## iterate through years
for year in years:
    print(year)
    replies = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/replies_{year}.csv"
    rmentions = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/reply_mentions_{year}.csv"
    users = set()

    ## extract mentions from replies and write to file
    with open(replies, "r") as rf, open(rmentions, "w", encoding='utf-8', newline='') as wf:
        # write header
        wf.write("tweet_id;mention\n")
        reply_csv = csv.DictReader(rf, delimiter=";", quotechar='"')
        count = 0
        for row in reply_csv:
            tweet_id = row["tweet_id"]
            mentions = row["mentions"].split(",")
            for ment in mentions:
                wf.write(f"{tweet_id};{ment}\n")
                users.add(ment)

    print(f"Extracted {len(users)} unique mentioned users.")


    ## load known users
    known_users = set()
    with open(f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/author_attributes_{year}.csv", "r") as kuf:
        author_csv = csv.DictReader(kuf, delimiter=",", quotechar='"')
        for row in author_csv:
            known_users.add(row["username"])

    print(f"Loaded {len(known_users)} known users.")

    unknown_users = users.difference(known_users)
    print(f"Found {len(unknown_users)} unknown mentioned users.")

    # write unknown users to file
    with open(f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/unknown_mentioned_users_{year}.csv", "w", encoding='utf-8') as ouf:
        ouf.write("username\n")
        for uu in unknown_users:
            ouf.write(f"{uu}\n")


            
                