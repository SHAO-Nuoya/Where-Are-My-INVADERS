from gmplot import gmplot
import pandas as pd
from zipfile import ZipFile
from pykml.factory import KML_ElementMaker as KML
from lxml import etree


class Invaders:
    def __init__(self, client: str, address_path: str = "data/address.csv", info_path: str = "data/info.csv") -> None:
        self.address_path = address_path
        self.info_path = info_path
        self.client = client
        self.merged_df = self.gather_all_info()
        self.generate_kmz()

    def gather_all_info(self):
        address_df = pd.read_csv(self.address_path, delimiter=";")
        info_df = pd.read_csv(self.info_path, delimiter=";")
        merged_df = pd.merge(address_df, info_df, how="outer")
        merged_df["Color"] = merged_df["State"].apply(self.classify_invader)
        # merged_df["Address"] = merged_df["Address"].astype("str")

        # get personal invader list
        client_invader_path = "data/" + self.client + ".csv"
        client_invader_df = pd.read_csv(client_invader_path).fillna(0)
        client_invader_df = client_invader_df.astype("int")

        # todo
        abbre_dic = {"Paris": "PA", "Versailles": "VRS", "Avignon": "AVI",
                     "Rennes": "RN", "Rome": "ROM", "Toulouse": "TLS"}
        client_invader_list = []
        for col in client_invader_df.columns:
            client_invader_list.extend(list(map(lambda x: abbre_dic[col] + "_" + str(
                x).strip().zfill(4), client_invader_df[col].values.tolist())))

        merged_df.loc[merged_df["ID"].isin(
            client_invader_list), "Color"] = "pink"
        merged_df.to_csv("data/merged_df.csv", index=False, sep=";")
        return merged_df

    def classify_invader(self, x):
        if x == "Détruit !":
            return "black"
        elif x == "Très dégradé":
            return "red"
        elif x == "Dégradé":
            return "orange"
        elif x == "Un peu dégradé":
            return "yellow"
        elif x == "Non visible":
            return "grey"
        else:
            return "blue"

    def generate_kmz(self):
        # create a ZipFile object
        fld = KML.Folder()
        draw_df = self.merged_df.dropna(subset=["Latitude"])
        for _, line in draw_df.iterrows():
            name = line['ID']
            href = f"data/icons/{line['Color']}.png"
            coordinates = str(line["Longitude"]) + \
                ',' + str(line["Latitude"])

            kml = KML.Placemark(
                KML.name(name),
                KML.Style(
                    KML.IconStyle(
                        KML.scale(1.0),
                        KML.Icon(
                            KML.href(href)
                        )
                    )
                ),
                KML.Point(
                    KML.coordinates(coordinates)
                ),
                KML.description('<table border="1">'
                                '<tr><th>Lat, Long : </th><td>{lat:.4f}, {lon:.4f}</td>'
                                '<tr><th>Point : </th><td>{point}</td>'
                                '<tr><th>Address : </th><td>{add}</td>'
                                '<tr><th>Source date : </th><td>{date}</td>'
                                '</table>'.format(
                                    lat=line["Latitude"],
                                    lon=line["Longitude"],
                                    point=line["Point"],
                                    add=line["Address"],
                                    date=line["Source_date"])
                                )
            )

            fld.append(kml)

        with ZipFile(f'result/{self.client}.kmz', 'w') as zipObj:
            # serialize KML to a string
            kml_str = etree.tostring(fld, pretty_print=True,
                                     xml_declaration=True, encoding='UTF-8')

            zipObj.writestr('invader.kml', kml_str)   # Add doc.kml entry

            for color in ["black", "green", "blue", "grey", "orange", "pink", "red", "yellow"]:
                image = f"data/icons/{color}.png"
                zipObj.write(image)        # Add icon to the zip

    def display(self):
        # Initialize the map at a given point
        gmap = gmplot.GoogleMapPlotter(48, 2, 5)

        # Add current position, blur point
        # g = geocoder.ip('me')
        # gmap.marker(g.latlng[0], g.latlng[1], color="pink")

        draw_df = self.merged_df.dropna(subset=["Latitude"])
        for _, line in draw_df.iterrows():
            info = line['ID']
            # line["Address"] = " " if not line["Address"] else line["Address"]
            gmap.marker(line['Latitude'], line['Longitude'], info_window=str(
                info), color=line["Color"], encoding="utf-8")

        # Draw map into HTML file
        gmap.draw(f"result/{self.client}.html")

    
if __name__ == "__main__":
    Inva = Invaders("nuoya")
    Inva.display()
