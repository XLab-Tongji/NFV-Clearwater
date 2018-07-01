import pandas as pd 



def wash_data(file_name):
    data = pd.read_csv(file_name)
    row_to_delete = []
    for index, row in data.iterrows():
        if int(row["sla level"]) == -1:
            row_to_delete.append(index)
        else:
            successful_rate = float(row["successful rate"].split("%")[0]) / 100.0
            if successful_rate < 0:
                row_to_delete.append(index)
    data = data.drop(row_to_delete)
    data.to_csv(file_name, index=None)


def main():
    top_dir = "./data/sla"
    wash_data(top_dir + "/node/sla-level.csv")
    wash_data(top_dir + "/pod_container/sla_level_container.csv")

if __name__ == '__main__':
    main()