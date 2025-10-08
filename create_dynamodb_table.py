#!/usr/bin/env python3
"""
Create DynamoDB table for WMU Students
Run this once to set up the table
"""

import boto3
from botocore.exceptions import ClientError

# DynamoDB configuration
TABLE_NAME = 'wmu-students'
REGION = 'us-east-1'

def create_table():
    """Create DynamoDB table"""
    dynamodb = boto3.resource('dynamodb', region_name=REGION)

    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'idn',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'idn',
                    'AttributeType': 'N'  # Number
                },
                {
                    'AttributeName': 'nama',
                    'AttributeType': 'S'  # String
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'nama-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'nama',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }
                    # No ProvisionedThroughput for PAY_PER_REQUEST billing mode
                }
            ],
            BillingMode='PAY_PER_REQUEST',  # On-demand pricing (no provisioned capacity)
            Tags=[
                {
                    'Key': 'Project',
                    'Value': 'WMU-Students-Update'
                },
                {
                    'Key': 'Environment',
                    'Value': 'Production'
                }
            ]
        )

        # Wait for table to be created
        print(f"Creating table '{TABLE_NAME}'...")
        table.wait_until_exists()

        print(f"\n[SUCCESS] Table '{TABLE_NAME}' created successfully!")
        print(f"\nTable ARN: {table.table_arn}")
        print(f"Table status: {table.table_status}")
        print(f"Item count: {table.item_count}")

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"\n[WARNING] Table '{TABLE_NAME}' already exists!")

            # Get table info
            dynamodb_client = boto3.client('dynamodb', region_name=REGION)
            response = dynamodb_client.describe_table(TableName=TABLE_NAME)
            print(f"Table status: {response['Table']['TableStatus']}")
            print(f"Item count: {response['Table']['ItemCount']}")
        else:
            print(f"\n[ERROR] Error creating table: {e}")
            raise

if __name__ == '__main__':
    print("="*60)
    print("DynamoDB Table Creation")
    print("="*60)
    print(f"Table Name: {TABLE_NAME}")
    print(f"Region: {REGION}")
    print(f"Billing: Pay-per-request (on-demand)")
    print("="*60)

    confirm = input("\nCreate table? (yes/no): ")

    if confirm.lower() == 'yes':
        create_table()
    else:
        print("Cancelled.")
