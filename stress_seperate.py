def main():
    fault_log_dir = "./data/fault_load/fault_log"
    stress_file = open(fault_log_dir+"/stress.log", "r")
    bono = open(fault_log_dir+"/bono-stress.log", "a")
    homestead = open(fault_log_dir+"/homestead-stress.log", "a")
    sprout = open(fault_log_dir+"/sprout-stress.log", "a")
    line = stress_file.readline()
    while line:
        componet = line.split(", ")
        if componet[0] == "192.168.1.23":
            bono.write(line)
        if componet[0] == "192.168.1.29":
            homestead.write(line)
        if componet[0] == "192.168.1.32":
            sprout.write(line)
        line = stress_file.readline()
    stress_file.close()
    bono.close()
    homestead.close()
    sprout.close()


if __name__ == '__main__':
    main()