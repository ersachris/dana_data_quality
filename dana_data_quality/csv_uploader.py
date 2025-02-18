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

    def upload_to_gcs(self) -> None:
        """Upload every file in a list to a bucket, concurrently in a process pool.

        Each blob name is derived from the filename, not including the
        `source_directory` parameter. For complete control of the blob name for each
        file (and other aspects of individual blob metadata), use
        transfer_manager.upload_many() instead.
        """

        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # A list (or other iterable) of filenames to upload.
        # filenames = ["file_1.txt", "file_2.txt"]

        # The directory on your computer that is the root of all of the files in the
        # list of filenames. This string is prepended (with os.path.join()) to each
        # filename to get the full path to the file. Relative paths and absolute
        # paths are both accepted. This string is not included in the name of the
        # uploaded blob; it is only used to find the source files. An empty string
        # means "the current working directory". Note that this parameter allows
        # directory traversal (e.g. "/", "../") and is not intended for unsanitized
        # end user input.
        # source_directory=""

        # The maximum number of processes to use for the operation. The performance
        # impact of this value depends on the use case, but smaller files usually
        # benefit from a higher number of processes. Each additional process occupies
        # some CPU and memory resources until finished. Threads can be used instead
        # of processes by passing `worker_type=transfer_manager.THREAD`.
        # workers=8


        storage_client = Client()
        bucket = storage_client.bucket(self.gcs_bucket)

        results = transfer_manager.upload_many_from_filenames(
            bucket, self.filenames, source_directory=self.source_dir, max_workers=self.workers
        )

        for name, result in zip(self.filenames, results):
            # The results list is either `None` or an exception for each filename in
            # the input list, in order.

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