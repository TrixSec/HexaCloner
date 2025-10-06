import re
import getpass
from termcolor import cprint, colored

class CLIOptions:
    def __init__(self):
        self.resource_types = ['html', 'images', 'css', 'js', 'all']
        self.selected_types = set(['all'])
        self.include_pattern = None
        self.exclude_pattern = None
        self.max_depth = None
        self.username = None
        self.password = None
        self.session_file = None
        self.import_session = False
        self.export_session = False

    def prompt(self):
        cprint('--- HexaCloner Advanced Options ---', 'cyan', attrs=['bold'])
        # Resource selection
        types = input(colored('Resources to clone (comma: html,images,css,js,all) [all]: ', 'yellow', attrs=['bold']))
        if types:
            self.selected_types = set(t.strip() for t in types.split(',') if t.strip() in self.resource_types)
            if not self.selected_types:
                self.selected_types = set(['all'])
        # URL filtering
        inc = input(colored('Include URL pattern (regex, optional): ', 'yellow'))
        if inc:
            self.include_pattern = inc
        exc = input(colored('Exclude URL pattern (regex, optional): ', 'yellow'))
        if exc:
            self.exclude_pattern = exc
        # Depth
        depth = input(colored('Max crawl depth (int, optional): ', 'yellow'))
        if depth.isdigit():
            self.max_depth = int(depth)
        # Auth
        auth = input(colored('Use HTTP Auth? (y/N): ', 'yellow'))
        if auth.lower() == 'y':
            self.username = input(colored('Username: ', 'yellow'))
            self.password = getpass.getpass(colored('Password: ', 'yellow'))
        # Session import/export
        sess = input(colored('Import previous session? (y/N): ', 'yellow'))
        if sess.lower() == 'y':
            self.import_session = True
            self.session_file = input(colored('Session file to import: ', 'yellow'))
        sess = input(colored('Export session after clone? (y/N): ', 'yellow'))
        if sess.lower() == 'y':
            self.export_session = True
            self.session_file = input(colored('Session file to export: ', 'yellow'))
