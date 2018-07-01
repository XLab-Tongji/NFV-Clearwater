import requests
import pandas as pd
import time
import json
import os


url = "http://lab205.jios.org:30001/query"
timeout = 10


def getMetrics(file="./metrics.json"):
    with open(file, 'r') as f:
        jsonString = f.read()
        jsonObj = json.loads(jsonString)
        metricsArray = jsonObj["results"][0]["series"][0]["values"]
        metrics = []
        for obj in metricsArray:
            metrics.append(obj[0])
        return metrics


# 解析请求返回数据
# 有数据则返回 pd.DataFrame, 由 timestamp + 维度数据 两列组成
# 无数据返回空的 pd.DataFrame
def parse(metric, jsonObj):
    try:
        serie = jsonObj["results"][0]["series"][0]
        columns = serie["columns"]
        tIndex = columns.index("time")
        vIndex = columns.index("value")

        valueArray = serie["values"]
        values = []
        timestampes = []
        for obj in valueArray:
            values.append(obj[vIndex])
            timestampes.append(obj[tIndex])

        newDF = pd.DataFrame()
    
        newDF["timestamp"] = timestampes
        newDF[metric] = values
        return newDF
    except:
        return pd.DataFrame()


# 获取一段时间内某层某对象某个维度的数据
# 返回 pd.DataFrame, 由 timestamp + 维度数据 两列组成
def getMetricData(metric, columnType, name, startTime, endTime):
    startTimestamp = int(time.mktime(time.strptime(startTime, "%Y-%m-%d %H:%M:%S")))
    endTimestamp = int(time.mktime(time.strptime(endTime, "%Y-%m-%d %H:%M:%S")))
    now = time.time()
    # 计算两个目标时间节点与当前时间的分钟差值(用于查询语句中)
    startDiffMin = int((now - startTimestamp)/60)
    endDiffMin = int((now - endTimestamp)/60)

    typeConstraint = ""
    if columnType == "node":
        typeConstraint = " AND nodename = '" + name + "'"
    elif columnType == "pod_container" or columnType == "sys_container":
        typeConstraint = " AND container_name = '" + name + "'"
    elif columnType == "pod":
        typeConstraint = " AND pod_name = '" + name + "'"
    else:
        raise RuntimeError("column type error")
      
    query = "SELECT * FROM \"" + metric + \
        "\" WHERE time > now() - " + str(startDiffMin) + "m" + \
        " AND time < now() - " + str(endDiffMin) + "m" + \
        " AND type = '" + columnType + "'" + \
        typeConstraint + \
        " ORDER BY time"

    # InfluxDB 请求参数
    # db:    数据库名
    # epoch: 指定返回的时间格式为UNIX时间戳，并指定其精确度，可选值为 ns/ms/s/m/h
    # q:     SQL 查询语句
    params = {"db": "k8s", "epoch": "s", "q": query}
    response = requests.get(url, params=params, timeout=timeout)
    jsonObj = response.json()
    # 返回的 json 对象交由`parse`函数解析
    return parse(metric, jsonObj)


# 通过相同的时间戳合并两份 pd.DataFrame
def mergeDataFrame(origin, newDF):
    if origin.empty:
        return newDF.copy()
    else:
        return pd.merge(origin, newDF, on="timestamp")


# 收集一段时间内某层次内某对象的`metricsArray`指定的指标数据
def collectData(columnType, name, metricsArray, startTime, endTime):
    df = pd.DataFrame()
    for metric in metricsArray:
        newDF =  getMetricData(metric, columnType, name, startTime, endTime)
        if newDF.empty:
            continue
        print(newDF)
        df = mergeDataFrame(df, newDF)
    return df


containers = ["homestead", "sprout", "bono"]


def get_container_data(top_dir):
    startTime = "2018-6-21 17:58:00"
    endTime = "2018-6-21 19:58:00"
    # 层次类型
    types = ["node", "pod", "pod_container", "sys_container"]
    columnType = types[2]
    # 获取所有维度指标
    metricsArray = getMetrics()

    folder = top_dir + "/" + columnType
    if not os.path.exists(folder):
        os.mkdir(folder)
    # 收集该层内所有对象的数据并存储为.csv文件
    for name in containers:
        data = collectData(columnType, name, metricsArray, startTime, endTime)
        print(data)
        print(data.keys().tolist())
        file_name = folder +  "/" + name + ".csv"
        data.to_csv(file_name, index=None)
    

def main():
    # for sla experiment
    top_dir = "./data/sla"
    # for fault_load experiment
    # top_dir = "./data/fault_load"
    get_container_data(top_dir)


if __name__ == '__main__':
    main()
