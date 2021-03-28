# Wild Port Scanner

This is a Network Port Scanner written in Python3, focussed on simplicity rather than advanced features.
It has been developed in incremental iterations, where main features are:

* Scans TCP ports.
* Multithreading. Level of concurrency is set by command line argument.
* Stealth mode to prevent firewall's scanning pattern detection. 
* http service detection.
* Output can by downloaded as json file for easy use on external tools.
* A Dockerized version is provided.
* No other Python libraries are required other than the standard ones.


## Installation and Configuration
Get the code:
```
$ git clone https://github.com/gbernat/simple_port_scanner.git
```
Go to the Iteration to run, and execute:
```
$ cd simple_port_scanner/Iteration_4
$ python3 port-scanner.py www.targeturl.com -t 20 -o
```
No additional libs are needed.

Global configuration parameters are in **port_scanner/conf.py**
Different configurations can be made depending on the Iteration you are in.  
Common settings are:
* Range of ports to scan.
* Custom socket connection timeout.

## Usage
Example of the full commandline arguments version:
```
$ port-scanner.py -h
usage: port-scanner.py [-h] [-o] [-t THREADS] [-f] target

Port scanner

positional arguments:
  target                Target hostname to scan

optional arguments:
  -h, --help            show this help message and exit
  -o, --output-json     Creates a json file with scanning results in current
                        path. Default: Disabled
  -t THREADS, --threads THREADS
                        Set max threads for concurrent execution. Default: 5
  -f, --disable-stealth
                        Disable stealth feature. No random ports order and
                        scanning intervalls changes will be performed to avoid
                        firewall scanning pattern detection. Default: Enabled
```

## Iterations description
### Iteration 1
This is the simplest version. Performs port scans in sequential order on one thread.  
The output shows whether a port is open or not responding to the connection attempt.

### Iteration 2
Adds multithreading capability to increase concurrency in the execution of scan ports.  
The concurrency level is set through command line argument, with 5 beeing the default max number of threads.

### Iteration 3
Implement mechanisms to prevent firewall from detecting the scan. Firewalls can detect scanning as attack behavior when recieving sequencial and predictive port connections.
Therefore, this Iteration adds a feature to avoid scanning consecutive port numbers and inyects a random delay between connections.
Both behaviors can be changed in **conf.py**.

### Iteration 4
In addition to the above characteristics, it tries to determine if the service binded to an open port is an http server.  
To keep the number of connections to the target server as low as possible, this feature is not a full fingerprint of the webserver.

### Iteration 5
Wraps the previous Iteration into a Docker image.


## Outputs
### Interactive output
```
Iteration_4 guido$ python3 port-scanner.py ec2-54-...-107.sa-east-1.compute.amazonaws.com -t 30 -o
```
```
\\\ WILD PORT \\\\
 //// SCANNER ////

I'm going to do:
 Target: ec2-54-...-107.sa-east-1.compute.amazonaws.com
 Range ports: (1, 1024)
 Max concurrent threads: 30
 Firewall detection avoidance enabled: True

Launching scan...

Results:
1024 ports were scanned

Port 80: open  (http)
Port 22: open

2 ports are open

File results_ec2-54-...-107.sa-east-1.compute.amazonaws.com_20215928_1359.json has been created with scan results

Done!
Time consumed: 1m 53s

```

### Json output file 
```json
[
    {
        "target": "ec2-54-...-107.sa-east-1.compute.amazonaws.com",
        "port": 3,
        "status": "closed"
    },
    {
        "target": "ec2-54-...-107.sa-east-1.compute.amazonaws.com",
        "port": 5,
        "status": "closed"
    },
...
    {
        "target": "ec2-54-...-107.sa-east-1.compute.amazonaws.com",
        "port": 78,
        "status": "closed"
    },
    {
        "target": "ec2-54-...-107.sa-east-1.compute.amazonaws.com",
        "port": 80,
        "status": "open",
        "web_server": true
    },
...
    {
        "target": "ec2-54-...-107.sa-east-1.compute.amazonaws.com",
        "port": 19,
        "status": "closed"
    },
    {
        "target": "ec2-54-...-107.sa-east-1.compute.amazonaws.com",
        "port": 22,
        "status": "open",
        "web_server": false
    },
...
]
```

## Limitations
* Delay step resolution cannot be configurable. (0.1 sec) 
* Only one target per scan



