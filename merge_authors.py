import csv
import os
import uuid

years = ["2019","2020","2021","2022"]

## merge author attributes files
output_file = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/author_attributes_final.csv"
if os.path.exists(output_file):
    print("final author attribute mapping already completed.")
else:
    ## check usernames
    usernames_seen = set()
    for year in years:
        print(year)
        input_file = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/author_attributes_{year}.csv"
        if year == "2019":
            # for the first year, create a file and write content from input
            with open(input_file, "r", encoding='utf-8') as infile, open(output_file, "w", encoding='utf-8', newline='') as outfile:
                reader = csv.DictReader(infile, delimiter=",", quotechar='"')
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=",", quotechar='"')
                writer.writeheader()
                for row in reader:
                    try:
                        if row["username"] in usernames_seen:
                            continue
                        writer.writerow(row)
                        usernames_seen.add(row["username"])
                    except: 
                        print("Error with row: ", row)
        else:
            # for subsequent years, append content without header
            with open(input_file, "r", encoding='utf-8') as infile, open(output_file, "a", encoding='utf-8', newline='') as outfile:
                reader = csv.DictReader(infile, delimiter=",", quotechar='"')
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=",", quotechar='"')
                writer.writeheader()
                for row in reader:
                    try:
                        if row["username"] in usernames_seen:
                            continue
                        writer.writerow(row)
                        usernames_seen.add(row["username"])
                    except: 
                        print("Error with row: ", row)

    ## add unknown mentioned users to the mapping file without further attributes
    for year in years:
        print(year)
        unknown_authors = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/unknown_mentioned_users_{year}.csv"
        with open(unknown_authors, "r", encoding='utf-8') as infile, open(output_file, "a", encoding='utf-8', newline='') as outfile:
            reader = csv.reader(infile, delimiter=",", quotechar='"')
            writer = csv.writer(outfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            next(reader) # skip header
            next(reader) # skip first line (empty row)
            for row in reader:
                username = row[0]
                if username in usernames_seen:
                    continue
                # create a unique tweet id for the unknown user
                tweet_id = str(uuid.uuid4())
                writer.writerow([tweet_id,"NA", username, "NA", "NA", "NA"])
                usernames_seen.add(username)

## merge tweet to author mapping files
output_file = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/author_mapping_final.csv"
if os.path.exists(output_file):
    print("final tweet author mapping already completed.")
else:
    for year in years:
        print(year)
        input_file = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/author_mapping_{year}.csv"
        unknown_authors = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/unknown_mentioned_users_{year}.csv"
        if year == "2019":
            # for the first year, create a file and write content from input
            with open(input_file, "r", encoding='utf-8') as infile, open(output_file, "w", encoding='utf-8', newline='') as outfile:
                reader = csv.reader(infile, delimiter=",", quotechar='"')
                # skip header
                next(reader)
                fieldnames = ["tweet_id", "author_username"]
                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=",", quotechar='"')
                writer.writeheader()
                for row in reader:
                    tweet_id = row[0]
                    username = row[2]
                    writer.writerow({"tweet_id": tweet_id, "author_username": username})
 
        else:
            # for subsequent years, append content without header
            with open(input_file, "r", encoding='utf-8') as infile, open(output_file, "a", encoding='utf-8', newline='') as outfile:
                reader = csv.reader(infile, delimiter=",", quotechar='"')
                # skip header
                next(reader)
                fieldnames = ["tweet_id", "author_username"]
                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=",", quotechar='"')
                writer.writeheader()
                for row in reader:
                    tweet_id = row[0]
                    username = row[2]
                    writer.writerow({"tweet_id": tweet_id, "author_username": username})
 
