# NFV-Clearwater压力测试及性能数据分析实验

## 一、SLA 压力测试实验

实验环境及部署参考[这里](https://github.com/XLab-Tongji/KDD-CUP99-Modeling/blob/master/clearwater%E5%AE%9E%E9%AA%8C/doc)，heapster及influxdb相关配置参考 Influxdb.md.

### 1、实验过程

#### (1) 创建虚拟用户

进入 cassandra 节点,  cassandra 容器

执行：

```shell
/usr/share/clearwater/crest-prov/src/metaswitch/crest/tools/stress_provision.sh 1000
```

#### (2) 执行压测脚本

1）进入 stress-ng 节点， stress-ng 容器
2）删掉 /var/log/clearwater-sip-stress 目录下所有文件
3）进入 /root 目录下创建 stress.sh 脚本，内容为 node_stress.sh 文件内容，其中 stress_time 变量代表每次压力测试的执行时间，单位为分钟。执行：

```shell
nohup sh stress.sh &
```

接下来等待实验结束，开始收集数据即可。

### 2、数据收集

#### (1) 清空原有数据

删除 ./data/sla/node , ./data/sla/pod_container, ./data/sla/stress_log 目录下的文件

#### (2) 收集sla_log数据

1）拷贝文件到宿主机：在 stress-ng 节点执行

```shell
docker cp $(docker ps | grep rainlf/clearwater-stress-ng |awk {'print $1'}):/var/log/clearwater-sip-stress ./
docker cp $(docker ps | grep rainlf/clearwater-stress-ng |awk {'print $1'}):/root/nohup.out ./clearwater-sip-stress
```

2）从stress-ng节点拷贝数据到master节点：在master节点执行

```shell
mkdir clearwater-sip-stress
scp root@192.168.1.33:/root/clearwater-sip-stress/* ./clearwater-sip-stress
cd clearwater-sip-stress
rm -f *_errors.log 		# 删除无用的 error log
```

注：若已经存在clearwater-sip-stress目录，则第1条不需要，但需要删除该目录下的所有文件。

192.168.1.33 为stress-ng 节点的ip地址

3）从master节点拷贝数据到本地：在本地执行

```shell
mkdir ~/Desktop/clearwater-sip-stress
scp -P 9000 root@lab205.jios.org:/root/clearwater-sip-stress/\* ~/Desktop/clearwater-sip-stress
```

4）将 *_caller_status.log 文件拷贝到 ./data/sla/stress_log 目录下

#### (3) 收集虚机层数据

查看 node_metrics.sh 文件

#### (4) 收集容器层数据

查看 data_request.py， 修改 main 函数中对应路径， 修改 get_container_data 函数中 startTime 和 endTime

并执行之。

#### (5) 给容器层数据打上sla标签

这一步包括了将 stress_log 数据合并的操作，需要在步骤6之前进行

查看 data_combine.py，修改 main 函数中对应调用的函数，并执行之。

#### (6) 给虚机层数据打上sla标签

查看 data_label.py,  修改 main 函数中对应的调用函数，并执行之。

#### (7) 数据清洗

这一步是删除 sla_level == -1 的数据和 successful rate < 0 的数据

执行 data_wash.py





## 二、故障注入实验

### 1、实验过程

#### (1) 同实验一创建用户

#### (2) 执行压力测试脚本

进入 stress-ng 节点， stress-ng 容器，执行

```shell
nohup /usr/share/clearwater/bin/run_stress default.svc.cluster.local \
            500 120  --initial-reg-rate 100 \
            --multiplier 450 &
```

#### (3) 执行故障注入脚本

在 master 节点执行：

```shell
nohup ./stress.py 120 &
```

### 2、数据收集

#### (1) 删除原有数据

删除 ./data/fault_load/node , ./data/fault_load/pod_container, ./data/fault_load/stress_log 目录下的文件

#### (2) 收集故障 log 数据并分离

参考实验一中方法将stress.log数据从master节点下载到本地，并放入 ./data/fault_load/fault_log 目录下，要求文件名必须为stress.log。

执行 stress_seprate.py 将数据分离

#### (3) 参考实验一收集虚机层和容器层数据

#### (4) 给虚机层数据打上 faultload 标签

查看 data_label.py，修改 main 函数

#### (5) 给容器层数据打上 faultload 标签 

查看 data_combine.py，修改 main 函数



## 三、数据分析

@author：[lyqun](https://github.com/lyqun)

SLA 实验：lab2_sla.ipynb

faultload 实验：lab3_faultload.ipynb





