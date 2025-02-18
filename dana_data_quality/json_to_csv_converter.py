import argparse
import pandas as pd
from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from typing import List

@dataclass
class JsonToCsvConverter:
    source_dir: str
    targer_dir: str
    filenames: List[str]
    chunk_size: int
    schema_dir: str
    source_dir_path: Path = field(init=False)
    targer_dir_path: Path = field(init=False)

    def __post_init__(self):
        self.source_dir_path = Path(self.source_dir)
        self.targer_dir_path = Path(self.targer_dir)
    
    def load_schema(self, filename: str) -> dict:
        module_name = f"{self.schema_dir}.{filename}"
        return import_module(module_name).schema       
    
    def load_json_as_df(self, filename: str) -> pd.DataFrame:
        schema = self.load_schema(filename)

        with open(self.source_dir_path / (filename + ".json"), "r") as f:
            reader = pd.read_json(f, orient="records", lines=True,
                        dtype=schema, chunksize=self.chunk_size)
        
            df = []
            for chunk in reader:
                df.append(chunk)

        return pd.concat(df, ignore_index=True)

    def save_as_csv(self, filename, df) -> None:
        df.to_csv(self.targer_dir_path / (filename + ".csv"), index=False)

    def execute(self):
        for filename in self.filenames:
            df = self.load_json_as_df(filename)
            self.save_as_csv(filename, df)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=str, required=True, help="Directory of the JSON files")
    parser.add_argument("--target-dir", type=str, required=True, help="Directory to put the CSV files")
    parser.add_argument(
        "--filenames", 
        type=str, 
        required=True, 
        help="Comma separated JSON filename to be ingested without the '.json' extention"
    )
    parser.add_argument(
        "--chunk-size", 
        type=int, 
        required=False, 
        help="Chunk size of JSON to be loaded into memory at the time, put it smaller if you are facing Out of memory issue",
        default=5000
    )
    parser.add_argument(
        "--schema-dir", 
        type=str, 
        required=False, 
        help="Directory of the schema files",
        default="schemas"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    filenames = args.filenames.split(",")
    converter = JsonToCsvConverter(
        args.source_dir,
        args.target_dir,
        filenames,
        args.chunk_size,
        args.schema_dir
    )
    converter.execute()

if __name__ == '__main__':
   main()