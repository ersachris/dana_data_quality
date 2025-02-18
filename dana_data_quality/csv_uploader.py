import argparse
from dataclasses import dataclass
from google.cloud.storage import Client, transfer_manager
from typing import List


@dataclass
class CsvUploader:
    source_dir: str
    gcs_bucket: str
    filenames: List[str]
    workers: int

    def __post_init__(self) -> None:
        self.filenames = [f"{filename}.csv" for filename in self.filenames]
        self.client = Client()

    def upload_to_gcs(self) -> None:
        bucket = self.client.bucket(self.gcs_bucket)

        results = transfer_manager.upload_many_from_filenames(
            bucket, self.filenames, source_directory=self.source_dir, max_workers=self.workers
        )

        for name, result in zip(self.filenames, results):
            if isinstance(result, Exception):
                print("Failed to upload {} due to exception: {}".format(name, result))
            else:
                print("Uploaded {} to {}.".format(name, bucket.name))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=str, required=True, help="Directory of the CSV files")
    parser.add_argument("--gcs-bucket", type=str, required=True, help="Name of the GCS bucket the files will be uploaded to")
    parser.add_argument(
        "--filenames", 
        type=str, 
        required=True, 
        help="Comma separated CSV filename to be ingested without the '.csv' extention"
    )
    parser.add_argument(
        "--workers", 
        type=int, 
        required=False, 
        help="Number of concurrent file uploads",
        default=5
    )
    return parser.parse_args()

def main():
    args = parse_args()
    filenames = args.filenames.split(",")
    uploader = CsvUploader(
        args.source_dir,
        args.gcs_bucket,
        filenames,
        args.workers,
    )
    uploader.upload_to_gcs()

if __name__ == '__main__':
   main()