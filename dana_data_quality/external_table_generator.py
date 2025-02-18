import argparse
from dataclasses import dataclass
from google.cloud import bigquery
from typing import List


@dataclass
class ExternalTableGenerator:
    filenames: List[str]
    gcs_bucket: str
    project_name: str
    dataset_name: str

    def __post_init__(self):
        self.client = bigquery.Client(project=self.project_name)

    def create_external_table(self, filename):
        external_config = bigquery.ExternalConfig('CSV')
        external_config.autodetect = True
        external_config.source_uris = [f"gs://{self.gcs_bucket}/{filename}.csv"]

        dataset_ref = self.client.dataset(self.dataset_name)
        table = bigquery.Table(dataset_ref.table(filename))
        table.external_data_configuration = external_config
        table = self.client.create_table(table, exists_ok=True)

    def execute(self):
        for filename in self.filenames:
            self.create_external_table(filename)
            print(f"External table {self.project_name}.{self.dataset_name}.{filename} created") 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filenames", 
        type=str, 
        required=True, 
        help="Comma separated CSV filename to be ingested without the '.csv' extention"
    )    
    parser.add_argument("--gcs-bucket", type=str, required=True, help="GCS bucket for source of the external table")
    parser.add_argument("--project-name", type=str, required=True, help="Project name where the external table will be created")
    parser.add_argument("--dataset-name", type=str, required=True, help="Dataset name where the external table will be created")
    return parser.parse_args()

def main():
    args = parse_args()
    filenames = args.filenames.split(",")
    generator = ExternalTableGenerator(
        filenames,
        args.gcs_bucket,
        args.project_name,
        args.dataset_name
    )
    generator.execute()

if __name__ == '__main__':
   main()