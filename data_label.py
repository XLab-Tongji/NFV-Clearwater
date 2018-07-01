#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd
import csv

# items
const_items = [u'host', u'clock', u'net.if.in[ens160]', u'net.if.out[ens160]', u'proc.num[,,run]', u'proc.num[]', u'system.cpu.intr', u'system.cpu.load[percpu,avg1]', u'system.cpu.load[percpu,avg15]', u'system.cpu.load[percpu,avg5]', u'system.cpu.switches', u'system.cpu.util[,idle]', u'system.cpu.util[,interrupt]', u'system.cpu.util[,iowait]', u'system.cpu.util[,nice]', u'system.cpu.util[,softirq]', u'system.cpu.util[,steal]', u'system.cpu.util[,system]',u'system.cpu.util[,user]', u'system.swap.size[,free]', u'system.swap.size[,pfree]', u'system.swap.size[,total]', u'vfs.fs.inode[/,pfree]', u'vfs.fs.inode[/boot,pfree]', u'vfs.fs.inode[/var/lib/docker/aufs,pfree]', u'vfs.fs.inode[/var/lib/kubelet,pfree]', u'vfs.fs.inode[/var/lib/rancher/volumes,pfree]', u'vfs.fs.size[/,pfree]', u'vfs.fs.size[/,total]', u'vfs.fs.size[/,used]', u'vfs.fs.size[/boot,free]', u'vfs.fs.size[/boot,pfree]', u'vfs.fs.size[/boot,total]', u'vfs.fs.size[/boot,used]', u'vfs.fs.size[/var/lib/docker/aufs,pfree]', u'vfs.fs.size[/var/lib/docker/aufs,total]', u'vfs.fs.size[/var/lib/docker/aufs,used]', u'vfs.fs.size[/var/lib/kubelet,free]', u'vfs.fs.size[/var/lib/kubelet,pfree]', u'vfs.fs.size[/var/lib/kubelet,total]', u'vfs.fs.size[/var/lib/kubelet,used]', u'vfs.fs.size[/var/lib/rancher/volumes,free]', u'vfs.fs.size[/var/lib/rancher/volumes,pfree]', u'vfs.fs.size[/var/lib/rancher/volumes,total]', u'vfs.fs.size[/var/lib/rancher/volumes,used]', u'vm.memory.size[available]', u'vm.memory.size[total]']
const_imtes_combine = [u'clock', u'bono_net.if.in[ens160]', u'bono_net.if.out[ens160]', u'bono_proc.num[,,run]', u'bono_proc.num[]', u'bono_system.cpu.intr', u'bono_system.cpu.load[percpu,avg1]', u'bono_system.cpu.load[percpu,avg15]', u'bono_system.cpu.load[percpu,avg5]', u'bono_system.cpu.switches', u'bono_system.cpu.util[,idle]', u'bono_system.cpu.util[,interrupt]', u'bono_system.cpu.util[,iowait]', u'bono_system.cpu.util[,nice]', u'bono_system.cpu.util[,softirq]', u'bono_system.cpu.util[,steal]', u'bono_system.cpu.util[,system]', u'bono_system.cpu.util[,user]', u'bono_system.swap.size[,free]', u'bono_system.swap.size[,pfree]', u'bono_system.swap.size[,total]', u'bono_vfs.fs.inode[/,pfree]', u'bono_vfs.fs.inode[/boot,pfree]', u'bono_vfs.fs.inode[/var/lib/docker/aufs,pfree]', u'bono_vfs.fs.inode[/var/lib/kubelet,pfree]', u'bono_vfs.fs.inode[/var/lib/rancher/volumes,pfree]', u'bono_vfs.fs.size[/,pfree]', u'bono_vfs.fs.size[/,total]', u'bono_vfs.fs.size[/,used]', u'bono_vfs.fs.size[/boot,free]', u'bono_vfs.fs.size[/boot,pfree]', u'bono_vfs.fs.size[/boot,total]', u'bono_vfs.fs.size[/boot,used]', u'bono_vfs.fs.size[/var/lib/docker/aufs,pfree]', u'bono_vfs.fs.size[/var/lib/docker/aufs,total]', u'bono_vfs.fs.size[/var/lib/docker/aufs,used]', u'bono_vfs.fs.size[/var/lib/kubelet,free]', u'bono_vfs.fs.size[/var/lib/kubelet,pfree]', u'bono_vfs.fs.size[/var/lib/kubelet,total]', u'bono_vfs.fs.size[/var/lib/kubelet,used]', u'bono_vfs.fs.size[/var/lib/rancher/volumes,free]', u'bono_vfs.fs.size[/var/lib/rancher/volumes,pfree]', u'bono_vfs.fs.size[/var/lib/rancher/volumes,total]',u'bono_vfs.fs.size[/var/lib/rancher/volumes,used]', u'bono_vm.memory.size[available]', u'bono_vm.memory.size[total]', u'homestead_net.if.in[ens160]', u'homestead_net.if.out[ens160]', u'homestead_proc.num[,,run]', u'homestead_proc.num[]', u'homestead_system.cpu.intr', u'homestead_system.cpu.load[percpu,avg1]', u'homestead_system.cpu.load[percpu,avg15]', u'homestead_system.cpu.load[percpu,avg5]', u'homestead_system.cpu.switches', u'homestead_system.cpu.util[,idle]', u'homestead_system.cpu.util[,interrupt]', u'homestead_system.cpu.util[,iowait]', u'homestead_system.cpu.util[,nice]', u'homestead_system.cpu.util[,softirq]', u'homestead_system.cpu.util[,steal]', u'homestead_system.cpu.util[,system]', u'homestead_system.cpu.util[,user]', u'homestead_system.swap.size[,free]', u'homestead_system.swap.size[,pfree]', u'homestead_system.swap.size[,total]', u'homestead_vfs.fs.inode[/,pfree]', u'homestead_vfs.fs.inode[/boot,pfree]', u'homestead_vfs.fs.inode[/var/lib/docker/aufs,pfree]', u'homestead_vfs.fs.inode[/var/lib/kubelet,pfree]', u'homestead_vfs.fs.inode[/var/lib/rancher/volumes,pfree]', u'homestead_vfs.fs.size[/,pfree]', u'homestead_vfs.fs.size[/,total]', u'homestead_vfs.fs.size[/,used]', u'homestead_vfs.fs.size[/boot,free]', u'homestead_vfs.fs.size[/boot,pfree]', u'homestead_vfs.fs.size[/boot,total]', u'homestead_vfs.fs.size[/boot,used]', u'homestead_vfs.fs.size[/var/lib/docker/aufs,pfree]', u'homestead_vfs.fs.size[/var/lib/docker/aufs,total]', u'homestead_vfs.fs.size[/var/lib/docker/aufs,used]', u'homestead_vfs.fs.size[/var/lib/kubelet,free]', u'homestead_vfs.fs.size[/var/lib/kubelet,pfree]', u'homestead_vfs.fs.size[/var/lib/kubelet,total]', u'homestead_vfs.fs.size[/var/lib/kubelet,used]', u'homestead_vfs.fs.size[/var/lib/rancher/volumes,free]', u'homestead_vfs.fs.size[/var/lib/rancher/volumes,pfree]', u'homestead_vfs.fs.size[/var/lib/rancher/volumes,total]', u'homestead_vfs.fs.size[/var/lib/rancher/volumes,used]', u'homestead_vm.memory.size[available]', u'homestead_vm.memory.size[total]', u'sprout_net.if.in[ens160]', u'sprout_net.if.out[ens160]', u'sprout_proc.num[,,run]', u'sprout_proc.num[]', u'sprout_system.cpu.intr', u'sprout_system.cpu.load[percpu,avg1]', u'sprout_system.cpu.load[percpu,avg15]', u'sprout_system.cpu.load[percpu,avg5]', u'sprout_system.cpu.switches', u'sprout_system.cpu.util[,idle]', u'sprout_system.cpu.util[,interrupt]', u'sprout_system.cpu.util[,iowait]', u'sprout_system.cpu.util[,nice]', u'sprout_system.cpu.util[,softirq]', u'sprout_system.cpu.util[,steal]', u'sprout_system.cpu.util[,system]', u'sprout_system.cpu.util[,user]', u'sprout_system.swap.size[,free]', u'sprout_system.swap.size[,pfree]', u'sprout_system.swap.size[,total]', u'sprout_vfs.fs.inode[/,pfree]', u'sprout_vfs.fs.inode[/boot,pfree]', u'sprout_vfs.fs.inode[/var/lib/docker/aufs,pfree]', u'sprout_vfs.fs.inode[/var/lib/kubelet,pfree]', u'sprout_vfs.fs.inode[/var/lib/rancher/volumes,pfree]', u'sprout_vfs.fs.size[/,pfree]', u'sprout_vfs.fs.size[/,total]', u'sprout_vfs.fs.size[/,used]', u'sprout_vfs.fs.size[/boot,free]', u'sprout_vfs.fs.size[/boot,pfree]', u'sprout_vfs.fs.size[/boot,total]', u'sprout_vfs.fs.size[/boot,used]', u'sprout_vfs.fs.size[/var/lib/docker/aufs,pfree]', u'sprout_vfs.fs.size[/var/lib/docker/aufs,total]', u'sprout_vfs.fs.size[/var/lib/docker/aufs,used]', u'sprout_vfs.fs.size[/var/lib/kubelet,free]', u'sprout_vfs.fs.size[/var/lib/kubelet,pfree]', u'sprout_vfs.fs.size[/var/lib/kubelet,total]', u'sprout_vfs.fs.size[/var/lib/kubelet,used]', u'sprout_vfs.fs.size[/var/lib/rancher/volumes,free]', u'sprout_vfs.fs.size[/var/lib/rancher/volumes,pfree]', u'sprout_vfs.fs.size[/var/lib/rancher/volumes,total]', u'sprout_vfs.fs.size[/var/lib/rancher/volumes,used]', u'sprout_vm.memory.size[available]', u'sprout_vm.memory.size[total]']
const_fault_label = ['normal', 'bono_cpu', 'bono_mem', 'bono_io', 'homestead_cpu', 'homestead_mem', 'homestead_io', 'sprout_cpu', 'sprout_mem', 'sprout_io']

