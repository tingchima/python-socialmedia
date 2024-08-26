import boto3
from botocore.exceptions import ClientError
from config.django.base import AWS_DYNAMODB_LOCAL


def run():
    """Migrate local dynamodb."""

    dynamodb = boto3.resource(
        service_name="dynamodb",
        endpoint_url=AWS_DYNAMODB_LOCAL,
    )

    message_table_name = "messages"
    # https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html

    try:
        table = dynamodb.create_table(
            TableName=message_table_name,
            KeySchema=[
                {"AttributeName": "room_id", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "created_timestamp", "KeyType": "N"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "room_id", "AttributeType": "N"},
                {"AttributeName": "created_timestamp", "AttributeType": "N"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10,
            },
        )

        table.wait_until_exists()
    except ClientError as err:
        code = err.response["Error"]["Code"]
        message = err.response["Error"]["Message"]
        print(f"cleint_error: code={code} message={message}")
