import logging
import os
import shutil


def copy_folder(src: str, dest: str) -> None:
    if not os.path.exists(dest):
        os.makedirs(dest)
    else:
        logging.info(f"Destination folder {dest} already exists. Erasing contents.")
        for item in os.listdir(dest):
            item_path = os.path.join(dest, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            copy_folder(s, d)
        else:
            logging.info(f"Copying {s} to {d}")
            shutil.copy(s, d)