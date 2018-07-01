## Collect data from InfluxDB

### 一、在 k8s 中的配置

1. 设置heapster收集数据的间隔为 t 秒

   在 k8s UI 中，选择命名空间为 kube-system，在 deployments 中找到 heapster，修改其 .yaml 文件。在command中增加命令 "--metric_resolution=ts"

   (参考源码：https://github.com/kubernetes/heapster/blob/master/metrics/options/options.go)

2. 暴露 influxdb 的对外端口

   在 kube-system 下，从 services 中找到 influxdb，修改器 .yaml 文件。将 type 从 "ClusterIP" 修改为 "NodePort"，在ports 下添加 "nodePort"={PORT}

   (PORT 设置值参考：https://github.com/XLab-Tongji/KDD-CUP99-Modeling/blob/master/clearwater%E5%AE%9E%E9%AA%8C/doc/address.md)

### 二、使用 influxdb 接口获取数据

#### 参考文档

- 官方文档参考： https://docs.influxdata.com/influxdb/v1.5/guides/querying_data/
- 中文资料：https://www.kubernetes.org.cn/936.html

#### 使用说明(以端口30001为例)

API:    http://lab205.jios.org:30001/query?db=k8s&pretty=true&q={SQL}

选项说明:

- db:       数据库名 (这里为k8s)
- epoch: 指定返回数据的时间格式为UNIX时间戳，并指定精度      可选值： ns/ms/s/m/h
- pretty: 是否格式化JSON输出     可选值：true/false

示例：

```shell
# 查看接口是否正常工作
curl -i 'http://lab205.jios.org:30001/ping' 
# 调用接口获取数据
curl -G 'http://lab205.jios.org:30001/query?db=k8s' --data-urlencode 'q={SQL}'
# 获取数据库的所有表
curl -G 'http://lab205.jios.org:30001/query?db=k8s' --data-urlencode 'q=SHOW MEASUREMENTS' 
```

SQL：

```sql
-- 使用API查询时需要注意的语法问题：
-- -- SQL中表名可以用 "" 括起来，也可以不用
-- -- 字符串数据只能用 '' 括起来
-- -- 需要指定时间区间时，目前只发现能用 WHERE time > now() - 5m 类似的相对当前时间的时间区间
-- -- 其他语法与普通SQL一致

-- 查询所有数据库名
SHOW DATABASES
-- 查询所有数据库表
SHOW MEASUREMENTS

SELECT * FROM "cpu/usage_rate" WHERE time > now() - 5m AND type = 'pod_container' AND container_name = 'sprout' ORDER BY time LIMIT 5
```



#### 其他说明

- 当需要收集 filesystem/... 的数据时，会有个标签叫 resource_id，可能表示不同磁盘的挂载点。收集 container 层的数据时，这部分数据只有一份，即不存在一个 container 对应多个 resource_id 的多个 filesystem/... 数据。收集 node 层的数据时，这部分数据可能有多份，即存在一个 node 对应多个 resource_id 的多个 filesystem/... 数据
- container的type有两种，分别为 sys_container 和 pod_container，在指定type时需要注意。