# Pandora Box: A Revolutionary Open-Source Python Environment
![](./logo.jpg)

[English](./README.MD) | [中文](./README_ZH.MD)

In the era of Large Language Models (LLMs), Pandora Box emerges as a pioneering open-source Python package, specifically designed to empower developers and innovators in the creation of LLM-based applications and agents. This versatile tool is engineered to provide a robust and secure Python environment, facilitating the seamless integration and execution of LLM-driven projects. Completely free and easily deployable via pip install, Pandora Box is set to revolutionize the way developers approach LLM-based development.

Key Advantages of Pandora Box:

- **Fully Open-Source and Free**: Embrace the open development ethos with Pandora Box, offering complete access to its source code. This ensures a collaborative and evolving platform for developers working on LLM applications and agents, without any financial barriers.

- **Seamless Local Deployment**: Get started instantly with a simple pip install command. Pandora Box's ease of installation on local machines allows developers to quickly set up and dive into LLM-based project development.

- **Versatile Application**: Whether you're developing LLM-based agents that run Python scripts or deploying sophisticated AI services via HTTP, Pandora Box provides the flexibility and tools needed to bring your vision to life.

- **Efficient Environment Management**: Create, execute, and close Python environments with unparalleled ease. Pandora Box streamlines the development process, enabling developers to focus on innovation rather than environment setup and management.

- **Ideal for LLM-Based Agents**: Pandora Box is specifically tailored to meet the needs of LLM-based application development. It offers a secure environment for running python code, ensuring that your LLM agents can operate efficiently.

Pandora Box is not just a Python package; it's a gateway to the future of LLM-based development. By offering a secure, easy-to-use, and completely open-source solution, it enables developers to explore the full potential of their LLM applications and agents. Whether you're creating a coding copilot, an AI data analyst, or any other LLM-powered tool, Pandora Box provides the foundation you need to innovate and excel in the LLM era.

## Installation
To ensure environment isolation and security, it is best to use `conda` to create a separate virtual environment.

```commandline
# python >= 3.11
conda create -n pandora-box python=3.11
conda activate pandora-box
pip install PandoraBox
```

## How to use
Pandora Box can be utilized in two distinct manners: either through Python scripts or via HTTP services, thereby catering to a variety of usage scenarios.

### HTTP Server
The HTTP Server is primarily used with the `pbox` command, which includes the creation and querying of API KEYS, and the starting of the HTTP Server. You can view detailed information by using "pbox -h".

```commandline
$ pbox -h
```
```commandline
usage: pbox [-h] {s,a,l,d} ...

positional arguments:
  {s,a,l,d}
    s         Start Pandora Box Server
    a         Add new API KEY
    l         List all API KEYS
    d         Del API KEY

options:
  -h, --help  show this help message and exit
```

Before starting the HTTP Server, you need to first create an API KEY using the following command, which will be used for authentication when accessing the HTTP Server you create next.

```commandline
$ pbox a
```
```text
pb-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

You can create multiple API KEYS through the above method.

Then, you can view all the API KEYS you have created by following command:
```commandline
$ pbox l
```
```text
API-KEY-1
...
API-KEY-n
```

And, you can delete a api_key by:
```commandline
$ pbox d <your-api-key>
```

Now, you can start the HTTP Server using the this command:
```commandline
$ pbox s
```

By default, the service starts at the address `0.0.0.0` and port `9501`. You can specify the startup address and port by passing the `server` and `port` parameters when using the `pbox s` command.

```commandline
$ pbox s --server x.x.x.x --port xxxx
```

```commandline
$ pbox s -h
```
```commandline
usage: pbox s [-h] [--server SERVER] [--port PORT]

options:
  -h, --help       show this help message and exit
  --server SERVER  Server address
  --port PORT      Port
