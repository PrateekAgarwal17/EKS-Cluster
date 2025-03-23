import pulumi
from components.iam import IAM
from components.network import Network
from components.eks_cluster import EksCluster
from confighandler.confighandler import EKSConfigHandler
from confValidation.validation import validate_config

config_handler = EKSConfigHandler()
cluster_vars = config_handler.handle_cluster_config()

validate_config(
    cluster_vars["desired_cpu_node_count"],
    cluster_vars["min_cpu_node_count"],
    cluster_vars["max_cpu_node_count"],
    cluster_vars["desired_gpu_node_count"],
    cluster_vars["min_gpu_node_count"],
    cluster_vars["max_gpu_node_count"],
)

network = Network()
iam = IAM(cluster_vars["cluster_name"])
eks_cluster = EksCluster(
    cluster_vars["cluster_name"],
    cluster_vars["cluster_version"],
    cluster_vars["cpu_instance_type"],
    cluster_vars["desired_cpu_node_count"],
    cluster_vars["min_cpu_node_count"],
    cluster_vars["max_cpu_node_count"],
    cluster_vars["cpu_node_disk_size"],
    cluster_vars["gpu_operator_version"],
    cluster_vars["gpu_instance_type"],
    cluster_vars["desired_gpu_node_count"],
    cluster_vars["min_gpu_node_count"],
    cluster_vars["max_gpu_node_count"],
    cluster_vars["gpu_node_disk_size"],
    vpc_id=network.vpc.vpc_id,
    subnet_ids=network.vpc.private_subnet_ids,
    node_role=iam.node_role,
    node_instance_profile=iam.node_instance_profile,
    opts=pulumi.ResourceOptions(depends_on=[network, iam]),
)