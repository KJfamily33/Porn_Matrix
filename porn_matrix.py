from os import path
from flask import (Flask, send_from_directory,
                  render_template, request)
from search_to_url import get_direct_link

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# AFAIK we don't need to worry about sanitizing input
# Flask escapes all input by default
@app.route("/")
def main_page():
    cols = int(request.args.get("cols", default=2))
    rows = int(request.args.get("rows", default=2))
    results = int(request.args.get("results", default=105))
    length = int(request.args.get("length", default=20))
    search = request.args.get("search", default="default")
    return render_template("vid_grid.html",
            cols=cols, rows=rows, results=results, length=length, search=search)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(path.join(app.root_path, "static"),
                               "favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.route("/search/<query>")
def direct_vid_link(query):
    results = int(request.args.get("results", default=105))
    length = int(request.args.get("length", default=20))
    direct_link = get_direct_link(query, results=results, length=length)
    return direct_link

if __name__ == "__main__":
    import sys
    import waitress
    import webbrowser
    print("Porn Matrix.exe 8080 to run on port 8080, etc.")
    PORT = sys.argv[1] if len(sys.argv) > 1 else '69'
    webbrowser.open('http://127.0.0.1:' + PORT)
    waitress.serve(app, port=PORT, threads=8)