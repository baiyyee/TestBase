- wrk(2)

Guideline：https://blog.csdn.net/ccccsy99/article/details/105958366

```console
[setup]

git clone https://github.com/wg/wrk.git
apt-get -y install gcc
cd wrk
make
cp wrk /usr/local/bin


[backup]
git clone https://gitee.com/am2901/wrk.git


[Server Status]
Get Server Processor: top
Memery Info         : cat /proc/meminfo
Physical CPU Counts : cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l
Physical CPU Cores  : cat /proc/cpuinfo| grep "cpu cores"| uniq
CPU Processor Counts: cat /proc/cpuinfo| grep "processor"| wc -l


[wrk]
wrk -c4 -t4 -d5s --latency "https://cn.bing.com/?FORM=Z9FD1"

[wrk2]
wrk -c4 -t4 -d5s -R 1000 --latency "https://cn.bing.com/?FORM=Z9FD1"

NOTE:
-R parameter is required in wrk2

```

- JMeter

```console

cd ~
mkdir stresstest
cd ~/stresstest
mkdir scripts
mkdir report

sh ~/apache-jmeter-5.4/bin/jmeter.sh -n -t scripts/stress.jmx -l report/result.log -e -o report

```


- LoadRunner

```console

#include "web_api.h"

Action()
{
	
	int HttpRetCode;
	                                     
	lr_start_transaction("send_request");

	web_custom_request("send_request", 
        "URL=https://cn.bing.com/?FORM=Z9FD1",
		"Method=GET",
		LAST);

        HttpRetCode = web_get_int_property(HTTP_INFO_RETURN_CODE);

	if(HttpRetCode == 200){
        lr_end_transaction("send_request", LR_PASS);
	}
	
	return 0;
}

```