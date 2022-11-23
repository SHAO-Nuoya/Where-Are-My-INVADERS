import pandas as pd

def modify_data(client:str):
    file_name = "data/" + client+".txt"
    print(file_name)
    with open(file_name) as file:
        lines = file.readlines()
        lines = list(map(lambda x:x.strip(), lines))
        lines.reverse()
    df = pd.DataFrame(lines, columns=["Paris"])
    df.to_csv(f"data/{client}.csv", index=False)

def clean_address_data():
    address_df = pd.read_csv("data/address.csv", delimiter=";")
    address_df["Address"].fillna("Unknown", inplace=True)
    address_df["Address"] = address_df["Address"].astype("str").apply(lambda x:x.strip())
    address_df["Address"] = address_df["Address"].apply(lambda item : item.encode('cp1252', errors='replace').decode('cp1252'))
    
    address_df[["Latitude", "Longitude"]] = address_df[["Latitude", "Longitude"]].astype("float")
    address_df.sort_values(by="ID", inplace=True)
    address_df.to_csv("data/address.csv", index=False, encoding="utf-8", sep=";")

def clean_info_data():
    info_df = pd.read_csv("data/info.csv", delimiter=";")
    info_df.to_csv("data/info.csv", index=False, encoding="utf-8", sep=";")
    
if __name__ == "__main__":
    clean_address_data()
    clean_info_data()
    # modify_data("xueying")