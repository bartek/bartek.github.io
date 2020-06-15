import sys

from flask import Flask, abort, render_template, redirect
from flask_frozen import Freezer

from blog.flatpages import discover_pages

app = Flask(__name__)
freezer = Freezer(app)

# Upon app load, we store all page content into memory. This is obviously
# obscene but warrants itself sufficient at time of writing. If I ever
# get around to writing more than a couple of things on here, I'll blow this
# up into something more sane.
discover_pages(app)

@app.route('/')
def index():
    return render_template('index.html')

@freezer.register_generator
def pages():
    for key in app.page_index.keys():
        yield 'page', {'path': key}

@app.route('/p/<path:path>/')
def page_with_prefix(path):
    """
    Updated URL for pages. Previous URLS should perma-redirect to this scheme.
    """
    p = app.page_index.get(path)
    if not p:
        abort(404)
    return render_template('page.html', page=p)

@app.route('/<path:path>/')
def page(path):
    p = app.page_index.get(path)
    if not p:
        abort(404)
    return redirect(f'/p/{path}', code=301)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=4000, debug=True)
