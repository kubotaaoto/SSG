import os
import shutil
from block_markdown import markdown_to_html_node


def copy_static(src_dir, dst_dir):
    if not os.path.isdir(src_dir) or not os.path.isdir(dst_dir):
        raise ValueError("invalid argument(s)")
    items = os.listdir(src_dir)
    for item in items:
        path = f"{src_dir}/{item}"
        if os.path.isdir(path):
            os.mkdir(f"{dst_dir}/{item}")
            copy_static(path, f"{dst_dir}/{item}")
        elif os.path.isfile(path):
            shutil.copy(path, dst_dir)
        else:
            raise ValueError(f"{path} is neither a directory nor a file")

def extract_title(markdown):
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block.startswith("# "):
            return block[2:]
    raise Exception("no h1 header in markdown")

def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        return
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        contents = f.read()
    with open(template_path) as f:
        html_template = f.read()
    title = extract_title(contents)
    contents_html = markdown_to_html_node(contents).to_html()
    res = html_template.replace("{{ Title }}", title).replace("{{ Content }}", contents_html)
    
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(res)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    item_names = os.listdir(dir_path_content)
    for item_name in item_names:
        from_path = os.path.join(dir_path_content, item_name)
        if os.path.isfile(from_path):
            dest_path = os.path.join(dest_dir_path, item_name.split(".")[0] + ".html")
            generate_page(from_path, template_path, dest_path)
        if os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, f"{dest_dir_path}/{item_name}")