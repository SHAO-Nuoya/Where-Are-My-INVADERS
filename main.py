from cmath import isnan
from gmplot import gmplot
import pandas as pd
import simplekml
from simplekml import Kml
from zipfile import ZipFile
from pykml.factory import KML_ElementMaker as KML
from lxml import etree


class Invaders:
    def __init__(self, client:str, address_path:str="data/address.csv", info_path:str="data/info.csv") -> None:
        self.address_path = address_path
        self.info_path = info_path
        self.client = client
        self.merged_df = self.gather_all_info()
        self.generate_kml()
    
    def gather_all_info(self):
        address_df = pd.read_csv(self.address_path)
        info_df = pd.read_csv(self.info_path)
        merged_df = pd.merge(address_df, info_df)
        merged_df["Color"] = merged_df["State"].apply(self.classify_invader)
        # merged_df["Address"] = merged_df["Address"].astype("str")
        
        # get personal invader list
        client_invader_path = "data/" + self.client + ".txt"
        with open(client_invader_path) as f:
            client_invader_list = f.readlines()
        client_invader_list = list(map(lambda x: "PA_" + x.strip().zfill(4), client_invader_list))
        merged_df.loc[merged_df["ID"].isin(client_invader_list), "Color"] = "blue"
        return merged_df
        
    def classify_invader(self, x):
        if x == "Détruit !":
            return "red"    
        elif x == "Très dégradé" :
            return "orange"
        elif x == "Dégradé" :
            return "yellow"
        elif x == "Un peu dégradé":
            return "white"
        elif x == "Non visible":
            return "grey"
        else:
            return "green"
        
    def generate_kml(self):
        df = self.merged_df
        kml = Kml()
        
        color_map = {"red":'ff0000ff', 
                     "orange":'ff00a5ff', 
                     "yellow":'ffe0ffff', 
                     "white":'fff0ffff', 
                     "grey":'ffd3d3d3',
                     "blue":'ffe6d8ad',
                     "green":'ff90ee90'}
        
        for _, line in df.iterrows():
            pnt = kml.newpoint()
            pnt.name = line["ID"]
            pnt.description = line["Address"]
            color = line["Color"]
            path = kml.addfile(f"data/icons/{color}.png")
            pnt.description = '<img src="' + path +'" alt="picture" width="400" height="300" align="left" />'
            # pnt.style.iconstyle.color = simplekml.Color.hex(color_map[line["Color"]])
            pnt.coords = [(line["Longitude"], line["Latitude"])]
        kml.save("data/invader.kml")
        
    def display(self):
        # Initialize the map at a given point
        gmap = gmplot.GoogleMapPlotter(48, 2, 5)
        
        # Add current position, blur point
        # g = geocoder.ip('me')
        # gmap.marker(g.latlng[0], g.latlng[1], color="pink")
        
        for _, line in self.merged_df.iterrows():
            if not isnan(line["Latitude"]):
                line["Address"] = "" if line["Address"] else line["Address"]
                gmap.marker(line["Latitude"], line["Longitude"], info_window=line["ID"] + " - - " + line["Address"], color=line["Color"])
        
        # Draw map into HTML file
        gmap.draw(f"{self.client}.html")


if __name__ == "__main__":
    Inva = Invaders("nuoya")
    Inva.display()