# setup

git clone https://github.com/wg/wrk.git
apt-get -y install gcc
cd wrk
make
cp wrk /usr/local/bin


# backup
git clone https://gitee.com/am2901/wrk.git


# Server Status
# Get Server Processor: top
# Memery Info         : cat /proc/meminfo
# Physical CPU Counts : cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l
# Physical CPU Cores  : cat /proc/cpuinfo| grep "cpu cores"| uniq
# CPU Processor Counts: cat /proc/cpuinfo| grep "processor"| wc -l


# wrk
wrk -c4 -t4 -d5s --latency "https://cn.bing.com/?FORM=Z9FD1"

# wrk2
wrk -c4 -t4 -d5s -R 1000 --latency "https://cn.bing.com/?FORM=Z9FD1"

# NOTE:
# -R parameter is required in wrk2