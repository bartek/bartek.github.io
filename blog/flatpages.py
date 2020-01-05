import json
import logging
import os
from itertools import takewhile
from typing import List

import markdown
import yaml
from flask import Flask, render_template
from jinja2 import Environment

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')

config = {
    'root': os.path.join(BASE_DIR, 'pages'),
    'encoding': 'utf-8',
    'extensions': ['md', 'jinja2'],
    'html_renderer': markdown,
}

logger = logging.getLogger(__name__)

def jinja_parse(content: str, context: dict) -> str:
    """
    Accept what should be a jinja template, parse with context
    """
    env = Environment()
    t = env.from_string(content)

    # Silly, but makes life easy. If we identify a data key in the YAML context,
    # extract that for rendering purposes. Assumes JSON data as well.
    if 'data' in context:
        with open(os.path.join(BASE_DIR, 'pages', context['data'])) as f:
            context['data'] = json.loads(f.read())
    
    render_context = context.get('data', None)
    return t.render(**render_context)
    
filetypes = {
    'md': lambda c, _: markdown.markdown,
    'jinja2': jinja_parse,
}

def discover_pages(app: Flask) -> List[dict]:
    """
    Walk the flatpage directory, finding, parsing, and
    storing all pages in an index
    """
    page_index = {}
    for current_path, _, file_list in os.walk(config['root']):
        relative_path = current_path.replace(config['root'], '').lstrip(os.sep)

        for name in file_list:
            if not name.endswith(tuple(config['extensions'])):
                continue

            name_without_extension = os.path.splitext(name)[0]

            # The path that'll be used for build output
            build_path = os.path.join(relative_path, name_without_extension)

            # The path we need to find the file, has extension.
            full_path = os.path.join(relative_path, name)
            page = get_page(full_path)

            page_index[build_path] = page

            # If the file name is index, strip the name and add a pointer
            # from the base directory to the full content.
            if name_without_extension == 'index':
                page_index[buiild_path.rsplit('/', 1)[0]] = page

    app.page_index = page_index
    return app

def parse_page(path: str, content: str) -> dict:
    """
    Given the contents of a Markdown file, parse
    the YAML config and HTML content
    """
    lines = iter(content.split('\n'))

    # Read lines until we hit the empty line
    meta = '\n'.join(takewhile(lambda l: l != '---', lines))

    try:
        meta = yaml.safe_load(meta)
    except yaml.scanner.ScannerError as exc:
        logger.fatal("Could not parse YAML. Make sure it's valid, and use a three-dashed line (---) to separate YAML config with content.")
        raise exc

    content = '\n'.join(lines)

    # Identify filetype and parse accordingly.
    _, extension = os.path.splitext(path)

    template_parser = filetypes[extension[1:]]
    html = template_parser(content, meta)

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

    path = os.path.join(config['root'], path)

    with open(path, encoding=encoding) as file:
        content = file.read()
    return parse_page(path, content)
