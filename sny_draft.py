from gmplot import gmplot
import pandas as pd
import json
import geocoder

class Invaders:
    def __init__(self, all_invader_txt_path:str, personal_invader_path:str, destroyed_invader_path:str) -> None:
        self.all_invader_txt_path = all_invader_txt_path
        self.all_invader_json_path = self.all_invader_txt_path.replace("txt", "json")
        self.all_invader_csv_path = self.all_invader_txt_path.replace("txt", "csv")
        self.personal_invader_path = personal_invader_path
        self.destroyed_invader_path = destroyed_invader_path
        self.get_personal_and_destroyed_invader_list()
    
    def get_personal_and_destroyed_invader_list(self):
        # get personal invader list
        with open(self.personal_invader_path) as f:
            personal_invader_list = f.readlines()
        self.personal_invader_list = list(map(lambda x: "PA_" + x.strip().zfill(4), personal_invader_list))
        
        # get destroyed invader list
        with open(self.destroyed_invader_path) as f:
            destroyed_invader_list = f.readlines()
        self.destroyed_invader_list = list(map(lambda x: x.strip(), destroyed_invader_list))
        
    def get_all_invader_json(self):
        with open(self.all_invader_txt_path) as f:
            data = f.read()
            
        # reconstructing the data as a dictionary
        js = json.loads(data)
        js = json.dumps(js)

        with open(self.all_invader_json_path, 'w') as outfile:
            outfile.write(js)
            
    def get_all_invader_csv(self):
        data = json.load(open(self.all_invader_txt_path))
        lines = data["layers"][0]

        invaders = lines["features"]
        dic = {"ID":[], "Address":[], "Longitude":[], "Latitude":[]}
        for invader in invaders:
            ID, Address = invader['properties']['name'].split(",", 1)
            ID = ID.split("Invader ")[-1]
            Longitude, Latitude = invader['geometry']['coordinates']
            if "&" not in ID:
                dic["ID"].append(ID)
                dic["Address"].append(Address)
                dic["Latitude"].append(Latitude)
                dic["Longitude"].append(Longitude)
            else:
                ID = ID.replace(" & ", " ")
                IDs = ID.split(" ")
                IDs = list(map(lambda x : x if "PA_" in x else "PA_" + x, IDs))
                n = len(IDs)
                
                dic["ID"].extend(IDs)
                dic["Address"].extend([Address]*n)
                dic["Latitude"].extend([Latitude]*n)
                dic["Longitude"].extend([Longitude]*n)
                
        df = pd.DataFrame.from_dict(dic)
        df.to_csv(self.all_invader_csv_path)
        
        return df

    def classify_invader(self, x):
        if x in self.personal_invader_list :
            return "green"    
        elif x in self.destroyed_invader_list :
            return "black"
        else:
            return "red"
        
    def display(self):
        # Initialize the map at a given point
        gmap = gmplot.GoogleMapPlotter(48, 2, 5)
        
        # Add current position, blur point
        g = geocoder.ip('me')
        gmap.marker(g.latlng[0], g.latlng[1], color="blue")
        
        all_invader_df = self.get_all_invader_csv()
        all_invader_df["Color"] = all_invader_df["ID"].apply(self.classify_invader)
        
        for _, line in all_invader_df.iterrows():
            gmap.marker(line["Latitude"], line["Longitude"], info_window=line["ID"].split(" ")[-1] + " - - " + line["Address"], color=line["Color"])
        
        # Draw map into HTML file
        gmap.draw("my_invaders.html")


if __name__ == "__main__":
    Inva = Invaders("data/all_invaders.txt", "data/Xue.txt", "data/destroyed.txt")
    Inva.get_all_invader_json()
    Inva.get_all_invader_csv()
    Inva.display()