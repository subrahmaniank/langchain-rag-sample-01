import logging
import os

import boto3
from dotenv import load_dotenv

load_dotenv(override=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AWSUtil:

    def __init__(self):
        _aws_secret_key = os.environ.get("AWS_SECRET_KEY")
        _aws_access_key = os.environ.get("AWS_ACCESS_KEY")
        _aws_region_id = os.environ.get("AWS_REGION_ID")
        _aws_role_arn = os.environ.get("AWS_ROLE_ARN")

        self.session = boto3.Session(
            aws_access_key_id=_aws_access_key,
            aws_secret_access_key=_aws_secret_key,
            region_name=_aws_region_id,
        )

        sts_client = self.session.client("sts")
        assume_role_response = sts_client.assume_role(
            RoleArn=_aws_role_arn, RoleSessionName="AWSSampleSession"
        )

        credentials = assume_role_response["Credentials"]

        self.aws_access_key_id = credentials["AccessKeyId"]
        self.aws_secret_access_key = credentials["SecretAccessKey"]
        self.aws_session_token = credentials["SessionToken"]
        self.region_name = _aws_region_id

    def get_client(self, service_name):

        logger.info("Getting client for service: %s", service_name)

        if self.aws_session_token is None:
            raise ValueError("AWS_SESSION_TOKEN is not set")

        return boto3.client(
            service_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
            region_name=self.region_name,
        )
