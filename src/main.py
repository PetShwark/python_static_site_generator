import logging
import sys
logging.basicConfig(level=logging.INFO)
from copy_folder import copy_folder
from markdown_processor import generate_pages_recursively

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    logging.info(f"Base path set to: {basepath}")
    copy_folder("static", "docs") # Copy static assets, clear destination first
    generate_pages_recursively(
        basepath=basepath,
        from_dir="content",
        template_path="template.html",
        dest_dir="docs",
    )

if __name__ == "__main__":
    main()