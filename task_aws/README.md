## Study with AWS

The following program:
- creates buckets for input, output and lambda layer
- creates lambda with additional lib
- set trigger and schedule for lambda 
  (it turns on when something is put in input bucket and
  applies functions to it)
  

How to deploy everything:
- install terraform
- connect to AWS account
- `chmod +x deploy.sh`
- `./deploy.sh`
