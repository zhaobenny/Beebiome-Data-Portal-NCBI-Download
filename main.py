import argparse
import logging
import os
from datetime import datetime

import toml

from upload.upload import upload
from download.download_manager import download

config = toml.load("config.toml")
runtime_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
if config["logging"]["filepath"] == "" or config["logging"]["filepath"] is None:
    logging.basicConfig(level=config['logging']['level'],
                        format="%(asctime)s %(levelname)s %(message)s", datefmt='%Y-%m-%d-%H:%M:%S')
else:
    logging.basicConfig(level=config['logging']['level'], filename=config['logging']['filepath'].format(runtime_timestamp),
                        format="%(asctime)s %(levelname)s %(message)s", datefmt='%Y-%m-%d-%H:%M:%S')
logger = logging.getLogger(__name__)


def main(taxon="Apoidea", filepath=None):
    config["taxon"] = taxon

    if filepath is None:
        filepath = f'./data/{taxon}_({runtime_timestamp})_run'
        os.makedirs(filepath, exist_ok=True)

    logger.info("Starting download process of NCBI XMLs")
    download(filepath, config)
    logger.info(
        f'Download process finished. Total time taken: {(datetime.now() - datetime.strptime(runtime_timestamp, "%Y-%m-%d_%H-%M")).strftime("%H:%M:%S")}')

    upload_db = False
    if (taxon == "Apoidea" and upload_db):
        upload(filepath)

    logging.shutdown()
    return filepath


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", type=str,
                        help="Optional filepath to save the downloaded XMLs to", default=None)
    parser.add_argument(
        "--name", type=str, help="Optional name of taxon subtree to download, default is Apoidea", default="Apoidea")
    args = parser.parse_args()
    main(taxon=args.name, filepath=args.filepath)
