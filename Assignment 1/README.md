
## Assignmnet 1

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
  ```bash
  $ chmod 400 labsuser.pem
  ```
  
  - To access into each VM run the below command based on especific VM IPv4:
  ```bash
  $ ssh -i labsusers.pem ubuntu@<public-ip>
  ```

