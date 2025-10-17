## conda env: env_clip
import torch
import csv

years = ["2019","2020","2021","2022"]

outfile = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/duplicate_images.csv"

with open(outfile, "w", encoding='utf-8', newline='') as of:
    writer = csv.writer(of, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["image_id_org", "image_id_dup"])
    for year in years:
        print(year)
        img_file = f"/ceph/lprasse/ClimateVisions/ClimateVisions_2.0/analysis/dedup/dups_{year}.torch"
        dup_check = torch.load(img_file)
        for org in dup_check:
            id_org = org.split("_")[1]
            for dup in dup_check[org]:
                id_dup = dup.split("_")[1]
                # duplicate found
                writer.writerow([id_org, id_dup])
        if year == "2019":
            continue
        else: 
            img_file_prev = f"/ceph/lprasse/ClimateVisions/ClimateVisions_2.0/analysis/dedup/dups_interyear_{year}.torch"
            dup_check_prev = torch.load(img_file_prev)
            for org in dup_check_prev:
                id_org = org.split("_")[1]
                for dup in dup_check_prev[org]:
                    id_dup = dup.split("_")[1]
                    # duplicate found
                    writer.writerow([id_org, id_dup])

