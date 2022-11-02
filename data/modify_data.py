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

modify_data("xueying")