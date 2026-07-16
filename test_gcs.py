from pathlib import Path

from google.cloud import storage

from app.core.config import settings


def main():

    client = storage.Client(
        project=settings.project_id,
    )

    bucket = client.bucket(
        settings.gcs_bucket,
    )

    blob = bucket.blob(
        "test.txt",
    )

    blob.upload_from_string(
        "Enterprise AI Orchestration Platform"
    )

    print(
        f"Uploaded to gs://{settings.gcs_bucket}/test.txt"
    )


if __name__ == "__main__":
    main()