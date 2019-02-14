
from xml.sax.saxutils import escape, unescape

 # escape() and unescape() takes care of &, < and >.

html_escape_table = {
'"': "&quot;",
"'": "&apos;",
".": "&#46;",
"@": "&#64;",
"#": "&#35;"
}
html_unescape_table = {v: k for k, v in html_escape_table.items()}

def html_escape(text):
    return escape(text, html_escape_table)

def html_unescape(text):
    return unescape(text, html_unescape_table)

if __name__=="__main__":
    print(html_escape("'@#jabkljldsjfldks"))