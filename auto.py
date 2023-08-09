import os
import markdown
from jinja2 import Template
import re
from datetime import datetime
import json
import yaml
from blog import blog_page
from tag import tag_page

def remove_yaml_metadata(markdown_content):
    # Use regular expression to find the YAML metadata section in the Markdown content
    match = re.search(r'^---(.*?)---', markdown_content, re.DOTALL)
    if match:
        metadata_section = match.group(0)
        markdown_content = markdown_content.replace(metadata_section, '').strip()

    return markdown_content

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def convert_markdown_to_html(markdown_content):
    # Convert the Markdown content to HTML
    html_content = markdown.markdown(markdown_content, extensions=['extra'])

    # Add class="animate" to all header tags in the HTML content
    html_content = re.sub(r'<h(\d)>', r'<h\1 class="animate">', html_content)

    return html_content

def extract_blog_metadata(markdown_content):
    # Use regular expression to find the YAML metadata section in the Markdown content
    match = re.search(r'^---(.*?)---', markdown_content, re.DOTALL)
    if match:
        metadata_section = match.group(1).strip()
    else:
        print("YAML metadata section not found!")
        exit(1)
    
    # Parse the YAML metadata section
    metadata = yaml.safe_load(metadata_section)
    # Extract title, summary, and tags from metadata
    blog_title = metadata.get('title', 'Untitled Blog')
    blog_summary = metadata.get('summary', 'No summary available')
    tags = metadata.get('tags', [])
    blog_image = None
    # Use regular expression to find the first image reference in the Markdown content
    image_refs = re.findall(r'!\[\[(.*?)\]\]', markdown_content)
    if image_refs:
        blog_image = 'https://samrathsacharya.me/blog/images/' + image_refs[0].replace(" ", "_")

    # Remove the metadata section from the Markdown content
    markdown_content = markdown_content.replace(f'---{metadata_section}---', '').strip()
    
    # Remove YAML metadata section
    markdown_content = remove_yaml_metadata(markdown_content)

    # Use regular expression to find all tags in the Markdown content
    tags += re.findall(r'#(\w+)', markdown_content)
    tags = [tag.lower() for tag in tags]

    # Remove the tags from the Markdown content
    for tag in tags:
        markdown_content = markdown_content.replace('#' + tag, '')

    return blog_summary, markdown_content, tags,blog_image

def download_images_from_markdown(markdown_content, output_folder, obsidian_folder):
    # Use regular expression to find all image references in the Markdown content
    image_refs = re.findall(r'!\[\[(.*?)\]\]', markdown_content)

    # Create the "images" subfolder if it doesn't exist
    images_folder = os.path.join(output_folder, 'images')
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Download the images and save them in the "images" folder
    for image_ref in image_refs:
        image_file_path = os.path.join(obsidian_folder, image_ref)
        if os.path.exists(image_file_path):
            image_filename = os.path.basename(image_file_path)
            image_filename = image_filename.replace(" ", "_")  # Replace spaces with underscores
            image_filepath = os.path.join(images_folder, image_filename)

            # Copy the image to the output_folder/images directory
            with open(image_file_path, 'rb') as src_image:
                with open(image_filepath, 'wb') as dest_image:
                    dest_image.write(src_image.read())

            # Replace the image reference in the Markdown content with the image tag
            markdown_content = markdown_content.replace(f'![[{image_ref}]]', f'<img src="./images/{image_filename}" alt="{image_ref}">')

        else:
            print(f"Warning: Image not found: {image_ref}")

    return markdown_content



