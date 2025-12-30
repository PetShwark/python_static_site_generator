import logging
import os
logging.basicConfig(level=logging.INFO)
from copy_folder import copy_folder
from markdown_processor import markdown_to_html_node, generate_page

def main():
    # import index markdown file and convert to HTMLNode
    # index_md_path = os.path.join("content", "index.md")
    # with open(index_md_path, "r", encoding="utf-8") as f:
    #     index_md = f.read()
    # logging.info("Converting markdown to HTMLNode...")
    # index_html_node = markdown_to_html_node(index_md)
    # logging.info("Conversion complete.")
    # logging.info("Generated HTML:")
    # html = index_html_node.to_html()
    # print(html)

    # copy_folder("static", "public") # Copy static assets, clear destination first
    generate_page(
        from_path=os.path.join("content", "index.md"),
        template_path="template.html",
        dest_path=os.path.join("public", "index.html"),
    )

if __name__ == "__main__":
    main()