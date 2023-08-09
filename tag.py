import json

def tag_page():
    # Read the processed_blogs_tags.json file
    with open('./blog/processed_blogs_tag.json', 'r') as f:
        processed_blogs = json.load(f)

    # Generate the HTML content for the tags and blogs
    html_content = ''
    for tag, blogs in processed_blogs.items():
        html_content += f'<ul><h1>{tag}</h1>'
        for blog in blogs:
            html_content += f'<ul><li><a href="{blog["blog_url"]}">{blog["blog_title"]}</a></li></ul>'
        html_content += '</ul>'

    # Read the existing page.html content
    with open('tag.html', 'r') as f:
        page_content = f.read()

    # Replace the <ul id="all-taxonomies"> section in page.html with the generated HTML content
    page_content = page_content.replace('<ul id="all-taxonomies"><ul>.*</ul></ul>', html_content)

    # Write the updated content back to page.html
    with open('tag.html', 'w') as f:
        f.write(page_content)
