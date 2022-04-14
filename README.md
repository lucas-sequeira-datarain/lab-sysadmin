# lab-sysadmin
**System Admin Laboratory**

A Laboratory to launch a application system using EC2 instances within a VPC. To do so, we have an administrator role, and a commom user role to manage the AWS environment. 

---

## AWS Architecture

![AWS Architecture](/assets/architecture/v2.png "AWS Architecture")

---

## Requisitions

All requisitions are listed as follows, and came from the [Laboratory material](/assets/material/).

### 1. MFA Policy

1. User must be able to manage their own MFA device;
2. Any IAM user operation must be blocked if its MFA device is not configured.

### 2. IAM User

1. The created user must only have the previously mentioned MFA device management permission;
2. He alone should not have any other permissions attached to him or his group.
3. Create two users, one administrator and one common.

### 3. IAM Role

1. Create two roles: one to be assumed by your SSO user and the IAM User administrator, and another to be assumed by the common IAM User;
2. The role must contain the necessary permissions for the user to operate;
3. Role operating time should be 4 hours.

### 4. Network Topology - Create VPC

1. Delete the default VPC;
2. Create a VPC in the N. Virginia region (us-east-1);
3. The VPC must have a CIDR block of 10.0.0.0/16;
4. Enable DNS hostnames and DNS resolution.

### 5. Network Topology - Create 6 Subnets

1. Configure 3 public subnets (10.0.{10,11,12}.0/24) balanced in us-east-1{a,b,c} zones;
2. Configure 3 private subnets (10.0.{0,1,2}.0/24) balanced in us-east-1{a,b,c} zones.

### 6. Security rules - Create NACL for the public and private Subnets

1. The public subnet must have a NACL allowing external inbound;
2. The private subnet cannot have external inbound;
3. As regras devem apenas permitir o necessário.

### 7. Security rules - Create Security Groups

1. Configure a security group for the bastion host;
2. Configure a security group for the external Load Balancer;
3. Configure two security groups for Application Servers: one for the application itself, another for SSH access via the Bastion Host;
4. Avoid using IP source, but ID of other security groups as source;
5. Rules should allow only what is necessary.

### 8. Bastion Host

1. Configure an EC2 as a Bastion Host;
2. It must be in the us-east-1c zone;
3. From there, the internal network must be accessed;
4. A CloudWatch alarm with auto-recovery of the instance must be configured using the StatusCheckFailed_System metric;
5. Force IMDSv2;
6. Create and associate an instance profile to list the instances.

### 9. Application Server

1. Two application servers must be configured;
2. They must be balanced in the us-east-1{a,b} zones;
3. A CloudWatch alarm with auto-recovery of the instance must be configured using the StatusCheckFailed_System metric;
4. Force IMDSv2;
5. User data must expose the domain “lab-sysadmin.belinelo.com.br” with the endpoint “/“ returning the header “X-Private-IP” with the IP of the instance;
6. In the same domain, the “/metrics” endpoint should serve a file with:
    - Timestamp;
    - CPU, RAM, SWAP and disk usage;
    - Number of tasks currently running.
7. The “/metrics” file should be updated (incremented) every 5 minutes with the new metrics;
8. Configure the default domain to only serve the “/health” endpoint.

### 10. Load Balancer

1. Create a Load Balancer for the two application servers;
2. Health check configured for the “/health” endpoint.

---

## Development

For the development, we've managed to code and design a [SAML template](/assets/templates/template.yaml) for CloudFormation to launch a full stack, the is required some small user actions. a small snippet of the code is written down:

```yaml
# Run (on /assets/templates/):
#    sam build
#    sam deploy --guided --profile lab-sys.admin_mfa --capabilities CAPABILITY_NAMED_IAM

AWSTemplateFormatVersion: 2010-09-09

Parameters:
  AppVPCCidr:
    Type: String
    Default: 10.0.0.0/16
  AppStage:
    Type: String
    Default: dev
(...)
```