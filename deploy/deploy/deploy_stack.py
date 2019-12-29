import os

from aws_cdk import core
import aws_cdk.aws_certificatemanager as certificatemanager
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_s3_deployment as s3deploy
import aws_cdk.aws_cloudfront as cloudfront


class DeployStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        domain = os.getenv('DOMAIN', 'gazwald.com')
        sub_domain = "meltest2." + domain

        certificate_id = 'c1636661-e3bb-497f-b057-8269a50796c8'
        arn = 'arn:aws:acm:us-east-1:{account}:certificate/{certificate_id}'.format(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                                                                    certificate_id=certificate_id)
        certificate = certificatemanager.Certificate.from_certificate_arn(self, "Certificate", arn)

        s3_bucket_source = s3.Bucket(self, "Bucket", removal_policy=core.RemovalPolicy.DESTROY)

        assets_directory = os.path.join(os.getcwd(), '..', 'src')
        s3deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3deploy.Source.asset(assets_directory)],
            destination_bucket=s3_bucket_source,
        )

        s3_origin_config = cloudfront.S3OriginConfig(s3_bucket_source=s3_bucket_source,
                                                     origin_access_identity=cloudfront.OriginAccessIdentity(self, "OAI"))

        distribution = cloudfront.CloudFrontWebDistribution(self, "AnAmazingWebsiteProbably",
            origin_configs=[cloudfront.SourceConfiguration(
                s3_origin_source=s3_origin_config,
                behaviors=[cloudfront.Behavior(is_default_behavior=True)]
            )],
            viewer_certificate=cloudfront.ViewerCertificate.from_acm_certificate(certificate,
                aliases=[sub_domain],
                security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1,
                ssl_method=cloudfront.SSLMethod.SNI
            )
        )