# path
data_dir = './data'
raw_data_dir = './raw_data'

def write_to_csv(file, data):
    with open(file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def read_xlsx(file):
    sheet = xlrd.open_workbook(file).sheet_by_index(0)
    # drop the frist and last record
    for i in range(1, sheet.nrows - 1):
        yield sheet.row_values(i)

def combine_data(bono_file, homestead_file, sprout_file):
    bono_data = []
    homestead_data = []
    sprout_data = []
    for data in read_xlsx(bono_file):
        bono_data.append(data)
    for data in read_xlsx(homestead_file):
        homestead_data.append(data)
    for data in read_xlsx(sprout_file):
        sprout_data.append(data)

    list_length = min(len(bono_data), len(homestead_data), len(sprout_data))
    combination_data = []
    for i in range(len(bono_data)):
        combination_data.append(bono_data[i][1:] + homestead_data[i][2:] + sprout_data[i][2:])

    return combination_data

def transfer_wl(key):
    dic = {'05': '0.5', '10': '1.0', '15': '1.5', '20': '2.0', '25': '2.5'}
    return dic[key]

def auto_label_workload():
    levels = ['05', '10', '15', '20', '25']

    label = ['workload level']
    sum_com_data = [const_imtes_combine + label]
    for level in levels:
        bono_file = '%s/workload/bono-%s.xlsx' % (raw_data_dir, level)
        homestead_file = '%s/workload/homestead-%s.xlsx' % (raw_data_dir, level)
        sprout_file = '%s/workload/sprout-%s.xlsx' % (raw_data_dir, level)

        com_data = combine_data(bono_file, homestead_file, sprout_file)
        com_data_label = [data + [transfer_wl(level)] for data in com_data]
        sum_com_data += com_data_label

    write_to_csv('%s/workload.csv' % data_dir, sum_com_data)

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

def match_rule(record, rule):
    find = False
    timestamp = record[0]
    for r in rule:
        if int(timestamp) > int(r[0]) and int(timestamp) < int(r[0]) + int(r[1])*60:
            record += transfer_fl(r[2])
            find = True
            break
    if not find:
        record += transfer_fl(None)
        
    return record


def auto_label_faultload():
    bono_csv = []
    homestead_csv = []
    sprout_csv = []
    node_dir = "./data/fault_load/node"
    fault_dir = "./data/fault_load/fault_log"
    for component in ['bono', 'homestead', 'sprout']:
        data = [record for record in read_xlsx('%s/%s.xlsx' % (node_dir, component))]
        rule = read_log('%s/%s-stress.log' % (fault_dir, component))
        data_label = [match_rule(record[1:], rule) for record in data]

        label_list = ['normal', 'cpu', 'mem', 'io']
        sum_com_data = [const_items[1:] + label_list]
        sum_com_data += data_label

        if component == 'bono':
            bono_csv = sum_com_data
        elif component == 'homestead':
            homestead_csv = sum_com_data
        elif component == 'sprout':
            sprout_csv = sum_com_data

        write_to_csv('%s/faultload-%s.csv' % (node_dir, component), sum_com_data)

    # combine csv
    combine_csv = []
    combine_csv.append(const_imtes_combine + const_fault_label)

    i = 0
    for bono_r, homestead_r, sprout_r in zip(bono_csv, homestead_csv, sprout_csv):
        i += 1
        if 1 == i:
            continue

        label_r = [0] + bono_r[-3:] + homestead_r[-3:] + sprout_r[-3:]
        if 1 not in label_r:
            label_r[0] = 1
        combine_r = bono_r[:-4] + homestead_r[1:-4] + sprout_r[1:-4] + label_r
        combine_csv.append(combine_r)
    write_to_csv('%s/faultload.csv' % (node_dir), combine_csv)


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

def match_sla(record, sla_list):
    find = False
    for sla in sla_list:
        if int(record[0]) > int(sla[0]) and int(record[0]) < int(sla[0]) + 60:
            record += transfer_sl(sla[1])
            find = True
            break
    if not find:
        record += transfer_sl(None)
    return record

def auto_label_sla():
    raw_dir = "./data/sla/node"
    com_data = combine_data('%s/bono.xlsx' % raw_dir, 
        '%s/homestead.xlsx' % raw_dir,
        '%s/sprout.xlsx' % raw_dir)
    sla_list = read_sla("./data/sla/stress_log/sla.log")

    com_data_label = [match_sla(record, sla_list) for record in com_data]
    label = ['sla level', 'successful rate']
    sum_com_data = [const_imtes_combine + label]
    sum_com_data += com_data_label
    write_to_csv('%s/sla-level.csv' % raw_dir, sum_com_data)


def main():
    # for sla
    auto_label_sla()
    # for faultload
    # auto_label_faultload()
    
    
    # try :
    #     auto_label_workload()
    # except:
    #     print('no label workload')
    # try:
    #     auto_label_faultload()
    # except:
    #     print('no label faultload')  
    # try:
    #     auto_label_sla()
    # except:
    #     print('no label sla')
   
if __name__ == '__main__':
    main()
