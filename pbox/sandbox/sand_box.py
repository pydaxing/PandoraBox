from jupyter_client import KernelManager
from pbox.utils import Result, Logs, Error
import atexit

class CodeSandBox:
    def __init__(self):
        self.km = KernelManager(kernel_name='python3')
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        self.kc.wait_for_ready()
        atexit.register(self.close)

    def execute_code(self, code):
        msg_id = self.kc.execute(code)
        result = self._parse_results(msg_id)
        return result

    def _parse_results(self, msg_id):
        stdout_content, stderr_content, results = "", "", []
        error = None

        while True:
            try:
                msg = self.kc.get_iopub_msg(timeout=3600)
            except Exception as e:
                print(f"Error getting message: {e}")
                break


            if msg['parent_header'].get('msg_id') != msg_id:
                continue  # skip messages not related to our execution

            match msg['msg_type']:
                case 'status' if msg['content']['execution_state'] == 'idle':
                    break
                case 'stream':
                    content = msg['content']['text']
                    if msg['content']['name'] == 'stdout':
                        stdout_content += content
                    else:
                        stderr_content += content
                case 'error':
                    error = Error(
                        name=msg['content']['ename'],
                        value=msg['content']['evalue'],
                        traceback="\n".join(msg['content']['traceback'])
                    )
                case 'execute_result' | 'display_data':
                    data = msg['content']['data']
                    for data_type, data_value in data.items():
                        if data_type == 'text/plain' and '<Figure size' in data_value:
                            continue  # Skip matplotlib size text
                        results.append({"type": data_type, "data": data_value})

        logs = Logs(stdout=stdout_content, stderr=stderr_content)
        result = Result(results=results, logs=logs, error=error)

        return result

    def close(self):
        try:
            if self.kc:
                self.kc.stop_channels()
                self.kc = None
        except Exception as e:
            print(f"Error stopping channels: {e}")


        try:
            if self.km:
                self.km.shutdown_kernel(now=True)
                self.km = None
        except Exception as e:
            print(f"Error shutting down kernel: {e}")

        return None




