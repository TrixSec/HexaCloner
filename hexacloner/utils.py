from urllib.parse import urljoin, urlparse
import os

def url_to_path(url):
    parsed = urlparse(url)
    path = parsed.path
    if path.endswith('/') or path == '':
        path += 'index.html'
    return os.path.join(parsed.netloc, path.lstrip('/'))

def is_valid_url(current_url, href, base_url):
    full_url = urljoin(current_url, href)
    if full_url.startswith(base_url):
        return full_url
    return None

def save_file(output_dir, url, content, binary=False):
    rel_path = url_to_path(url)
    file_path = os.path.join(output_dir, rel_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    mode = 'wb' if binary else 'w'
    with open(file_path, mode, encoding=None if binary else 'utf-8') as f:
        f.write(content)
