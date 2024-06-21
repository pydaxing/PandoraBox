import uvicorn
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, field_validator
import json
import argparse

from .sandbox import CodeSandBoxManager
from .utils import validate_api_key, validate_kernel_id
from .utils import new_api_key, look_api_key


app = FastAPI()
# 创建自定义 OpenAPI 函数
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Pandora Box",
        version="1.0.0",  # 修改这里来自定义版本信息
        description="",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {"url": ""}  # 示例：添加自定义 logo
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi


@app.on_event("startup")
def context():
    global sandbox_manager
    sandbox_manager = CodeSandBoxManager()

class ExecuteRequest(BaseModel):
    code: str

    @field_validator('code')
    def validate_code(cls, value):
        if value is None or not value.strip():
            print("Invalid code")
            raise ValueError("Invalid code")
        return value

@app.get('/health', status_code=200)
def health():
    return 'success'



@app.get('/create', status_code=200)
def create_sandbox(api_key: str = Depends(validate_api_key)):        
    kernel_id = sandbox_manager.create_sandbox(api_key)
    if kernel_id:
        print(json.dumps({"api_key": api_key, "kernel_id": kernel_id}, ensure_ascii=False, indent=4))
        return {"kernel_id": kernel_id}
    else:
        print(f"Failed to create a new sandbox. API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail="Failed to create a new sandbox.")

    
    
@app.post('/execute', status_code=200)
def execute_code(request: ExecuteRequest, api_key: str = Depends(validate_api_key), kernel_id: str = Depends(validate_kernel_id)):
    code = request.code
    execution_result = sandbox_manager.execute_code(api_key, kernel_id, code)
    if not execution_result:
        print(f"Failed to execute code. API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail="Failed to execute code.")
    elif isinstance(execution_result, str):
        print(execution_result + f" API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail=execution_result)
    else:
        res = execution_result.json()
        res["API_KEY"] = api_key
        print(json.dumps(res, ensure_ascii=False, indent=4))
        return res
    

    
@app.get('/close', status_code=200)
def close_sandbox(api_key: str = Depends(validate_api_key), kernel_id: str = Depends(validate_kernel_id)):    
    status = sandbox_manager.close_sandbox(api_key, kernel_id)
    if not status:
        print(f"Failed to close Sandbox. API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail="Failed to close Sandbox.")
    elif isinstance(status, str):
        print(status + f" API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail=status)
    else:
        print(json.dumps({"message": "Sandbox closed.", "api_key": api_key}, ensure_ascii=False, indent=4))
        return {"message": "Sandbox closed."}

    
    
@app.get('/kernels', status_code=200)
def get_kernel_ids(api_key: str = Depends(validate_api_key)):
    kernel_ids = sandbox_manager.kernels(api_key)
    if not kernel_ids:
        print(f"Failed to get kernels. API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail="Failed to get kernels.")
    elif isinstance(kernel_ids, str):  # 如果返回了错误消息
        print(kernel_ids + f" API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail=kernel_ids)
    else:
        print(json.dumps({"kernel_ids": kernel_ids, "api_key": api_key}, ensure_ascii=False, indent=4))
        return {"kernel_ids": kernel_ids}


def start(args):
    if args.server in ["0.0.0.0", "127.0.0.1"]:
        docs_url = f"http://127.0.0.1:{args.port}/docs"
    else:
        docs_url = f"http://{args.server}:{args.port}/docs"
    print(f"Start Pandora Box Server，Docs: {docs_url}")
    uvicorn.run(app, host=args.server, port=args.port)

def main():
    parser = argparse.ArgumentParser(prog="pbox")
    subparsers = parser.add_subparsers(dest='command')

    # 添加子命令 start
    parser_start = subparsers.add_parser('s', help='Start Pandora Box Server')
    parser_start.add_argument("--server", type=str, default="0.0.0.0", required=False, help="Server address")
    parser_start.add_argument("--port", type=int, default=9501, required=False, help="Port")
    parser_start.set_defaults(func=lambda args: start(args), needs_args=True)

    # 添加子命令 addkey
    parser_addkey = subparsers.add_parser('a', help='Add a new API KEY')
    parser_addkey.set_defaults(func=new_api_key, needs_args=False)

    # 添加子命令 keys
    parser_keys = subparsers.add_parser('k', help='List all API KEYS')
    parser_keys.set_defaults(func=look_api_key, needs_args=False)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        if getattr(args, 'needs_args', False):
            args.func(args)
        else:
            args.func()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()