from datetime import datetime

import pytest

from elt.client.aws_client import AwsClient
from elt.config.config import Config

config = Config()
config.AWS_BUCKET_NAME = "pv-demo-bucket"
aws_client = AwsClient(config)

def test_get_s3_buckets():
    response = aws_client.get_s3_buckets()
    bucket_names = [bucket["Name"] for bucket in response["Buckets"]]
    assert len(response) > 0
    assert config.AWS_BUCKET_NAME in bucket_names

def test_upload_raw_data():
    test_dict = {
        "name": "John Doe",
        "age": 30,
        "location": "Wonderland"
    }
    try:
        aws_client.upload_raw_data(test_dict)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")

def test_get_json_as_dict():
    response = aws_client.get_json_as_dict("temp_20250920_202654_697.json")
    assert response
    assert response["name"] == "John Doe"
    assert response["age"] == 30
    assert response["location"] == "Wonderland"

def test_get_object_keys_with_pattern():
    today_str = "20250920"
    response = aws_client.get_object_keys_with_pattern(pattern=today_str)
    assert response
    assert "temp_20250920_202654_697.json" in response
    assert "temp_20250924_200211_952.json" not in response

def test_get_object_keys_with_pattern_should_be_reversed():
    today_str = "20250924"
    response = aws_client.get_object_keys_with_pattern(pattern=today_str)
    assert response
    assert "temp_20250924_200528_981.json" == response[0]
    assert "temp_20250924_200211_952.json" == response[1]
