import pickle as pkl
import csv

years = ["2019","2020","2021","2022"]
categories = ["animals", "climateaction", "consequences", "setting", "type"]

outfile = "/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/image_labels.csv"

with open(outfile, "w", encoding='utf-8', newline='') as of:
    writer = csv.writer(of, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["image_id", "label_animals", "label_climateaction", "label_consequences", "label_setting", "label_type"])
    for year in years:
        print(year)
        label_dict = {}
        for cat in categories:
            label_file = f"/ceph/lprasse/ClimateVisions/ClimateVisions_2.0/analysis/content_all/images_all_{year}_CLIP-ViT-B32_{cat}.pkl"
            with open(label_file, "rb") as lf:
                label_data = pkl.load(lf)
            for key in label_data:
                id_img = key.split("_")[1]
                label = label_data[key]
                # extract key from label dict
                label = list(label.keys())[0]
                if id_img not in label_dict:
                    label_dict[id_img] = {}
                label_dict[id_img][cat] = label
        for id_img in label_dict:
            row = [id_img]
            for cat in categories:
                row.append(label_dict[id_img].get(cat, ""))
            writer.writerow(row)
