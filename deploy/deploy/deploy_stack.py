import os

from aws_cdk import core
import aws_cdk.aws_certificatemanager as certificatemanager
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_s3_deployment as s3deploy
import aws_cdk.aws_cloudfront as cloudfront


class DeployStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        domain = "gazwald.com"
        sub_domain = "meltest." + domain

        certificate = certificatemanager.Certificate(self, "Certificate",
            domain_name=domain,
            subject_alternative_names=["*." + domain],
            validation_method=certificatemanager.ValidationMethod.DNS
        )

        s3_bucket_source = s3.Bucket(self, "Bucket")

        assets_directory = os.path.join(os.getcwd(), '..', 'src')
        s3deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3deploy.Source.asset(assets_directory)],
            destination_bucket=s3_bucket_source,
        )

        distribution = cloudfront.CloudFrontWebDistribution(self, "AnAmazingWebsiteProbably",
            origin_configs=[cloudfront.SourceConfiguration(
                s3_origin_source={"s3_bucket_source": s3_bucket_source},
                behaviors=[cloudfront.Behavior(is_default_behavior=True)]
            )],
            viewer_certificate=cloudfront.ViewerCertificate.from_acm_certificate(certificate,
                aliases=[sub_domain],
                security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1,
                ssl_method=cloudfront.SSLMethod.SNI
            )
        )
