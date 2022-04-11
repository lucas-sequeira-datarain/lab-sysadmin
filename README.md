# lab-sysadmin
System Admin Laboratory

## 1. Política de MFA

Forçar o uso do MFA para o IAM User

1. O usuário deve ser capaz de gerenciar seu próprio MFA device;
2. Deve ser bloqueada qualquer operação do IAM user se seu MFA device
não estiver configurado.

Políticas:
 - [MFAPolicy](policies/MFAPolicy.json)

Assume Role:
 - [AdminRole](https://signin.aws.amazon.com/switchrole?roleName=AdminRole&account=685463979595)
 - [ComumRole](https://signin.aws.amazon.com/switchrole?roleName=ComumRole&account=685463979595)


Recursos:
 - [VPC + BastionHost](https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c02/learn/lecture/13528534#overview)
 - [AWS: Allows MFA-authenticated IAM users to manage their own MFA device on the My Security Credentials page](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_my-sec-creds-self-manage-mfa-only.html)
 - [Modifying a role (console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-modify_max-session-duration)
 - [Assigning users or groups to an existing role](https://docs.informatica.com/data-integration/powerexchange-adapters-for-informatica/10-5/powerexchange-for-amazon-s3-user-guide/powerexchange-for-amazon-s3-configuration-overview/assumerole/assumerole-policy.html)
 - [Amazon VPC policy examples](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-policy-examples.html)
 - [NACL Rules](https://stackoverflow.com/questions/62413853/how-to-create-nacl-for-private-subnets)
 - [EC2 Policies](https://docs.amazonaws.cn/en_us/AWSEC2/latest/UserGuide/iam-policies-ec2-console.html)
 - [Add recover actions to Amazon CloudWatch alarms](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/UsingAlarmActions.html#AddingRecoverActions)
 - [Sample App Python](https://docs.aws.amazon.com/pt_br/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)
 - [Create Instance Profile](https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-iam-instance-profile.html)