import requests
from bs4 import BeautifulSoup
from termcolor import cprint, colored
from .utils import url_to_path, is_valid_url, save_file


import re

class Downloader:
    def __init__(self, base_url, output_dir, state, resource_types=None, include_pattern=None, exclude_pattern=None, max_depth=None, username=None, password=None):
        self.base_url = base_url
        self.output_dir = output_dir
        self.state = state
        self.resource_types = resource_types or set(['all'])
        self.include_pattern = re.compile(include_pattern) if include_pattern else None
        self.exclude_pattern = re.compile(exclude_pattern) if exclude_pattern else None
        self.max_depth = max_depth
        self.username = username
        self.password = password
        self.session = requests.Session()
        if username and password:
            self.session.auth = (username, password)

    def clone_page(self, url, to_visit, lock, depth=0):
        if self.max_depth is not None and depth > self.max_depth:
            cprint('[!] Max depth reached for: ', 'red', attrs=['bold'], end='')
            cprint(url, 'white', attrs=['bold'])
            return
        if self.include_pattern and not self.include_pattern.search(url):
            cprint('[!] Skipping (no match): ', 'yellow', attrs=['bold'], end='')
            cprint(url, 'white', attrs=['bold'])
            return
        if self.exclude_pattern and self.exclude_pattern.search(url):
            cprint('[!] Skipping (excluded): ', 'yellow', attrs=['bold'], end='')
            cprint(url, 'white', attrs=['bold'])
            return
        cprint('[>] Cloning: ', 'cyan', attrs=['bold'], end='')
        cprint(url, 'white', attrs=['bold'])
        try:
            resp = self.session.get(url, timeout=10)
        except Exception as e:
            cprint('[!] Request error: ', 'red', attrs=['bold'], end='')
            cprint(f'{url} ({e})', 'white', attrs=['bold'])
            return
        if resp.status_code != 200:
            cprint('[!] Failed to fetch: ', 'red', attrs=['bold'], end='')
            cprint(url, 'white', attrs=['bold'])
            return
        soup = BeautifulSoup(resp.text, 'html.parser')
        if 'all' in self.resource_types or 'html' in self.resource_types:
            save_file(self.output_dir, url, resp.text)
        self.enqueue_links(soup, url, to_visit, lock, depth)
        self.download_assets(soup, url)

    def enqueue_links(self, soup, current_url, to_visit, lock, depth):
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = is_valid_url(current_url, href, self.base_url)
            if full_url:
                with lock:
                    if not self.state.is_visited(full_url):
                        to_visit.put((full_url, depth + 1))

    def download_assets(self, soup, current_url):
        tags = {}
        if 'all' in self.resource_types or 'images' in self.resource_types:
            tags['img'] = 'src'
        if 'all' in self.resource_types or 'css' in self.resource_types:
            tags['link'] = 'href'
        if 'all' in self.resource_types or 'js' in self.resource_types:
            tags['script'] = 'src'
        # Add more tags for fonts, videos, etc. as needed
        for tag, attr in tags.items():
            for element in soup.find_all(tag):
                asset_url = element.get(attr)
                if asset_url:
                    full_url = is_valid_url(current_url, asset_url, self.base_url)
                    if full_url:
                        self.save_asset(full_url, tag)

    def save_asset(self, url, tag=None):
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                save_file(self.output_dir, url, resp.content, binary=True)
                cprint('[+] Asset saved: ', 'green', attrs=['bold'], end='')
                cprint(url, 'white', attrs=['bold'])
        except Exception as e:
            cprint('[!] Failed to download asset: ', 'red', attrs=['bold'], end='')
            cprint(f'{url} ({e})', 'white', attrs=['bold'])
