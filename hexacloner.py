


from termcolor import cprint, colored
from hexacloner.core import HexaCloner
from hexacloner.cli import CLIOptions
from hexacloner.settings import BANNER, AUTHOR, GITHUB, VERSION, COPYRIGHT
import requests
def print_banner():
    cprint(BANNER, 'magenta', attrs=['bold'])
    cprint(f'Author: {AUTHOR}', 'cyan', attrs=['bold'])
    cprint(f'GitHub: {GITHUB}', 'yellow', attrs=['bold'])
    cprint(f'Version: {VERSION}', 'green', attrs=['bold'])
    cprint(COPYRIGHT, 'white', attrs=['bold'])

def check_version():
    try:
        url = 'https://raw.githubusercontent.com/TrixSec/HexaCloner/main/hexacloner/version.py'
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            remote = resp.text
            import re
            m = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", remote)
            if m:
                remote_version = m.group(1)
                from hexacloner.version import __version__
                if remote_version != __version__:
                    cprint(f"[!] New version available: {remote_version} (current: {__version__})", 'yellow', attrs=['bold'])
                    cprint("[>] Update using: python hexacloner.py --update", 'cyan', attrs=['bold'])
    except Exception:
        pass


def main():
    print_banner()
    check_version()
    url = input(colored('Enter the URL to clone: ', 'yellow', attrs=['bold']))
    threads = input(colored('Number of threads [default 5]: ', 'yellow', attrs=['bold']))
    threads = int(threads) if threads.isdigit() else 5
    cli_opts = CLIOptions()
    cli_opts.prompt()
    cloner = HexaCloner(
        url,
        num_threads=threads,
        resource_types=cli_opts.selected_types,
        include_pattern=cli_opts.include_pattern,
        exclude_pattern=cli_opts.exclude_pattern,
        max_depth=cli_opts.max_depth,
        username=cli_opts.username,
        password=cli_opts.password,
        import_session=cli_opts.import_session,
        export_session=cli_opts.export_session,
        session_file=cli_opts.session_file
    )
    cloner.run()
    cprint('Done!', 'green', attrs=['bold'])

if __name__ == '__main__':
    main()
