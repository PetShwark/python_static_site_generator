import logging
import os
logging.basicConfig(level=logging.INFO)
from copy_folder import copy_folder
from markdown_processor import markdown_to_html_node, generate_page, generate_pages_recursively

def main():
    copy_folder("static", "public") # Copy static assets, clear destination first
    generate_pages_recursively(
        from_dir="content",
        template_path="template.html",
        dest_dir="public",
    )

if __name__ == "__main__":
    main()