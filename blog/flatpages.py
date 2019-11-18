import logging
import os
from itertools import takewhile
from typing import List

import markdown
import yaml
from flask import Flask

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')

config = {
    'root': os.path.join(BASE_DIR, 'pages'),
    'encoding': 'utf-8',
    'extension': '.md',
    'html_renderer': markdown,
}

logger = logging.getLogger(__name__)

def discover_pages(app: Flask) -> List[dict]:
    """
    Walk the flatpage directory, finding, parsing, and
    storing all pages in an index
    """
    page_index = {}
    for current_path, _, file_list in os.walk(config['root']):
        relative_path = current_path.replace(config['root'], '').lstrip(os.sep)

        for name in file_list:
            if not name.endswith(config['extension']):
                continue

            name_without_extension = os.path.splitext(name)[0]
            full_path = os.path.join(relative_path, name_without_extension)

            page = get_page(full_path)
            page_index[full_path] = page

            # If the file name is index, strip the name and add a pointer
            # from the base directory to the full content.
            if name_without_extension == 'index':
                page_index[full_path.rsplit('/', 1)[0]] = page

    app.page_index = page_index
    return app

def parse_page(content: str) -> dict:
    """
    Given the contents of a Markdown file, parse
    the YAML config and HTML content
    """
    lines = iter(content.split('\n'))

    # Read lines until we hit the empty line
    meta = '\n'.join(takewhile(lambda l: l != '---', lines))
    meta = yaml.safe_load(meta)
    content = '\n'.join(lines)

    # Render the Markdown content as HTML
    html = markdown.markdown(content)

    return dict(
        **meta,
        **{'html': html},
    )

def get_page(path: str, encoding: str=None) -> dict:
    """
    Accept a path in the vein of the blog, open it
    within the filesystem, and parse its contents
    """
    logger.debug("Getting %s", path)
    if encoding is None:
        encoding = config['encoding']

    path = os.path.join(config['root'], path + ".md")

    with open(path, encoding=encoding) as file:
        content = file.read()
    return parse_page(content)
