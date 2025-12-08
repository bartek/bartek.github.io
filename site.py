import sys
import os

from flask import Flask, abort, render_template, redirect
from flask_frozen import Freezer

from blog.flatpages import discover_pages, get_page

app = Flask(__name__)
freezer = Freezer(app)
discover_pages(app)

@app.route("/")
def index():
    posts = []
    for key, full_path in app.page_index.items():
        if key.startswith('posts/'):
            page = get_page(full_path)
            posts.append({'slug': key.replace('posts/', ''), 'title': page.get('title', key), 'date': page.get('date')})
    posts.sort(key=lambda p: p['date'] or 0, reverse=True)
    return render_template("index.html", posts=posts)


@freezer.register_generator
def pages():
    for key in app.page_index.keys():
        yield "page", {"path": key}


@app.route("/p/<path:path>/")
def page_with_prefix(path):
    """
    Updated URL for pages. Previous URLS should perma-redirect to this scheme.
    """
    full_path = app.page_index.get(path)
    page = get_page(full_path)
    if not page:
        abort(404)
    return render_template("page.html", page=page)

@app.route("/hfxbikeparking/")
def hfxbikeparking():
    """
    Pointer to github.com/bartek/hfxbikeparking build
    """
    return render_template("hfxbikeparking/index.html", token=os.environ.get('MAPBOX_TOKEN'))


@app.route("/<path:path>/")
def page(path):
    p = app.page_index.get(path)
    if not p:
        abort(404)
    return redirect(f"/p/{path}", code=301)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=4000, debug=True)
