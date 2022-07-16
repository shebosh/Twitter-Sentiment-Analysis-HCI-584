import glob
import pandas as pd
import re
import os 


os.chdir('/Users/skurt/Desktop/2022 Summer/HCI 584/HCI 584 Project/proje')

clean_list = []
for file in os.listdir():
    if "elonmusk.csv" in file:
        csv_files = pd.read_csv(file)
        # new_header = csv_files.iloc[0] #grab the first row for the header
        # csv_files = csv_files[1:] #take the data less the header row
        # csv_files.columns = new_header #set the header row as the df header
    
        for item in csv_files:
            if item == "text":
                for info in csv_files[item]:
                    if "http" not in info:
                        clean_list.append(info)
                # second_edition_csv = csv_files[item]
                df = pd.DataFrame(clean_list)
                df.columns = ["text"]

                df.to_csv("elonmusk_just_text.csv")

#Get CSV files from a folder
# path = '/Users/skurt/Desktop/proje'
# csv_files = glob.glob(path + "/*.csv")

# #Read each file into a df
# df_list = (pd.read_csv(file) for file in csv_files)
# print(list(df_list))

# dfs = []
# for filepath in csv_files:
#     dfs.append(pd.read_csv(filepath, sep='delimiter', header=None))
# # print(dfs)

# # Concatenate all data into one DataFrame
# all_data = pd.concat(dfs, ignore_index=True)

# # pd.read_csv("<path>", sep=";")
# text = "2021-12-31 21:04:46+00:00,1349149096909668363,,Betty White brought a smile to the lips of generations of Americans. She’s a cultural icon who will be sorely missed. Jill and I are thinking of her family and all those who loved her this New Year’s Eve. 2021-12-31 19:28:35+00:00,1349149096909668363,,"
 

# cleaning = re.findall('\b\w+', text)

# print(cleaning)