def generate_html_for_blog(markdown_file_path, output_folder, template_path, markdown_file, obsidian_folder):
    # Read the Markdown content from the file
    markdown_content = read_markdown_file(markdown_file_path)

    # Extract blog metadata from the Markdown content
    blog_title = markdown_file.split('.')[0]
    blog_summary, markdown_content, tags,blog_image = extract_blog_metadata(markdown_content)

    # Download images and update image references in the Markdown content
    markdown_content = download_images_from_markdown(markdown_content, output_folder, obsidian_folder)

    # Remove the summary placeholder from the Markdown content
    markdown_content = markdown_content.replace('<!--summary-->', '')

    # Convert the Markdown content to HTML
    blog_content = convert_markdown_to_html(markdown_content)

    # Replace special characters in blog title to create a valid file name
    blog_filename = re.sub(r'[^\w\s-]', '', blog_title).strip().lower()
    blog_filename = re.sub(r'[-\s]+', '-', blog_filename)

    # Get the current date in the format "<date> <month>, <year>"
    blog_published_time = datetime.now().strftime("%d %B, %Y")

    # Calculate the blog read time (you can customize this calculation based on your requirements)
    blog_read_time = len(markdown_content.split()) // 200  # Assuming 200 words per minute reading speed

    # Define the context data for the Jinja2 template
    context = {
        'blog_title': blog_title,
        'blog_summary': blog_summary,
        'blog_published_time': blog_published_time,
        'blog_read_time': f'{blog_read_time} minute read',
        'blog_content': blog_content,
        'blog_filename': blog_filename,
        'blog_image': blog_image
    }

    # Generate the final HTML page using the template and context data
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    template = Template(template_content)
    generated_html = template.render(context)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the generated HTML to a file
    output_file_path = os.path.join(output_folder, f'{blog_filename}.html')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(generated_html)

   # Define the blog information
    blog_info = {
        'blog_title': blog_title,
        'blog_summary': blog_summary,
        'blog_published_time': blog_published_time,
        'blog_url': 'https://samrathsacharya.me/blog/' + blog_filename + '.html'
    }

    processed_blogs_file = os.path.join(output_folder, 'processed_blogs.json')
    if os.path.exists(processed_blogs_file):
        with open(processed_blogs_file, 'r') as f:
            processed_blogs = json.load(f)
    else:
        processed_blogs = []

    processed_blogs.append(blog_info)
    with open(processed_blogs_file, 'w') as f:
        json.dump(processed_blogs, f, indent=4)

    # Update the JSON file with information about the processed blog
    processed_blogs_file = os.path.join(output_folder, 'processed_blogs_tag.json')
    if os.path.exists(processed_blogs_file):
        with open(processed_blogs_file, 'r') as f:
            processed_blogs = json.load(f)
    else:
        processed_blogs = {}

    # Update the dictionary with the blog information under the appropriate tag
    for tag in tags:
        tag = tag.lower()  # Convert the tag to lowercase for consistency
        if tag in processed_blogs:
            processed_blogs[tag].append(blog_info)
        else:
            processed_blogs[tag] = [blog_info]

    # Write the updated dictionary to the JSON file
    with open(processed_blogs_file, 'w') as f:
        json.dump(processed_blogs, f, indent=4)
    
    #Update the blog page
    blog_page()

    #Update the pages with tags
    tag_page()

def main():
    obsidian_folder = 'D:\Storage\Obsidian\Blog'
    output_folder = 'blog'
    template_path = 'blog-template.html'

    # Get all Markdown files in the Obsidian folder
    markdown_files = [file for file in os.listdir(obsidian_folder) if file.endswith('.md')]

    # Load the information about processed blogs from the JSON file
    processed_blogs_file = os.path.join(output_folder, 'processed_blogs.json')
    if os.path.exists(processed_blogs_file):
        with open(processed_blogs_file, 'r') as f:
            processed_blogs = json.load(f)
    else:
        processed_blogs = []

    # Generate HTML for new markdown files and update the JSON file with processed blog information
    for markdown_file in markdown_files:
        blog_title = markdown_file.split('.')[0]
        blog_filename = re.sub(r'[^\w\s-]', '', blog_title).strip().lower()
        blog_filename = re.sub(r'[-\s]+', '-', blog_filename)

        if not any(blog_info['blog_title'] == blog_title for blog_info in processed_blogs):
            markdown_file_path = os.path.join(obsidian_folder, markdown_file)
            with open(markdown_file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
                if not markdown_content.strip():
                    print(f"Warning: Empty Markdown file: {markdown_file}")
                    continue  # Skip empty Markdown files
            generate_html_for_blog(markdown_file_path, output_folder, template_path, markdown_file, obsidian_folder)

if __name__ == '__main__':
    main()
