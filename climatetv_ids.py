import glob
import os
import pickle

path_19 = "/ceph/lprasse/ClimateVisions/Images/ClimateTV/2019"
path_20 = "/ceph/lprasse/ClimateVisions/Images/ClimateTV/2020"
path_21 = "/ceph/lprasse/ClimateVisions/Images/ClimateTV/2021"
path_22 = "/ceph/lprasse/ClimateVisions/Images/ClimateTV/2022"

# load rel ids for 2019
url_2019_all = pickle.load(open("/ceph/lprasse/ClimateVisions/IMG_urls/final_IMG_urls_2019_all.pkl", "rb"))
# print(list(url_2019_all)[:5]) ['id_1142068401516490752_2019-06-21', 'id_1187695040673538053_2019-10-25', 'id_1166365022148288512_2019-08-27', 'id_1091504552694689793_2019-02-02', 'id_1139180974238044166_2019-06-13']

all_ids = []

files_19 = glob.glob(path_19+"/*/*.jpg")
files_19 = [os.path.basename(f).replace(".jpg","") for f in files_19]
print(len(files_19)) # 707,713
files_19 = [f for f in files_19 if f in url_2019_all]
print(len(files_19)) # 707,438

files_20 = glob.glob(path_20+"/*/*.jpg")
files_20 = [os.path.basename(f).replace(".jpg","") for f in files_20]
print(len(files_20)) # 510,051

files_21 = glob.glob(path_21+"/*/*.jpg")
files_21 = [os.path.basename(f).replace(".jpg","") for f in files_21]
print(len(files_21)) # 589,038

files_22 = glob.glob(path_22+"/*/*.jpg")
files_22 = [os.path.basename(f).replace(".jpg","") for f in files_22]
print(len(files_22)) # 606,008

all_ids = files_19 + files_20 + files_21 + files_22
print(len(all_ids)) # 2,412,535

# save
with open("/ceph/lprasse/ClimateVisions/ClimateWeb/inputs/climatetv_complete.txt", "w") as f:
    for line in all_ids:
        f.write(line+"\n")