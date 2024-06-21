from jupyter_client import KernelManager
from pbox.utils import Result, Logs, Error

class CodeSandBox:
    def __init__(self):
        self.km = KernelManager(kernel_name='python3')
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        self.kc.wait_for_ready()

    def execute_code(self, code):
        msg_id = self.kc.execute(code)
        stdout_content = ""
        stderr_content = ""
        results = []
        error = None

        while True:
            try:
                msg = self.kc.get_iopub_msg(timeout=60)
            except Exception as e:
                print(f"Error getting message: {e}")
                break

            if msg['parent_header'].get('msg_id') != msg_id:
                continue  # skip messages not related to our execution
            if msg['msg_type'] == 'status' and msg['content']['execution_state'] == 'idle':
                break  # execution is complete
            elif msg['msg_type'] == 'stream':
                if msg['content']['name'] == 'stdout':
                    stdout_content += msg['content']['text']
                else:
                    stderr_content += msg['content']['text']
            elif msg['msg_type'] == 'error':
                error = Error(
                    name=msg['content']['ename'],
                    value=msg['content']['evalue'],
                    traceback="\n".join(msg['content']['traceback'])
                )
            elif msg['msg_type'] in ['execute_result', 'display_data']:
                data = msg['content']['data']
                for data_type, data_value in data.items():
                    if data_type == 'text/plain' and '<Figure size' in data_value:
                        continue  # Skip matplotlib size text
                    results.append({"type": data_type, "data": data_value})

        logs = Logs(stdout=stdout_content, stderr=stderr_content)
        return Result(results=results, logs=logs, error=error)

    def close(self):
        try:
            self.kc.stop_channels()
        except Exception as e:
            print(f"Error stopping channels: {e}")
        try:
            self.km.shutdown_kernel(now=True)
        except Exception as e:
            print(f"Error shutting down kernel: {e}")
        del self.kc
        del self.km
        return None
