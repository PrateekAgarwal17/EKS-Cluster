from typing import Optional
import pulumi_aws as aws

def validate_config(
    desired_cpu_node_count: Optional[int],
    min_cpu_node_count: Optional[int],
    max_cpu_node_count: Optional[int],
    desired_gpu_node_count: Optional[int],
    min_gpu_node_count: Optional[int],
    max_gpu_node_count: Optional[int]
    
):
    validate_node_counts(desired_cpu_node_count, min_cpu_node_count, max_cpu_node_count)
    validate_node_counts(desired_gpu_node_count, min_gpu_node_count, max_gpu_node_count)
    

def validate_node_counts(desired: int, min_count: int, max_count: int) -> None:
    if desired < 0 or min_count < 0 or max_count < 0:
        raise ValueError("Node counts must be non-negative integers.")
    if not (min_count <= desired <= max_count):
        raise ValueError(
            "Desired node count must be between min and max counts."
        )