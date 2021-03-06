import os
import shutil
import subprocess
import logging
from main import main as main_script

logger = logging.getLogger(__name__)

"""
Wrapper script for running in GCP.
"""

def main():
    download_folder = "./data"
    try:
        main_script()

        # Compressed downloaded files
        files = [os.path.join(download_folder, file)
                for file in os.listdir(download_folder)]
        for file in files:
            if os.path.isdir(file):
                shutil.make_archive(file, 'zip', file)
                shutil.rmtree(file)

        # Remove oldest run
        files = [os.path.join(download_folder, file)
                for file in os.listdir(download_folder)]
        if len(files) >= 3:
            oldest_file = min(files, key=os.path.getmtime)
            shutil.rmtree(oldest_file)

        # Remove oldest log file
        files = [os.path.join("/var/log/ncbi_download/", file) for file in os.listdir("/var/log/ncbi_download")]
        if len(files) >= 6:
            oldest_file = min(files, key=os.path.getmtime)
            os.remove(oldest_file)

    except Exception as e:
        logger.critical(e, exc_info=True)  # failsafe

    # stop the machine script is running on
    subprocess.call(["shutdown"])

if __name__ == "__main__":
    main()