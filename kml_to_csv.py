from bs4 import BeautifulSoup
import pandas as pd
from os import listdir
from os.path import isfile, join

def convert(kml_file):
    outfile =  kml_file.replace(".kml", ".csv")
    
    with open(kml_file, 'r') as f:
        s = BeautifulSoup(f, 'xml')
            
        coords = s.find_all('coordinates')
        IDs = s.find_all('name')[2:]
        
        data = []
        for i in range(len(coords)):
            long, lat, _ = coords[i].string.split(",")
            long = long.strip()
            lat = lat.strip()
            ID = IDs[i].string.split(",")[0]
            if "_" in ID:
                ID = ID.split("_")[0] + "_" + ID.split("_")[1].zfill(4)
            # Take coordinate string from KML and break it up into [Lat,Lon,Lat,Lon...] to get CSV row
            add = ""
            data.append([ID, add, long, lat])
            
        df = pd.DataFrame(data, columns=["ID", "Address", "Longitude", "Latitude"]).sort_values(by="ID")
        df.to_csv('data/address.csv', mode='a', index=False, header=False, sep=";")
        
            # for split in space_splits[1:]:
            #     # Note: because of the space between <coordinates>" "-80.123, we slice [1:]
            #     comma_split = split.split(',')
            #     # lattitude
            #     row.append(comma_split[1])
                
            #     # longitude
            #     row.append(comma_split[0])
            
            # writer.writerow(row)


def main():
    path = "data/kml"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file in onlyfiles:
        convert("data/kml/" + file)


if __name__ == "__main__":
    main()