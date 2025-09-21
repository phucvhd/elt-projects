import json
import logging
import os
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from elt.config.config import Config

logger = logging.getLogger(__name__)

class AwsClient:
    def __init__(self, config: Config):
        self.AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
        self.AWS_DEFAULT_REGION = config.AWS_DEFAULT_REGION
        self.AWS_BUCKET_NAME = config.AWS_BUCKET_NAME
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region_name=self.AWS_DEFAULT_REGION
        )
        self.temp_files = []

    def get_s3_buckets(self) -> dict | None:
        try:
            response = self.s3_client.list_buckets()
            logger.info("S3 Connection successful")
            return response
        except ClientError as e:
            logger.error("Error connecting to S3: ", e)
            raise e

    def upload_raw_data(self, raw_data: dict) -> bool:
        temp_filename = self.create_temp_json_file(raw_data)
        try:
            s3_key = temp_filename

            self.s3_client.upload_file(
                temp_filename,
                self.AWS_BUCKET_NAME,
                s3_key,
                ExtraArgs={
                    'ContentType': 'application/json',
                    'Metadata': {
                        'created_at': datetime.now().isoformat(),
                        'data_type': 'json_dictionary',
                        'pretty_formatted': 'true'
                    }
                }
            )

            logger.info(f"Uploaded dict as JSON: s3://{self.AWS_BUCKET_NAME}/{s3_key}")

            self.cleanup_temp_file(temp_filename)
            return True
        except Exception as e:
            logger.error("Error uploading dict as file: ", e)
            try:
                self.cleanup_temp_file(temp_filename)
            except:
                pass
            return False

    def create_temp_json_file(self, data_dict: dict, pretty_print=True, prefix="temp", suffix=".json") -> str | None:
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            temp_filename = f"{prefix}_{timestamp}{suffix}"

            with open(temp_filename, 'w', encoding='utf-8') as f:
                if pretty_print:
                    json.dump(data_dict, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(data_dict, f, ensure_ascii=False)

            self.temp_files.append(temp_filename)

            logger.info(f"Created temporary file: {temp_filename}")
            return temp_filename
        except Exception as e:
            logger.error("Error creating temp file: ", e)
            return None

    def cleanup_temp_file(self, filename: str) -> bool:
        try:
            if os.path.exists(filename):
                os.remove(filename)
                logger.info(f"Cleaned up: {filename}")

                if filename in self.temp_files:
                    self.temp_files.remove(filename)

                return True
            else:
                logger.info(f"File not found for cleanup: {filename}")
                return False
        except Exception as e:
            logger.error("Error cleaning up {filename}: ", e)
            return False

    def get_json_as_dict(self, s3_key: str) -> dict | None:
        try:
            logger.info(f"Getting object from s3://{self.AWS_BUCKET_NAME}/{s3_key}")

            response = self.s3_client.get_object(Bucket=self.AWS_BUCKET_NAME, Key=s3_key)

            json_content = response['Body'].read().decode('utf-8')

            data_dict = json.loads(json_content)

            return data_dict
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error(f"JSON file not found: s3://{self.AWS_BUCKET_NAME}/{s3_key}")
            else:
                logger.error("AWS error: ", e)
            raise e
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON format: ", e)
            raise e
        except Exception as e:
            logger.error("Unexpected error: ", e)
            raise e

    def get_object_keys_with_pattern(self, prefix="", pattern="") -> list[str]:
        try:
            logger.info(f"Searching for objects containing: '{pattern}'")
            if prefix:
                logger.info(f"In prefix: {prefix}")

            matching_objects = []
            continuation_token = None

            while True:
                params = {'Bucket': self.AWS_BUCKET_NAME, 'MaxKeys': 1000}
                if prefix:
                    params['Prefix'] = prefix
                if continuation_token:
                    params['ContinuationToken'] = continuation_token

                response = self.s3_client.list_objects_v2(**params)

                if 'Contents' not in response:
                    break

                for obj in response['Contents']:
                    key = obj['Key']

                    if pattern in key:
                        matching_objects.append(obj)

                if not response.get('IsTruncated', False):
                    break
                continuation_token = response.get('NextContinuationToken')

            results = [obj["Key"] for obj in matching_objects]

            logger.info(f"Found {len(results)} objects with today's date pattern")
            return results

        except Exception as e:
            logger.error("Error searching for today's objects: ", e)
            return []
