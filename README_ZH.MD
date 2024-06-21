# Pandora Box: A Revolutionary Open-Source Python Environment
![](./logo.jpg)


[中文](./README_ZH.MD) | [English](./README.MD)

在大型语言模型（LLMs）的时代，Pandora Box作为一款开创性的开源Python包浮现，专门旨在赋能开发者和创新者创建基于LLM的应用程序和代理。这一多功能工具旨在提供一个健壯且安全的Python环境，便于无缝集成和执行LLM驱动的项目。Pandora Box完全免费，通过pip install即可轻松部署，旨在彻底改变开发者处理LLM基础开发的方式。

Pandora Box的关键优势：

- **完全开源且免费**：采用Pandora Box，拥抱开放开发精神，提供对其源代码的完全访问权限。这确保了一个协作且不断进化的平台，供从事LLM应用和代理开发的开发者使用，无需任何财务障碍。

- **无缝本地部署**：通过一个简单的pip install命令即可立即开始。Pandora Box的安装便捷性使得开发者能够迅速设置并深入LLM基础项目开发。

- **多功能应用**：无论您是在开发运行Python脚本的LLM基础代理，还是通过HTTP部署复杂的AI服务，Pandora Box都提供了实现您愿景所需的灵活性和工具。

- **高效的环境管理**：以前所未有的便捷性创建、执行和关闭Python环境。Pandora Box简化了开发过程，使开发者能够专注于创新，而不是环境设置和管理。

- **理想的LLM基础代理**：Pandora Box专为满足LLM基础应用开发的需求而量身定制。它提供了一个安全、隔离的环境，用于运行不受信任的代码，确保您的LLM代理能够安全高效地运行。

Pandora Box不仅仅是一个Python包；它是通往LLM基础开发未来的大门。通过提供一个安全、易用且完全开源的解决方案，它使开发者能够探索他们的LLM应用和代理的全部潜力。无论您是在创建一个编码助手、一个AI数据分析师，还是任何其他LLM驱动的工具，Pandora Box都为您提供了创新和卓越的基础。
## 安装
为了确保环境隔离和安全，最好使用`conda`来创建一个独立的虚拟环境。

```commandline
# python >= 3.11
conda create -n pandora-box python=3.11
conda activate pandora-box
pip install PandoraBox
```

## 使用
Pandora Box可以通过两种不同的方式使用：要么通过Python脚本，要么通过HTTP服务，从而满足多种使用场景的需求。

### HTTP 服务
HTTP服务器主要通过`pbox`命令使用，该命令包括创建和查询API密钥，以及启动HTTP服务器。您可以通过使用`pbox -h`查看详细信息。

```commandline
$ pbox -h
```
```commandline
usage: pbox [-h] {s,a,k} ...

positional arguments:
  {s,a,k}
    s         Start Pandora Box Server
    a         Add a new API KEY
    k         List all API KEYS

options:
  -h, --help  show this help message and exit
```

在启动HTTP服务器之前，您需要先使用以下命令创建一个API密钥，该密钥将用于在访问您接下来创建的HTTP服务器时进行身份验证。

```commandline
$ pbox a
```
```text
pb-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

您可以通过上述方法创建多个API密钥。

然后，您可以通过以下命令查看您创建的所有API密钥：
```commandline
$ pbox k
```
```text
API-KEY-1
...
API-KEY-n
```

现在，您可以使用以下命令启动HTTP服务器：
```commandline
$ pbox s
```

默认情况下，服务启动在地址`0.0.0.0`和端口`9501`。您可以在使用`pbox s`命令时，通过传递`server`和`port`参数来指定启动地址和端口。

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

恭喜🎉，您已经启动了HTTP服务器。您可以在http://127.0.0.1:9501/docs查看API文档。

#### 状态检查
您可以使用`curl`来检查http服务器的健康状态：
```commandline
$ curl http://127.0.0.1:9501/health
```
```text
success
```

#### 创建 Python SandBox
您可以按照以下方式创建一个Python沙盒环境：
```commandline
$ curl http://127.0.0.1:9501/create \
-H "API-KEY: your-api-key"
```
```json
{
    "kernel_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

您将收到一个kernel_id，这是Python沙盒的唯一标识符。如果创建后返回了kernel_id，这表明创建成功。

#### 查询 Python SandBox
当前已创建的Python环境可以通过以下方式查询：
```commandline
$ curl http://127.0.0.1:9501/kernels \
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

#### 执行 Python 代码
现在，您可以在这个Python沙盒中执行Python代码：
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

执行Python代码后，返回的结果可能包括以下几个部分：

`results` 包含了base64编码的图像数据，如果您使用matplotlib绘制了图片。

`logs` 包含了执行过程中打印到标准输出(stdout)和标准错误(stderr)的信息。日志的例子包括打印语句、警告、子进程输出等。它包含两个字段：
- `stdout`：字符串列表，每个字符串是打印到标准输出的一行。
- `stderr`：字符串列表，每个字符串是打印到标准错误的一行。

`error` 包含了执行单元格过程中出现的错误信息。它包含三个字段：
- `name`：错误的名称，例如NameError、ValueError等。
- `value`：错误的值，例如'name 'non_existent_variable' is not defined'等。
- `traceback`：错误的追踪信息。

#### 关闭 Python Sandbox
当您不需要使用Python环境时，可以及时关闭它以减少资源浪费。

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

每个内核如果没有手动关闭，将在6小时后自动关闭。这意味着每个内核的最大持续时间是6小时。这样做是为了避免资源浪费。当前版本还不支持持续时间设置。

### Python 脚本中使用
您可以在Python脚本中直接导入pbox包进行使用。如果您不需要任何Python环境管理或API密钥认证功能，您可以直接使用CodeSandBox创建一个Python环境并执行代码。
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

返回的结果是一个`Result`类，您可以使用`str()`查看具体内容。`Result`中包含的`results`是一个列表。`Logs`也是一个类似于`Result`的类，包含两个列表：`stdout`和`stderr`。当代码正常执行时，`error`为`null`；当代码出现错误时，`error`是一个`Error`类，包含三个属性：`name`、`value`和`traceback`。可以使用`.`操作符访问`Result`、`Logs`和`Error`中的值，例如`result.logs.stdout`。

`CodeSandBox`具有记住Python代码上下文的能力，直到它被关闭。
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
如果您不再需要它，可以直接关闭它。

```python
code_sandbox.close()
```

如果您需要API密钥认证机制以及内核在6小时后自动关闭的机制，您可以使用`CodeSandBoxManager`来创建和关闭沙盒以及执行代码。
```python
from pbox import CodeSandBoxManager

csb_manager = CodeSandBoxManager()

# creqte sandbox
kernel_id = csb_manager.create_sandbox("your-api-key")

# list sandbox
csb_manager.kernels("your-api-key")

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

## 贡献
欢迎为这个项目做出贡献。您可以开启一个问题(issue)或提交一个拉取请求(pull request)。

## 联系
您可以通过电子邮件pydaxing@gmail.com与我们联系。