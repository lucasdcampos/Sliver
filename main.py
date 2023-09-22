import mistune
import os
import yaml
import shutil
from jinja2 import Environment, FileSystemLoader

input_folder = 'content/_posts'
output_folder = 'build'
layout_folder = 'layout'
templates_folder = 'templates'
blog_posts = []

def main():
    # Initialize the Jinja2 environment with the 'layout' folder as the template directory.
    env = Environment(loader=FileSystemLoader('layout'))
    global config
    config = load_config()
    base_url = config.get('base-url', '')
    
    # Create the article folder based on the configuration.
    create_article_folder(config)

    # Copy styles and assets from 'resources' to 'assets'.
    get_styles()
    create_assets_folder()

    # Process each Markdown file in the 'content/_posts' folder.
    for filename in os.listdir(input_folder):
        if filename.endswith(".md"):
            input_path = os.path.join(input_folder, filename)
            post = convert_md_to_html(input_path)
            post_file_path = 'article/' + os.path.splitext(filename)[0] + ".html"
            post['post_file'] = post_file_path

            # Create an HTML file for each post.
            create_post_html(env, config, base_url, post, 'build/'+post_file_path)
    
    # After processing the posts, render HTML pages.
    rendered_html_pages = render_html_pages(env, config, base_url)

    # Write the rendered HTML pages to the 'build' folder.
    for page_name, page_content in rendered_html_pages.items():
        page_path = os.path.join(output_folder, page_name)
        with open(page_path, 'w', encoding='utf-8') as page_file:
            page_file.write(page_content)

def load_config():
    # Load the configuration settings from 'config.yml'.
    with open('config.yml', 'r') as config_yml:
        return yaml.load(config_yml, Loader=yaml.FullLoader)

def create_article_folder(config):
    # Create the article folder based on the configuration.
    article_folder = os.path.join(output_folder, config['post-output'])
    os.makedirs(article_folder, exist_ok=True)

def create_assets_folder():
    source_folder = 'resources'
    target_folder = os.path.join(output_folder, 'assets')

    # Check if the target folder ('assets') exists and remove it if it does.
    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)

    try:
        # Copy the contents of the 'resources' folder to the 'assets' folder.
        shutil.copytree(source_folder, target_folder)
    except Exception as e:
        print(f"Error while loading and copying folder: {e}")

def create_post_html(env, config, base_url, post, output_path):
    base_template = load_base_template()
    complete_post = base_template.replace('{{ postContent }}', post['post_content'])
    blog_posts.sort(key=lambda post: post['post_date'], reverse=True)
    blog_posts.append(post)
    
    # Ensure that the 'article' directory exists.
    article_dir = os.path.dirname(output_path)
    os.makedirs(article_dir, exist_ok=True)

    context = create_context(env, config, base_url, post, 'a')
    
    # Render the template with the context.
    post_content = env.from_string(complete_post).render(context)
    
    with open(output_path, 'w', encoding='utf-8') as post_file:
        post_file.write(post_content)

def create_context(env, config, base_url, post=None, page_title=None):
    # If the page is a post and has a title, use the post's title.
    # Otherwise, use the default title from the configuration.
    if post and 'post_title' in post:
        title = post['post_title']
    else:
        title = config['title']
    
    context = {
        'title': title,
        'baseurl': base_url,
        'styles': stylesString,
        'styles2': stylesStringSubfolder,
        'styles3': stylesStringSubfolder2,
        'blog_posts': blog_posts,
    }

    if post:
        context['post_file'] = post.get('post_file', '')
        context['post_title'] = post.get('post_title', '')
        context['page_title'] = title  # Use the same title defined above
        context['post_date'] = post.get('post_date', '')
        context['post_tags'] = post.get('post_tags', [])
        context['post_description'] = post.get('post_description', '')

    return context

def load_layout_content(filename):
    with open(os.path.join(layout_folder, filename), 'r', encoding='utf-8') as file:
        return file.read()

def load_base_template():
    with open('layout/base.html', 'r', encoding='utf-8') as base_file:
        return base_file.read()

def get_styles():
    linkStylesSubfolder = []
    linkStylesSubfolder2 = []
    linkStyles = []

    for style in config['templates']:
        linkStyles.append(f'<link rel="stylesheet" href="assets/styles/{style}">')
        linkStylesSubfolder.append(f'<link rel="stylesheet" href="../assets/styles/{style}">')
        linkStylesSubfolder2.append(f'<link rel="stylesheet" href="../../assets/styles/{style}">')

    global stylesString, stylesStringSubfolder, stylesStringSubfolder2
    stylesString = '\n'.join(linkStyles)
    stylesStringSubfolder = '\n'.join(linkStylesSubfolder)
    stylesStringSubfolder2 = '\n'.join(linkStylesSubfolder2)

def render_html_pages(env, config, base_url):
    rendered_pages = {}

    for page in config.get('html-pages', []):
        page_path = os.path.join(layout_folder, page)

        # Load the content of the content page.
        with open(page_path, 'r', encoding='utf-8') as file:
            page_content = file.read()

        # Create a Jinja2 context with the content parts.
        context = create_context(env, config, base_url, '')

        # Render the page with the context.
        rendered_page = env.from_string(page_content).render(context)
        rendered_pages[page] = rendered_page

    return rendered_pages

def convert_md_to_html(input_path):
    with open(input_path, 'r', encoding='utf-8') as md_file:
        markdown_lines = md_file.readlines()

    metadata_list = []
    content = []
    metadata_started = False

    for line in markdown_lines:
        if metadata_started:
            if line.strip() == '---':
                metadata_started = False
            else:
                metadata_list.append(line)
        else:
            if line.strip() == '---':
                metadata_started = True
            else:
                content.append(line)

    if metadata_list:
        metadata_string = ''.join(metadata_list)
        metadata_dict = yaml.load(metadata_string, Loader=yaml.FullLoader)
        post_title = metadata_dict.get('title', 'Untitled')
        post_date = metadata_dict.get('date', 'Unknown Date')
        post_tags = metadata_dict.get('tags', [])
        post_description = metadata_dict.get('description', '')

        post = {
            "post_title": post_title,
            "post_date": post_date,
            "post_tags": post_tags,
            "post_description": post_description,
        }

        markdown_text = ''.join(content)

        markdown = mistune.Markdown(renderer=HTMLRendererWithHeaders())
        post_html = markdown(markdown_text)

        post['post_content'] = post_html

        return post

class HTMLRendererWithHeaders(mistune.HTMLRenderer):
    def header(self, text, level, raw=None):
        return f'<h{level}>{text}</h{level}>'

if __name__ == "__main__":
    main()
