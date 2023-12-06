import os
from io import BytesIO

import boto3
import pytest
from birdnetlib.exceptions import AudioFormatError
from dotenv import load_dotenv

from remote import Remote

from .utils import (
    return_stubber_client_for_filedownload,
)

load_dotenv(".env")

API_ENDPOINT = os.environ.get("API_ENDPOINT", "")
API_KEY = os.environ.get("API_KEY", "")
S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY", "")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY", "")

s3 = boto3.resource("s3")

LIVE_TEST = False


def test_corrupt_file():
    # Setup stubber.
    bucket_name = "non-existant-bucket"
    key = "PROJECT/GROUP/file.wav"
    with open("tests/test_files/not_an_audio_file.wav", "rb") as fh:
        buf = BytesIO(fh.read())
    mocked_s3_client = return_stubber_client_for_filedownload(
        bucket_name, key, bcontents=buf
    )
    # Fake the queue return.
    queued_audio_dict = {
        "audio": {
            "file_path": key,
            "file_source": {
                "s3_bucket": bucket_name,
            },
        },
        "group": {
            "analyzer_config": {
                "analyzer": {"id": 1, "name": "BirdNET-Analyzer"},
                "minimum_detection_confidence": 0.6,
                "config": {},
                "id": 2,
            },
            "id": 1,
            "name": "Main Group",
        },
    }

    # Test file download.
    remote = Remote(
        api_endpoint=API_ENDPOINT,
        api_key=API_KEY,
        processor_id="local123",
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
    )
    remote._client = mocked_s3_client
    remote.queued_audio_dict = dict(queued_audio_dict)
    remote._retrieve_file()  # This is a real file now, let's analyze it.
    with pytest.raises(AudioFormatError):
        remote._analyze_file()

    assert remote.audio_filepath == "./file.wav"
    remote._cleanup_files()
    assert os.path.exists(remote.audio_filepath) is False
