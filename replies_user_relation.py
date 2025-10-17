import csv

years = ["2019","2020","2021","2022"]

outfile = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/reply_user_relation.csv"

with open(outfile, "w", encoding='utf-8', newline='') as of:
    writer = csv.writer(of, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["reply_id", "mention_username"])
    for year in years:
        print(year)
        replies = f"/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/reply_mentions_{year}.csv"
        with open(replies, "r", encoding='utf-8') as rf:
            reply_csv = csv.DictReader(rf, delimiter=";", quotechar='"')
            for row in reply_csv:
                reply_id = row["reply_id"]
                username = row["mention"]
                writer.writerow([reply_id, username])
