class Result:
    def __init__(self, results, logs, error):
        self.results = results
        self.logs = logs
        self.error = error

    def __str__(self):
        return f"Result(results={self.results}, logs={self.logs}, error={self.error})"

    def json(self):
        return {
            'results': self.results,
            'logs': self.logs.json() if self.logs else None,
            'error': self.error.json() if self.error else None
        }

class Logs:
    def __init__(self, stdout, stderr):
        self.stdout = stdout.splitlines() if stdout else []
        self.stderr = stderr.splitlines() if stderr else []

    def __str__(self):
        return f"Logs(stdout={self.stdout}, stderr={self.stderr})"

    def json(self):
        return {
            'stdout': self.stdout,
            'stderr': self.stderr
        }

class Error:
    def __init__(self, name, value, traceback):
        self.name = name
        self.value = value
        self.traceback = traceback.splitlines() if traceback else []

    def __str__(self):
        return f"Error(name={self.name}, value={self.value}, traceback={self.traceback})"

    def json(self):
        return {
            'name': self.name,
            'value': self.value,
            'traceback': self.traceback
        }