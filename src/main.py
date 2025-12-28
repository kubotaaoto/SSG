from textnode import TextNode, TextType
import os
import shutil
from generate_page import copy_static, generate_pages_recursive


def main():
    if os.path.exists("public"):
        print("Deleting public directory...")
        shutil.rmtree("public")
    os.mkdir("public")
    print("Copying static files to public directory...")
    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    

main()