```

Congratulation🎉, you have launched the HTTP Server. You can view the API documentation at http://127.0.0.1:9501/docs.

#### Health Check
You can use `curl` to check the health status of the http server:
```commandline
$ curl http://127.0.0.1:9501/health
```
```text
success
```

#### Create Python SandBox
You can create a Python sandbox as follows:
```commandline
$ curl http://127.0.0.1:9501/create \
-H "API-KEY: your-api-key"
```
```json
{
    "kernel_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

You will receive a kernel_id, which is the unique identifier for the Python box. If a kernel_id is returned after creation, it indicates that the creation was successful.

#### List Python SandBox
The current Python environments that have been created can be queried in the following way.
```commandline
$ curl http://127.0.0.1:9501/sandbox \
-H "API-KEY: your-api-key"
```
```json
{
  "kernel_ids":[
    "kernel_id_1", 
    "kernel_id_2", 
    "...", 
    "kernel_id_n"]
}
```



#### Execute Python Code
You can now execute Python code in this Python Box：
```commandline
$ curl http://127.0.0.1:9501/execute \
-H "API-KEY: your-api-key" \
-H "Content-Type: application/json; charset=utf-8" \
-H "KERNEL-ID: your-kernel-id" \
-d '{
    "code": "print(\"Hello, Pandora Box!\")"
}'
```
```json
{
  "results": [],
  "logs": {
    "stdout": ["Hello, Pandora Box!"],
    "stderr": []
  },
  "error": null
}
```

`results` has base64 encoded image, if you use matplotlib to plot a picture.

`logs` printed to stdout and stderr during execution. Examples of logs are print statements, warnings, subprocess output, etc. It contains two fields:
- `stdout`: List of strings, each string is a line printed to stdout.
- `stderr`: List of strings, each string is a line printed to stderr.

`error` message, if there was an error during execution of the cell. It contains three fields:

- `name`: Name of the error, e.g. NameError, ValueError, etc.
- `value`: Value of the error, e.g. name 'non_existent_variable' is not defined, etc.
- `traceback`: Traceback of the error.

#### Close Python Sandbox
When you don't need to use the Python environment, you can close it in time to reduce resource waste.

```commandline
$ curl http://127.0.0.1:9501/close \
-H "API-KEY: your-api-key" \
-H "KERNEL-ID: your-kernel-id"
```
```json
{
  "message": "Sandbox Closed."
}
```

Each kernel, if not manually closed, will automatically shut down after 6 hours. This means that the maximum duration for each kernel is 6 hours. This is to avoid wasting resources. The current version does not support duration settings yet.

### Python Script
You can directly import the pbox package in your Python script for use. If you don't need any Python environment management or API KEY authentication features, you can directly use CodeSandBox to create a Python environment and execute the code.
```python
from pbox import CodeSandBox

code_sandbox = CodeSandBox()
result = code_sandbox.execute_code("print('Hello, PandaroBox!')")

print(str(result))
print(result.logs.stdout)
```
```text
Result(results=[], logs=Logs(stdout=['Hello, PandaroBox!'], stderr=[]), error=None)
['Hello, PandaroBox!']
```

The returned result is a `Result` class, which you can view the specific content by using `str()`. The `results` contained within the `Result` is a list. `Logs` is also a class similar to `Result`, containing two lists: `stdout` and `stderr`. The `error` is `null` when the code executes normally, and it is an `Error` class when there is a code error, containing three attributes: `name`, `value`, and `traceback`. The values in `Result`, `Logs`, and `Error` can be accessed using the `.` operator, such as `result.logs.stdout`.

`CodeSandBox` has the ability to remember the context of Python code until it is closed.
```python
from pbox import CodeSandBox

code_sandbox = CodeSandBox()
code_sandbox.execute_code("x = 'Hello, PandoraBox!'")
result = code_sandbox.execute_code("print(x)")

print(str(result))
```
```text
Result(results=[], logs=Logs(stdout=['Hello, PandoraBox!'], stderr=[]), error=None)
```
If you no longer need it, you can directly close it.

```python
code_sandbox.close()
```

If you require an API KEY authentication mechanism and the mechanism for kernels to automatically close after 6 hours, you can use `CodeSandBoxManager` to create and close sandboxes as well as execute code.
```python
from pbox import CodeSandBoxManager

csb_manager = CodeSandBoxManager()

# creqte sandbox
kernel_id = csb_manager.create_sandbox("your-api-key")

# list sandbox
csb_manager.get_sandbox("your-api-key")

# execute code
result = csb_manager.execute_code (
    "your-api-key",
    "your-kernel-id",
    "print('Hello, Pandaro Box!')"
)

# close sandbox, If you forget, it will automatically close after 6 hours.
csb_manager.close_sandbox(
    "your-api-key",
    "your-kernel-id"
)
```

## Contributing
Feel free to contribute to this project. You can open an issue or submit a pull request.

## Contact info
You can contact at pydaxing@gmail.com