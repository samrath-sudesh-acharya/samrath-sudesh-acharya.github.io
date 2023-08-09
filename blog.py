import json

def blog_page():

    def generate_blog_html(blog_data):
        html_content = ""
        for blog in blog_data:
            html_content += f'<a href="{blog["blog_url"]}">{blog["blog_title"]}</a>\n'
            html_content += f'<br>\n<code>//</code>Published: {blog["blog_published_time"]}\n'
            html_content += f'<br>\n<code>//</code>{blog["blog_summary"]}\n'
            html_content += '<br>\n<br>\n<br>\n'
        return html_content
    
    def update_html_file(html_content):
        with open('blog.html', 'r') as html_file:
            original_html = html_file.read()
    
        # Find the position to insert the new blogs after the <h1 class="animate"> Blogs </h1> element
        insert_index = original_html.find('<h1 class="animate"> Blogs </h1>')
        if insert_index == -1:
            # If <h1 class="animate"> Blogs </h1> not found, just append the new content to the end
            modified_html = original_html + html_content
        else:
            # Insert the new blogs after the <h1 class="animate"> Blogs </h1> element
            insert_index += len('<h1 class="animate"> Blogs </h1>')
            modified_html = original_html[:insert_index] + html_content + original_html[insert_index:]
    
        with open('blog.html', 'w') as html_file:
            html_file.write(modified_html)
    
    # Read the data from the JSON file
    with open('./blog/processed_blogs.json', 'r') as json_file:
        blog_data = json.load(json_file)
        
    # Generate the HTML content
    html_content = generate_blog_html(blog_data)
    
    # Update the HTML file by adding new content after the <h1 class="animate"> Blogs </h1> element
    update_html_file(html_content)
