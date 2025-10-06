import os
import pickle

class StateManager:
    def __init__(self, state_file):
        self.state_file = state_file
        self.visited = set()


    def load(self, to_visit):
        return self.load_file(to_visit, self.state_file)

    def load_file(self, to_visit, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                state = pickle.load(f)
                self.visited = state['visited']
                for url in state['to_visit']:
                    to_visit.put(url)
            print(f'[*] Resuming session from {file_path}...')
            return True
        return False


    def save(self, to_visit):
        self.save_file(to_visit, self.state_file)

    def save_file(self, to_visit, file_path):
        state = {
            'visited': self.visited,
            'to_visit': list(to_visit.queue)
        }
        with open(file_path, 'wb') as f:
            pickle.dump(state, f)

    def is_visited(self, url):
        return url in self.visited

    def mark_visited(self, url):
        self.visited.add(url)
