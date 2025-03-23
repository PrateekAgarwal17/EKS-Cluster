import pulumi


class EKSConfigHandler:
    def __init__(self):
        self.cluster_config = pulumi.Config("cluster")

    def handle_cluster_config(self):
        cluster_vars = {
            "cluster_name": self.cluster_config.require("name"),
            "cluster_version": self.cluster_config.require("version"),
            "cpu_instance_type": self.cluster_config.require(
                "cpu_instance_type"
            ),
            "desired_cpu_node_count": self.cluster_config.require_int(
                "desired_cpu_node_count"
            ),
            "min_cpu_node_count": self.cluster_config.require_int(
                "min_cpu_node_count"
            ),
            "max_cpu_node_count": self.cluster_config.require_int(
                "max_cpu_node_count"
            ),
            "cpu_node_disk_size": self.cluster_config.require_int(
                "cpu_node_disk_size"
            ),
            "gpu_operator_version": self.cluster_config.require(
                "gpu_operator_version"
            ),
            "gpu_instance_type": self.cluster_config.require(
                "gpu_instance_type"
            ),
            "desired_gpu_node_count": self.cluster_config.require_int(
                "desired_gpu_node_count"
            ),
            "min_gpu_node_count": self.cluster_config.require_int(
                "min_gpu_node_count"
            ),
            "max_gpu_node_count": self.cluster_config.require_int(
                "max_gpu_node_count"
            ),
            "gpu_node_disk_size": self.cluster_config.require_int(
                "gpu_node_disk_size"
            ),
        }
        return cluster_vars