
## Assignmnet 1 : Cluster Benchmarking using EC2 Virtual Machines and Elastic Load Balancer (ELB)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

#### Inctance Information:


| #  | Type       | Name       | IPv4 Public IP | Description |
| :- | :--------- | :--------- | :------------- | :---------- |
| 1. | `M4-large` | M4-large-1 | 54.164.0.164.  | |
| 2. | 'M4-large' | M4-large-2 | 44.211.161.152 | |
| 3. | 'M4-large' | M4-large-3 | 172.31.81.143  | |
| 4. | 'M4-large' | M4-large-4 | 18.233.225.20  | |
| 5. | 'M4-large' | M4-large-5 | 3.94.79.209    | |
| 6. | 'T2-large' | T2-large-1 | 54.160.231.184 | |
| 7. | 'T2-large' | T2-large-2 | 3.87.80.104    | |
| 8. | 'T2-large' | T2-large-3 | 184.73.93.102  | |
| 9. | 'T2-large' | T2-large-4 | 3.95.231.194   | |
|10. | 'T2-large' | T2-large-5 | ---            | |


#### SSH Access
  To access the VMs:

  - Download `labsusers.pem` (Certificate file) and change your directory to that downlowded file.
  
  - Change the permission of the file.
  ```console
  $ chmod 400 labsuser.pem
  ```
  
  - To access into each VM run the below command based on especific VM IPv4:
  ```console
  $ ssh -i labsusers.pem ubuntu@<public-ip>
  ```

#### Setup Instances

To install the flask webserver for each VM, please follow the below instruction.

```console
$ sudo apt update
$ mkdir flask_application && cd flask_application
$ sudo apt install python3-pip -y
$ sudo apt install python3-flask -y

$ echo "from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return 'VM name: <VM_name>'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)" > my_app.py

          $ export FLASK_APP=my_app.py
$ nohup sudo python3 my_app.py &
```
##### Setup Outcome
![pic 1](Setup_pics/1.png)
![pic 2](Setup_pics/2.png)
![pic 3](Setup_pics/3.png)
![pic 4](Setup_pics/4.png)
![pic 5](Setup_pics/5.png)
![pic 6](Setup_pics/6.png)
![pic 7](Setup_pics/7.png)
![pic 8](Setup_pics/8.png)
![pic 9](Setup_pics/9.png)