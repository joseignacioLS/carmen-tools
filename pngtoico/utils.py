import re


def get_content_section(func):
    def get_content_lines(content):
        return content.strip().split("\n")[1:]

    def wrap(*args, **kwargs):
        match = re.search(f"#{kwargs['section']}[^#]+", kwargs['content'])
        return func(*args, get_content_lines(match.group()) if match else [])

    return wrap

