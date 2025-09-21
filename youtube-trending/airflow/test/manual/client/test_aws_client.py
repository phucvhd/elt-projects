from datetime import datetime

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
    result = aws_client.upload_raw_data(test_dict)
    assert result

def test_get_json_as_dict():
    response = aws_client.get_json_as_dict("temp_20250920_202654_697.json")
    assert response
    assert response["name"] == "John Doe"
    assert response["age"] == 30
    assert response["location"] == "Wonderland"

def test_get_object_keys_with_pattern():
    today_str = datetime.now().strftime('%Y%m%d')
    response = aws_client.get_object_keys_with_pattern(pattern=today_str)
    assert response
    assert "temp_20250920_202654_697.json" in response
