# HexaCloner

HexaCloner is an advanced, modular, and highly configurable website cloner written in Python. It supports full site mirroring, selective resource cloning, authentication, session resume, and a colorful, prompt-based CLI. Designed for both beginners and power users, HexaCloner works on Windows CMD, Linux, and Termux.

## Features
- **Full Website Cloning**: Download HTML, images, CSS, JS, and more, preserving the original directory structure.
- **Selective Resource Cloning**: Choose to clone only HTML, images, CSS, JS, or all resources.
- **URL Filtering & Depth Control**: Include/exclude URLs by regex and set maximum crawl depth.
- **Threaded Downloads**: Fast, multi-threaded crawling and downloading.
- **Resume & Session Export/Import**: Resume incomplete downloads and export/import session state for robust recovery.
- **Authentication Support**: Clone protected/member-only sites with HTTP Basic Auth or cookies.
- **Progress Bar & Logging**: Real-time progress bar (tqdm) and detailed, color-coded logs.
- **Cross-Platform CLI**: Colorful, bold, and prompt-based interface for Windows, Linux, and Termux.

## Installation
1. Clone this repository or download the source code.
2. Install dependencies:
	```sh
	pip install -r requirements.txt
	```

## Usage
Run the main script and follow the prompts:

```sh
python hexacloner.py
```

### CLI Options
- **URL to clone**: The starting URL of the website.
- **Number of threads**: Number of parallel download threads (default: 5).
- **Resources to clone**: Choose from html, images, css, js, all (comma-separated).
- **Include/Exclude URL pattern**: Regex to filter URLs.
- **Max crawl depth**: Limit how deep the crawler goes.
- **Authentication**: Enter username/password for HTTP Auth if needed.
- **Session import/export**: Resume or save session state to a file.

### Example
```
python hexacloner.py
# Enter the URL to clone: https://example.com
# Number of threads [default 5]: 10
# Resources to clone (comma: html,images,css,js,all) [all]: html,images
# Include URL pattern (regex, optional): ^https://example.com/blog
# Exclude URL pattern (regex, optional): logout
# Max crawl depth (int, optional): 3
# Use HTTP Auth? (y/N): y
# Username: user
# Password: ******
# Import previous session? (y/N): n
# Export session after clone? (y/N): y
# Session file to export: mysession.pkl
```

## Advanced Features
- **Session Resume**: If interrupted, simply re-run with the same session file to continue.
- **Progress Bar**: See real-time progress with tqdm.
- **Detailed Logging**: Color-coded output for errors, warnings, and successes.

## Requirements
- Python 3.7+
- requests
- beautifulsoup4
- termcolor
- tqdm

## License
MIT License

## Contributing
Pull requests and suggestions are welcome!

## Disclaimer
Use HexaCloner responsibly. Always respect website terms of service and robots.txt.
