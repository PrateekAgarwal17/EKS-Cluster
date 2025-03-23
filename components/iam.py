import json
import pulumi
import pulumi_aws as aws
from typing import Tuple


class IAM(pulumi.ComponentResource):
    """
    Managed Policy ARN node role
    """

    managed_policy_arns_node = [
        "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
        "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
        "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
        "arn:aws:iam::aws:policy/AmazonSSMManagedEC2InstanceDefaultPolicy",
    ]

    node_assume_role_policy = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AllowAssumeRole",
                    "Effect": "Allow",
                    "Principal": {"Service": "ec2.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
    )

    def __init__(self, cluster_name: pulumi.Input[str], opts=None):
        self.cluster_name = cluster_name
        self.node_role, self.node_instance_profile = self._create_node_role()

        super().__init__(
            "custom:components:IAM", self.cluster_name, None, opts
        )

    def _create_node_role(
        self,
    ) -> Tuple[aws.iam.Role, aws.iam.InstanceProfile]:
        role = aws.iam.Role(
            f"{self.cluster_name}-node-role",
            assume_role_policy=self.node_assume_role_policy,
            managed_policy_arns=self.managed_policy_arns_node,
        )

        instance_profile = aws.iam.InstanceProfile(
            f"{self.cluster_name}-node-profile", role=role.name
        )
        return (role, instance_profile)