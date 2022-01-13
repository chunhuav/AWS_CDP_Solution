from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_elasticsearch as es,
    aws_ec2 as ec2
)
from aws_cdk.aws_elasticsearch import Domain
import aws_cdk as cdk


class CdpSolution2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "CDP_VPC",
            nat_gateways=0,
            subnet_configuration=[ec2.SubnetConfiguration(name="public",subnet_type=ec2.SubnetType.PUBLIC)]
            )

        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        unmomi_security_group = ec2.SecurityGroup(self, "SecurityGroup",
            vpc=vpc,
            description="cdp unomi security group",
            allow_all_outbound=True
        )
        unmomi_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")
        unmomi_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8181), "allow unomi access port 8181")
        unmomi_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(9443), "allow unomi access port 9443")
        # amzn_linux = ec2.MachineImage.latest_amazon_linux(
        #             generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
        #             edition=ec2.AmazonLinuxEdition.STANDARD,
        #             virtualization=ec2.AmazonLinuxVirt.HVM,
        #             storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        #             )

        # "ap-northeast-1":"ami-088da9557aae42f39"
        machine_image=ec2.GenericLinuxImage({
        "us-east-1": "ami-04505e74c0741db8d",
        "ap-northeast-1":"ami-088da9557aae42f39"
        })

        # userdata ='''
        # #!/bin/bash
        # sudo apt-get update -y
        # sudo apt-get upgrade -y
        # sudo apt install openjdk-8-jdk -y
        # wget https://dlcdn.apache.org/unomi/1.5.7/unomi-1.5.7-bin.tar.gz
        # tar -xzvf unomi-1.5.7-bin.tar.gz

        # '''

        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("m5.xlarge"),
            machine_image=machine_image,
            vpc = vpc,
            role = role,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            # user_data=ec2.UserData.custom(userdata),
            security_group=unmomi_security_group,
            keyName='ee-default-keypair'
            )

        this_stack = cdk.Stack.of(self)
        domain_arn = f"arn:aws:es:{this_stack.region}:{this_stack.account}:domain/cdp-sol-domain-13jxxas5c8nfj/*"

        access_policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            principals=[
                iam.AnyPrincipal()
            ],
            actions=["es:*"],
            resources=[domain_arn]
        )



        cdp_domain = es.Domain(self, "Domain",
            version=es.ElasticsearchVersion.V7_4,
            ebs=es.EbsOptions(volume_size=100),
            node_to_node_encryption=True,
            enforce_https=True,
            encryption_at_rest=es.EncryptionAtRestOptions(enabled=True),
            access_policies=[access_policy_statement],
            fine_grained_access_control=es.AdvancedSecurityOptions(
                master_user_name="master-user"
            )
        )

        master_user_password = cdp_domain.master_user_password
        # cdk.CfnOutput(self, "OpenSearch-master-user-password", value=master_user_password)

  