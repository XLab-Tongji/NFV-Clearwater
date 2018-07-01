# 拷贝容器文件到宿主机(stress-ng执行)
docker cp $(docker ps | grep rainlf/clearwater-stress-ng |awk {'print $1'}):/var/log/clearwater-sip-stress ./
docker cp $(docker ps | grep rainlf/clearwater-stress-ng |awk {'print $1'}):/root/nohup.out ./clearwater-sip-stress

# 从stress-ng拷贝数据到zabbix-server (zabbix-server执行)
mkdir clearwater-sip-stress
scp root@192.168.1.33:/root/clearwater-sip-stress/* ./clearwater-sip-stress
# 删除无用的 errors.log文件
cd clearwater-sip-stress
rm *_errors.log

# 从zabbix-server拷贝数据到本地 (本地执行)
mkdir ~/Desktop/clearwater-sip-stress
scp -P 9000 root@lab205.jios.org:/root/clearwater-sip-stress/\* ~/Desktop/clearwater-sip-stress

