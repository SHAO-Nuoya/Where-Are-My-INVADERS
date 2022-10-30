from cmath import isnan
from gmplot import gmplot
import pandas as pd
import geocoder

class Invaders:
    def __init__(self, all_invader_txt_path:str, personal_invader_path:str, destroyed_invader_path:str) -> None:
        self.all_invader_txt_path = all_invader_txt_path
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
        
        all_invader_df = pd.read_csv(self.all_invader_txt_path)
        all_invader_df["Color"] = all_invader_df["ID"].apply(self.classify_invader)
        all_invader_df["Address"] = all_invader_df["Address"].astype("str")
        
        for _, line in all_invader_df.iterrows():
            if not isnan(line["Latitude"]):
                line["Address"] = "" if line["Address"] else line["Address"]
                gmap.marker(line["Latitude"], line["Longitude"], info_window=line["ID"] + " - - " + line["Address"], color=line["Color"])
        
        # Draw map into HTML file
        gmap.draw("my_invaders.html")


if __name__ == "__main__":
    Inva = Invaders("data/address.csv", "data/Xue.txt", "data/destroyed.txt")
    Inva.display()