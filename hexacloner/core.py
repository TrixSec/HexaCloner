
import threading
import queue
from tqdm import tqdm
from .downloader import Downloader
from .state import StateManager


class HexaCloner:
    def __init__(self, base_url, output_dir='cloned_site', num_threads=5, state_file='hexacloner_state.pkl',
                 resource_types=None, include_pattern=None, exclude_pattern=None, max_depth=None,
                 username=None, password=None, import_session=False, export_session=False, session_file=None):
        self.base_url = base_url.rstrip('/')
        self.output_dir = output_dir
        self.num_threads = num_threads
        self.resource_types = resource_types or set(['all'])
        self.include_pattern = include_pattern
        self.exclude_pattern = exclude_pattern
        self.max_depth = max_depth
        self.username = username
        self.password = password
        self.import_session = import_session
        self.export_session = export_session
        self.session_file = session_file
        self.state = StateManager(state_file)
        self.downloader = Downloader(
            base_url, output_dir, self.state,
            resource_types=self.resource_types,
            include_pattern=self.include_pattern,
            exclude_pattern=self.exclude_pattern,
            max_depth=self.max_depth,
            username=self.username,
            password=self.password
        )
        self.to_visit = queue.Queue()
        self.lock = threading.Lock()
        if self.import_session and self.session_file:
            self.resume = self.state.load_file(self.to_visit, self.session_file)
        else:
            self.resume = self.state.load(self.to_visit)
        if self.to_visit.empty():
            self.to_visit.put((self.base_url, 0))
        self.progress = tqdm(total=0, desc='Cloning', unit='page', dynamic_ncols=True)

    def run(self):
        threads = []
        for _ in range(self.num_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
        self.to_visit.join()
        for t in threads:
            t.join(timeout=1)
        self.progress.close()
        if self.export_session and self.session_file:
            self.state.save_file(self.to_visit, self.session_file)
        else:
            self.state.save(self.to_visit)

    def worker(self):
        while True:
            try:
                url, depth = self.to_visit.get(timeout=3)
            except queue.Empty:
                return
            if self.state.is_visited(url):
                self.to_visit.task_done()
                continue
            try:
                self.downloader.clone_page(url, self.to_visit, self.lock, depth=depth)
            except Exception as e:
                print(f'[!] Error cloning {url}: {e}')
            self.state.mark_visited(url)
            self.state.save(self.to_visit)
            self.progress.update(1)
            self.to_visit.task_done()
