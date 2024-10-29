from pbox import CodeSandBox
from pbox import CodeSandBoxManager

code_sandbox = CodeSandBox()
code_sandbox.execute_code("x = 'Hello, PandoraBox!'")
result = code_sandbox.execute_code("print(x)")
print(str(result))



api_key = "pb-WpBpcmRNeBfb3e4569524327B0601167a61C3ea49EkiWRX"
csb_manager = CodeSandBoxManager()
# creqte sandbox
kernel_id = csb_manager.create_sandbox(api_key)

# list sandbox
csb_manager.get_sandbox(api_key)

# execute code
result = csb_manager.execute_code (
    api_key,
    kernel_id,
    "print('Hello, Pandaro Box!')"
)

print(result)

# close sandbox, If you forget, it will automatically close after 6 hours.
csb_manager.close_sandbox(
    api_key,
    kernel_id
)