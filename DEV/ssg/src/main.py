import os
import shutil

from parse_markdown import markdown_to_html_node


def copy_rec(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)

    entries = os.listdir(src)
    for entry in entries:
        src_path = os.path.join(src, entry)
        dest_path = os.path.join(dest, entry)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_rec(src_path, dest_path)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.split("# ", 1)[1].strip()


def main():
    from_path = os.path.expanduser("~/DEV/ssg/content")
    template_path = os.path.expanduser("~/DEV/ssg/template.html")
    dest_path = os.path.expanduser("~/DEV/ssg/public")
    print(f"From path exists: {os.path.exists(from_path)}")
    print(f"Template path exists: {os.path.exists(template_path)}")
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public")
    if os.path.exists("static"):
        copy_rec("static", "public")
    generate_page_recursive(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file:
        md = md_file.read()
        print("Markdown content:", repr(md))
    with open(template_path) as template_file:
        template = template_file.read()
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    new_doc = template.replace("{{ Title }}", title)
    new_doc = new_doc.replace("{{ Content }}", content)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as dest_file:
        dest_file.write(new_doc)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    print(
        f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}"
    )
    entries = os.listdir(dir_path_content)
    for entry in entries:

        entry_path = os.path.join(dir_path_content, entry)
        dest_entry_path = os.path.join(dest_dir_path, entry)

        if entry.endswith(".md"):
            dest_entry_path = dest_entry_path[:-3] + ".html"
            os.makedirs(os.path.dirname(dest_entry_path), exist_ok=True)

            with open(entry_path) as md_file:
                md = md_file.read()
            with open(template_path) as template_file:
                template = template_file.read()

            content = markdown_to_html_node(md).to_html()
            title = extract_title(md)
            new_doc = template.replace("{{ Title }}", title)
            new_doc = new_doc.replace("{{ Content }}", content)

            with open(dest_entry_path, "w") as dest_file:
                dest_file.write(new_doc)

        elif os.path.isdir(entry_path):
            os.makedirs(dest_entry_path, exist_ok=True)
            generate_page_recursive(entry_path, template_path, dest_entry_path)


if __name__ == "__main__":
    main()
