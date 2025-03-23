from typing import List
import pulumi
import pulumi_eks as eks
import pulumi_aws as aws
from pulumi_kubernetes.helm.v3 import Release
import pulumi_kubernetes as k8s


class EksCluster(pulumi.ComponentResource):
    """
    EKS Cluster creation class
    """

    vpc_id: pulumi.Input[str]

    subnet_ids: List[pulumi.Input[str]]

    k8s_provider: k8s.Provider

    def __init__(
        self,
        cluster_name: pulumi.Input[str],
        cluster_version: pulumi.Input[str],
        cpu_instance_type: pulumi.Input[str],
        desired_cpu_node_count: pulumi.Input[int],
        min_cpu_node_count: pulumi.Input[int],
        max_cpu_node_count: pulumi.Input[int],
        cpu_node_disk_size: pulumi.Input[int],
        gpu_operator_version: pulumi.Input[str],
        gpu_instance_type: pulumi.Input[str],
        desired_gpu_node_count: pulumi.Input[int],
        min_gpu_node_count: pulumi.Input[int],
        max_gpu_node_count: pulumi.Input[int],
        gpu_node_disk_size: pulumi.Input[int],
        vpc_id: pulumi.Input[str],
        subnet_ids: List[pulumi.Input[str]],
        node_role: pulumi.Input[aws.iam.Role],
        node_instance_profile: pulumi.Input[aws.iam.InstanceProfile],
        opts=None,
    ):
        self.cluster_name = cluster_name
        self.cluster_version = cluster_version

        self.node_role = node_role
        self.node_instance_profile = node_instance_profile

        self.vpc_id = vpc_id
        self.subnet_ids = subnet_ids

        self.cpu_instance_type = (
            cpu_instance_type if cpu_instance_type != "" else "t3.medium"
        )
        self.desired_cpu_node_count = desired_cpu_node_count
        self.min_cpu_node_count = min_cpu_node_count
        self.max_cpu_node_count = max_cpu_node_count
        self.cpu_node_disk_size = cpu_node_disk_size
        self.gpu_operator_version = gpu_operator_version

        self.gpu_instance_type = (
            gpu_instance_type if gpu_instance_type != "" else "g4dn.xlarge"
        )

        self.desired_gpu_node_count = desired_gpu_node_count
        self.min_gpu_node_count = min_gpu_node_count
        self.max_gpu_node_count = max_gpu_node_count
        self.gpu_node_disk_size = gpu_node_disk_size

        super().__init__(
            "custom:components:EksCluster", cluster_name, {}, opts
        )

        self.cluster = self._create_eks_cluster()
        self.k8s_provider = self._create_kubernetes_provider()
        self._create_managed_node_groups()

    def _create_eks_cluster(self):
        kms_key = aws.kms.Key(
            f"{self.cluster_name}-key",
            enable_key_rotation=True,
            rotation_period_in_days=90,
        )

        return eks.Cluster(
            self.cluster_name,
            vpc_id=self.vpc_id,
            instance_roles=[self.node_role],
            subnet_ids=self.subnet_ids,
            version=self.cluster_version,
            endpoint_public_access=True,
            endpoint_private_access=True,
            encryption_config_key_arn=kms_key.arn,
            skip_default_node_group=True,
            authentication_mode=eks.AuthenticationMode.API_AND_CONFIG_MAP,
            opts=pulumi.ResourceOptions(parent=self),
        )

    def _create_managed_node_groups(self):
        self.cpu_node_group = eks.ManagedNodeGroup(
            f"{self.cluster_name}-cpu-node-group",
            cluster=self.cluster.core,
            instance_types=[self.cpu_instance_type],
            node_role=self.node_role,
            scaling_config=aws.eks.NodeGroupScalingConfigArgs(
                desired_size=self.desired_cpu_node_count,
                min_size=self.min_cpu_node_count,
                max_size=self.max_cpu_node_count,
            ),
            subnet_ids=self.subnet_ids,
            ami_type="AL2_x86_64",
            disk_size=self.cpu_node_disk_size,
            opts=pulumi.ResourceOptions(parent=self),
        )

    def _create_kubernetes_provider(self) -> k8s.Provider:
        """
        Creating the kubernetes provider
        """
        return k8s.Provider(
            f"{self.cluster_name}-k8s-provider",
            kubeconfig=self.cluster.kubeconfig,
            opts=pulumi.ResourceOptions(parent=self.cluster),
        )