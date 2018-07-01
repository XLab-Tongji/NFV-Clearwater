import pandas as pd
import re
import os


def read_sla(sla_file):
    info_list = []
    with open(sla_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            elements = line.split(';')
            info_list.append((elements[1], elements[10], elements[16]))
    
    sla_list = []
    for info in info_list[1:]:
        if info[1] == '0':
            continue
        sla_list.append((info[0].split('\t')[2].split('.')[0], float(info[2]) / float(info[1])))
    return sla_list


def transfer_sl(key):
    if None == key:
        return ['-1', 'no match']
    elif key > 0.9:
        return ['2', '%0.2f%%' % ((1-key)*100)]
    elif key > 0.5:
        return ['1', '%0.2f%%' % ((1-key)*100)]
    else:
        return ['0', '%0.2f%%' % ((1-key)*100)]


def match(row, sla_list):
    time = int(row["timestamp"])
    for sla in sla_list:
        sla_time = int(sla[0])
        if time > sla_time and time < sla_time + 60:
            result = transfer_sl(sla[1])
            return result
    result = transfer_sl(None)
    return result


def label_container_sla():
    top_dir = "./data/sla"
    sla_list = read_sla(top_dir + "/stress_log/sla.log")
    container_data = pd.read_csv(top_dir + "/pod_container/containers.csv")
    container_data["sla level"] = -1
    container_data["successful rate"] = 0
    for index, row in container_data.iterrows():
        result = match(row, sla_list)
        container_data.loc[index, ["sla level", "successful rate"]] = result

    container_data.to_csv(top_dir + "/pod_container/sla_level_container.csv", index=None)


def combine_log():
    stress_log_dir = "./data/sla/stress_log"
    files = os.listdir(stress_log_dir)
    files.sort()
    data = pd.DataFrame()
    for f in files:
        if re.match(r'(.*)caller_stats.log', f):
            if data.empty:
                data = pd.read_csv(stress_log_dir+"/"+f, sep=";")
                data = data[1:-1]
            else:
                tmp_data = pd.read_csv(stress_log_dir+"/"+f, sep=";")
                tmp_data = tmp_data[1:-1]
                data = data.append(tmp_data, ignore_index=True)
    data.to_csv(stress_log_dir+"/sla.log", sep=";", index=None)


def data_merge():
    print("start merge ...")
    containers_dir = "./data/sla/pod_container"
    df = pd.DataFrame()
    containers = ["homestead", "sprout", "bono"]
    for item in containers:
        column_dict = {}   
        itemDf = pd.read_csv(containers_dir+"/"+item+".csv")
        for value in itemDf.columns.values:
            if value == "timestamp":
                continue
            column_dict[value] = item + "_" + value
        itemDf.rename(columns=column_dict, inplace=True)
        if df.empty:
            df = itemDf
        else:
            df = pd.merge(df, itemDf, on="timestamp")
    df.to_csv(containers_dir+"/containers.csv", index=None)
    print("Done!")


def sla():
    combine_log()
    data_merge()
    label_container_sla()


def read_log(log):
    rule = []
    with open(log, 'r') as file:
        lines = file.readlines()

    for line in lines:
        context = line.split(', ')
        rule.append((context[3], context[2], context[1]))
    
    return rule

def transfer_fl(key):
    dic = {'cpu': [0, 1, 0, 0], 'mem': [0, 0, 1, 0], 'io': [0, 0, 0, 1]}
    if None == key:
        return [1, 0, 0, 0] # normal
    else:
        return dic[key]

def match_rule(row, rule):
    timestamp = row['timestamp']
    for r in rule:
        if int(timestamp) > int(r[0]) and int(timestamp) < int(r[0]) + int(r[1])*60:
            return transfer_fl(r[2])
    return transfer_fl(None)
    

def rename_columns(component, columns):
    rename_dict = {}
    for col in columns:
        if col == "timestamp":
            continue
        rename_dict[col] = component + "_" + col
    return rename_dict



def merge_fault_load_data():
    top_dir = "./data/fault_load"
    container_dir = top_dir + "/pod_container"
    df = pd.DataFrame()
    label_df = pd.DataFrame()
    label_columns = ['timestamp', 'cpu', 'mem', 'io']
    for component in ['bono', 'homestead', 'sprout']:
        data = pd.read_csv('%s/faultload-%s.csv' % (container_dir, component))
        all_columns = data.columns.values
        performance_columns = ['timestamp', 'normal']
        for col in all_columns:
            if col in label_columns:
                continue
            performance_columns.append(col)
        label_data = data[label_columns].copy()
        rename_dict = rename_columns(component, label_columns)
        label_data.rename(columns=rename_dict, inplace=True)

        performance_data = data[performance_columns].copy()
        rename_dict = rename_columns(component, performance_columns)
        performance_data.rename(columns=rename_dict, inplace=True)
        if df.empty:
            df = performance_data
        else:
            df = pd.merge(df, performance_data, on="timestamp")
        if label_df.empty:
            label_df = label_data
        else:
            label_df = pd.merge(label_df, label_data, on="timestamp")
    
    normal_data = []
    for _, row in label_df.iterrows():
        label = row.values[1:]
        normal = True
        for i in label:
            if i != 0:
                normal = False 
                break
        if normal:
            normal_data.append(1)
        else:
            normal_data.append(0)
    label_df["normal"] = normal_data
    com_df = pd.merge(df, label_df, on="timestamp")
    com_df.to_csv("%s/faultload_container.csv" % container_dir, index=None)



def fault_load():
    top_dir = "./data/fault_load"
    fault_dir = top_dir + "/fault_log"
    container_dir = top_dir + "/pod_container"
    labels = ['normal', 'cpu', 'mem', 'io']
    for component in ['bono', 'homestead', 'sprout']:
        rule = read_log('%s/%s-stress.log' % (fault_dir, component))
        data = pd.read_csv('%s/%s.csv' % (container_dir, component))
        for label in labels:
            data[label] = 0
        for index, row in data.iterrows():
            result = match_rule(row, rule)
            data.loc[index, labels] = result
        data.to_csv("%s/faultload-%s.csv" % (container_dir, component), index=None)
    merge_fault_load_data()


def main():
    # for sla experiment
    sla()
    # for faultload experiment
    # fault_load()


if __name__ == '__main__':
    main()
