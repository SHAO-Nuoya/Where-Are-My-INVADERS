from gmplot import gmplot
import pandas as pd
import json



class Invaders:
    def __init__(self, all_path_txt:str, personal_path:str) -> None:
        self.all_path_txt = all_path_txt
        self.all_path_json = self.all_path_txt.replace("txt", "json")
        self.all_path_csv = self.all_path_txt.replace("txt", "csv")
        self.personal_path = personal_path
        
    def to_json(self):
        with open(self.all_path_txt) as f:
            data = f.read()
            
        # reconstructing the data as a dictionary
        js = json.loads(data)
        js = json.dumps(js)

        with open(self.all_path_json, 'w') as outfile:
            outfile.write(js)
            
    def to_csv(self):
        data = json.load(open(self.all_path_txt))
        lines = data["layers"][0]

        invaders = lines["features"]
        dic = {"ID":[], "Address":[], "Longitude":[], "Latitude":[]}
        for invader in invaders:
            ID, Address = invader['properties']['name'].split(",", 1)
            Longitude, Latitude = invader['geometry']['coordinates']
            dic["ID"].append(ID)
            dic["Address"].append(Address)
            dic["Latitude"].append(Latitude)
            dic["Longitude"].append(Longitude)
        df = pd.DataFrame.from_dict(dic)
        df.to_csv(self.all_path_csv)
        return df
    
    def display(self):
        # Initialize the map at a given point
        gmap = gmplot.GoogleMapPlotter(48, 2, 5)

        # Add a marker
        df = self.to_csv()
        for _, line in df.iterrows():
            gmap.marker(line["Latitude"], line["Longitude"], info_window=line["ID"].split(" ")[-1] + " - - " + line["Address"])

        # Draw map into HTML file
        gmap.draw("my_invaders.html")

if __name__ == "__main__":
    Inva = Invaders("data/all_invaders.txt", "data/nuoya.txt")
    Inva.to_json()
    Inva.to_csv()
    Inva.display()