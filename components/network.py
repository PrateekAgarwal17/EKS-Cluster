import pulumi
import pulumi_awsx as awsx


class Network(pulumi.ComponentResource):
    def __init__(self, opts=None):
        """
        Class constructor
        """
        cluster_config = pulumi.Config("cluster")
        network_config = pulumi.Config("network")

        cluster_name = cluster_config.require("name")
        vpc_cidr = network_config.get(
            "vpc_cidr"
        )  # Use get to handle optional values
        public_subnet_cidrs = network_config.get_object("public_subnet_cidrs")
        private_subnet_cidrs = network_config.get_object(
            "private_subnet_cidrs"
        )
        single_nat = network_config.get_bool("single_nat")

        super().__init__("custom:components:Network", cluster_name, None, opts)

        self.cluster_name = cluster_name
        self.vpc_cidr = vpc_cidr if vpc_cidr != "" else "10.0.0.0/16"

        self.public_subnet_cidrs = (
            public_subnet_cidrs
            if public_subnet_cidrs != []
            else [
                "10.0.96.0/19",
                "10.0.128.0/19",
                "10.0.160.0/19",
            ]
        )

        self.private_subnet_cidrs = (
            private_subnet_cidrs
            if private_subnet_cidrs != []
            else [
                "10.0.0.0/19",
                "10.0.32.0/19",
                "10.0.64.0/19",
            ]
        )

        self.single_nat = True if single_nat else False

        self.vpc = self._create_vpc()

    def _create_vpc(self) -> awsx.ec2.Vpc:
        """
        Create our vpc
        """
        # Create VPC
        vpc = awsx.ec2.Vpc(
            f"{self.cluster_name}-vpc",
            cidr_block=self.vpc_cidr,
            number_of_availability_zones=3,
            subnet_specs=[
                awsx.ec2.SubnetSpecArgs(
                    cidr_blocks=self.public_subnet_cidrs,
                    type=awsx.ec2.SubnetType.PUBLIC,
                ),
                awsx.ec2.SubnetSpecArgs(
                    cidr_blocks=self.private_subnet_cidrs,
                    type=awsx.ec2.SubnetType.PRIVATE,
                ),
            ],
            nat_gateways=awsx.ec2.NatGatewayConfigurationArgs(
                strategy=(
                    awsx.ec2.NatGatewayStrategy.SINGLE
                    if self.single_nat
                    else awsx.ec2.NatGatewayStrategy.ONE_PER_AZ
                )
            ),
            opts=pulumi.ResourceOptions(parent=self),
        )

        return vpc