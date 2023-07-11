import boto3
import os
import argparse
import mimetypes
import logging


def configure_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
    )


def upload_to_s3(directory_path, bucket_name):
    """Upload files from a local directory to an S3 bucket.

    Args:
        directory_path (str): The local directory path.
        bucket_name (str): The name of the S3 bucket.
    """
    s3 = boto3.client("s3")
    logging.info(
        f"Started uploading files from '{directory_path}' to S3 bucket '{bucket_name}'"
    )

    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            s3_key = os.path.relpath(file_path, directory_path)

            content_type, _ = mimetypes.guess_type(file_path)
            content_type = content_type or "binary/octet-stream"

            try:
                with open(file_path, "rb") as data:
                    s3.put_object(
                        Bucket=bucket_name,
                        Key=s3_key,
                        Body=data,
                        ContentType=content_type,
                    )
                logging.info(
                    f"Uploaded file '{file_path}' to S3 bucket '{bucket_name}' with key '{s3_key}'"
                )
            except Exception as e:
                logging.error(f"Error while uploading file '{file_path}': {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Upload files from a local directory to an S3 bucket."
    )
    parser.add_argument("directory_path", type=str, help="The local directory path")
    parser.add_argument("bucket_name", type=str, help="The name of the S3 bucket")

    args = parser.parse_args()

    if not os.path.isdir(args.directory_path):
        sys.exit(f"Directory not found: {args.directory_path}")

    upload_to_s3(args.directory_path, args.bucket_name)


if __name__ == "__main__":
    configure_logging()
    main()
