from textnode import TextNode, TextType
import os
import shutil
import sys
from generate_page import copy_static, generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if os.path.exists("docs"):
        print("Deleting docs directory...")
        shutil.rmtree("docs")
    os.mkdir("docs")
    print("Copying static files to docs directory...")
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    

main()