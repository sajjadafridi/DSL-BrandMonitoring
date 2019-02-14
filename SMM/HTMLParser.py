html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;",
            ".": "&#46;",
            "@": "&#64;",
            "#": "&#35;",
        }
html_unescape_table = {v:k for k, v in html_escape_table.items()}

class HTMLParser:
    # not working yet
    @staticmethod
    def html_unescape(text):
        return "".join(html_unescape_table.get(c, c) for c in text)

    @staticmethod
    def html_escape(text):
        return "".join(html_escape_table.get(c, c) for c in text)


if __name__=="__main__":
    v="djfldksjfl'dfsfsfdsf"
    v=v.replace("'","\\'")
    print(v)