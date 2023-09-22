# Sliver - Static Website and Blog Generator

Sliver is a Python script that enables you to generate static websites and blogs quickly and easily. It simplifies the process of converting Markdown files into HTML and provides templating features for creating consistent web pages.

## Features

- Converts Markdown files to HTML.
- YAML front matter for defining metadata such as title, date, and tags for blog posts.
- Customizable templates using Jinja2.
- Automatic generation of blog index with sorting by date.
- Easily manage styles and templates.

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sliver.git
   cd sliver

2. **Install dependencies**
    ```bash
      pip install mistune jinja2 pyyaml
    ```
3. **Configuration**

    Customize your website by editing the config.yml file.

3. **Create Posts**

    Add your blog posts in Markdown format to the _posts directory. Use YAML front matter to define metadata.

    Example:

    ```markdown
    ---
    title: Sample Blog Post
    date: 2023-09-20
    tags: [tag1, tag2]
    ---
    # My Title!
    Your Markdown content goes here.
    ```

4. **Generate the Website**

    Run the following command to generate the website:

    ```bash
    python main.py
    ```

5. **View Your Website**

    The generated static website can be found in the build directory. Open **build/index.html** in your browser to view your website.

## Customization
  - Templates: Customize the website layout by editing the templates in the templates directory.
  
  - Styles: Add your own CSS styles by placing them in the assets/styles directory.

## Contributing
  Contributions are welcome! If you'd like to improve Sliver, feel free to submit issues or pull requests.

## License
  This project is licensed under the MIT License. See the **LICENSE** file for details.
