import csv
years = ["2019","2020","2021","2022"]

outfile = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/merged_replies.csv"

with open(outfile, "w", encoding='utf-8', newline='') as of:
    writer = csv.writer(of, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["tweet_id","created_at","reply_text","reply_id"])
    for year in years:
        print(year)
        replies = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/replies_{year}.csv"
        with open(replies, "r", encoding='utf-8') as rf:
            reply_csv = csv.DictReader(rf, delimiter=";", quotechar='"')
            for row in reply_csv:
                reply_id = row["reply_id"]
                tweet_id = row["tweet_id"]
                reply_text = row["reply_text"]
                created_at = row["created_at"]
                writer.writerow([tweet_id, created_at, reply_text, reply_id])