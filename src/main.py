import sys
import os
import shutil

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, markdown_to_html_node
from extractmarkdown import extract_markdown_images, extract_markdown_links

if len(sys.argv) > 1:
	basepath = sys.argv[1]
else:
	basepath = "/"


def main():
	#node = TextNode("this is text", TextType.LINK, "this is url")
	#message = node.__repr__()
	#print(message)

	copy_directory("static", "docs")

	#generate_page("content/index.md", "template.html", "public/index.html")
	generate_pages_recursive("content", "template.html", "docs")





### Recursive function that copies contents from a source directory to a destination directory (in this instance from static to public)
def copy_directory(source, destination):
	#import os
	#import shutil

	if os.path.exists(destination):
		shutil.rmtree(destination)

	os.makedirs(destination)
	for item in os.listdir(source):
		source_item = os.path.join(source, item)
		destination_item = os.path.join(destination, item)

		if os.path.isdir(source_item):
			copy_directory(source_item, destination_item)
		else:
			shutil.copy2(source_item, destination)


### Function the extracts title from a markdown text, if there is no title raises exception
def extract_title(markdown):
	lines = markdown.splitlines()
	for line in lines:
		if line.startswith("# "):
			return line.replace("# ", "").strip()

	raise ValueError("Markdown text must contain a title starting with '# '")


### Generates an HTML page from a markdown file, using a template file and saves it to the destination path. The template file must contain {{ Content }} and {{ Title }} as placeholders for the content and title respectively.
def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path} template")

	from_path_var = open(from_path).read()
	template_path_var = open(template_path).read()

	html_string = markdown_to_html_node(from_path_var).to_html()
	title = extract_title(from_path_var)

	template_path_var = template_path_var.replace("{{ Content }}", html_string)
	template_path_var = template_path_var.replace("{{ Title }}", title)
	template_path_var = template_path_var.replace('href="/', f'href="{basepath}')
	template_path_var = template_path_var.replace('href="/', f'href="{basepath}')

	if not os.path.exists(os.path.dirname(dest_path)):
		os.makedirs(os.path.dirname(dest_path))

	open(dest_path, "w").write(template_path_var)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	for item in os.listdir(dir_path_content):
		content_item = os.path.join(dir_path_content, item)
		dest_item = os.path.join(dest_dir_path, item)

		if os.path.isdir(content_item):
			generate_pages_recursive(content_item, template_path, dest_item)
		else:
			if os.path.isfile(content_item) and content_item.endswith(".md"):
				generate_page(content_item, template_path, dest_item.replace(".md", ".html"))


	
main()
