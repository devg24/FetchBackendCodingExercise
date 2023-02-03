import pandas as pd


import sys


def main():
    # get file name and points from arguments
    file_name = "./transactions.csv"
    if len(sys.argv) < 1:
        raise Exception("Please provide points to deduct")
    points = int(sys.argv[1])

    # read csv file
    df = pd.read_csv(file_name)

    if ("payer" not in df.columns or "points" not in df.columns or "timestamp" not in df.columns):
        raise Exception("Invalid file format")

    # calculate current points of each payer as a dictionary
    current_points = df.groupby("payer").sum()["points"]
    current_points = current_points.to_dict()

    # sort transactions by timestamp
    df = df.sort_values(by="timestamp")

    # deduct points based on oldest timestamp making sure that no payers go negative
    for index, row in df.iterrows():
        if points == 0:
            break
        if current_points[row["payer"]] - row["points"] < 0 :
            continue
        else:
            current_points[row["payer"]] -= min(row["points"], points)
            points -= min(row["points"], points)
    
    # print output
    for payer, points in current_points.items():
        print(f"{payer}: {points}")
    
    

if __name__ == "__main__":
    main()
