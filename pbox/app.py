import uvicorn
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, field_validator
import json
import argparse

from .sandbox import CodeSandBoxManager
from .utils import APIKeyManager
from .utils import validate_api_key, validate_kernel_id


app = FastAPI()


@app.on_event("startup")
def context():
    pass


class ExecuteRequest(BaseModel):
    code: str

    @field_validator('code')
    def validate_code(cls, value):
        if value is None or not value.strip():
            print("Invalid code")
            raise ValueError("Invalid code")
        return value

@app.get('/health',
         status_code=200,
         summary="Check the health status of the PandoraBox.",
         operation_id="health",
         responses={
             200: {
                 "description": "The health status of the PandoraBox.",
                 "content": {"text/plain": {"example": "success"}}
             }
         })
def health():
    return 'success'



@app.get('/create',
         status_code=200,
         summary="Create a python sandbox to receive a unique kernel ID, which allows you to execute python code within it.",
         operation_id="create_sandbox",
         responses={
             200: {
                 "description": "The id of the created python sandbox.",
                 "content": {
                     "application/json": {"example": {"kernel_id": "xx-xx-xx-xx"}}
                 }
             },
             400: {"description": "Bad Request - API Key missing or invalid."},
             500: {"description": "Internal Server Error - Failed to create a new sandbox."}
         })
def create_sandbox(api_key: str = Depends(validate_api_key)):
    if not api_key_manager.check_api_key(api_key):
        print("Invalid API_KEY.")
        raise HTTPException(status_code=400, detail="Invalid API_KEY.")

    kernel_id = sandbox_manager.create_sandbox(api_key)
    if kernel_id:
        print(json.dumps({"kernel_id": kernel_id}, ensure_ascii=False, indent=4))
        return {"kernel_id": kernel_id}
    else:
        print(f"Failed to create a new sandbox.")
        raise HTTPException(status_code=500, detail="Failed to create a new sandbox.")

    
    
@app.post('/execute',
          status_code=200,
          summary="Execute Python code and return the results.",
          operation_id="execute_code",
          responses={
              200: {
                  "description": "The result of the python code, contains three parts: results, logs and error",
                  "content": {
                      "application/json": {
                          "example": {
                              "results": [],
                              "logs": {
                                  "stdout": ["Hello, PandoraBox!"],
                                  "stderr": []
                              },
                              "error": None
                          }
                      }
                  }
              },
              400: {"description": "Bad Request - API Key / Kernel ID missing or invalid."},
              500: {"description": "Internal Server Error - Failed to execute code."}
          })
def execute_code(request: ExecuteRequest, api_key: str = Depends(validate_api_key), kernel_id: str = Depends(validate_kernel_id)):
    if not api_key_manager.check_api_key(api_key):
        print("Invalid API_KEY.")
        raise HTTPException(status_code=400, detail="Invalid API_KEY.")

    code = request.code
    execution_result = sandbox_manager.execute_code(api_key, kernel_id, code)
    if not execution_result:
        print(f"Failed to execute code.")
        raise HTTPException(status_code=500, detail="Failed to execute code.")
    elif isinstance(execution_result, str):
        print(execution_result)
        raise HTTPException(status_code=500, detail=execution_result)
    else:
        res = execution_result.json()
        print(json.dumps(res, ensure_ascii=False, indent=4))
        return res
    

    
@app.get('/close',
         status_code=200,
         summary="Close the python sandbox.",
         operation_id="close_sandbox",
         responses={
             200: {
                 "description": "Closing result.",
                 "content": {
                     "application/json": {
                         "example": {
                             "message": "Sandbox closed."
                         }
                     }
                 }
             },
             400: {"description": "Bad Request - API Key / Kernel ID missing or invalid."},
             500: {"description": "Internal Server Error - Failed to close Sandbox."}
         })
def close_sandbox(api_key: str = Depends(validate_api_key), kernel_id: str = Depends(validate_kernel_id)):
    if not api_key_manager.check_api_key(api_key):
        print("Invalid API_KEY.")
        raise HTTPException(status_code=400, detail="Invalid API_KEY.")

    status = sandbox_manager.close_sandbox(api_key, kernel_id)
    if not status:
        print(f"Failed to close Sandbox.")
        raise HTTPException(status_code=500, detail="Failed to close Sandbox.")
    elif isinstance(status, str):
        print(status)
        raise HTTPException(status_code=500, detail=status)
    else:
        print(json.dumps({"message": "Sandbox closed."}, ensure_ascii=False, indent=4))
        return {"message": "Sandbox closed."}

    
    
@app.get('/sandbox',
         status_code=200,
         summary="List all created sandbox's kernels.",
         operation_id="get_sandbox",
         responses={
             200: {
                 "description": "The list of created python sandbox's kernels.",
                 "content": {
                     "application/json": {
                         "example": {
                             "kernel_ids": ["xxx", "xxx", "xxx"]
                         }
                     }
                 }
             },
             400: {"description": "Bad Request - API Key / Kernel ID missing or invalid."},
             500: {"description": "Internal Server Error - Failed to get kernels."}
         })
def get_sandbox(api_key: str = Depends(validate_api_key)):
    if not api_key_manager.check_api_key(api_key):
        print("Invalid API_KEY.")
        raise HTTPException(status_code=400, detail="Invalid API_KEY.")

    kernel_ids = sandbox_manager.get_sandbox(api_key)
    if not kernel_ids:
        print(f"Failed to get kernels.")
        raise HTTPException(status_code=500, detail="Failed to get kernels.")
    elif isinstance(kernel_ids, str):  # 如果返回了错误消息
        print(kernel_ids)
        raise HTTPException(status_code=500, detail=kernel_ids)
    else:
        print(json.dumps({"kernel_ids": kernel_ids}, ensure_ascii=False, indent=4))
        return {"kernel_ids": kernel_ids}


def start(args):
    if args.server in ["0.0.0.0", "127.0.0.1"]:
        args.server = "127.0.0.1"
    docs_url = f"http://{args.server}:{args.port}/docs"
    server_url = f"http://{args.server}:{args.port}/"

    def custom_openapi():
        openapi_schema = get_openapi(
            title="Pandora Box",
            version="1.2.0",  # 修改这里来自定义版本信息
            description="",
            routes=app.routes,
        )
        openapi_schema["servers"] = [
            {
                "url": server_url,
                "description": "Pandora Box server"
            }
        ]
        # openapi_schema["info"]["x-logo"] = {"url": ""}  # 示例：添加自定义 logo
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    print(f"Start Pandora Box Server，Docs: {docs_url}")
    uvicorn.run(app, host=args.server, port=args.port)


# 创建自定义 OpenAPI 函数

def main():
    global sandbox_manager, api_key_manager
    sandbox_manager = CodeSandBoxManager()
    api_key_manager = APIKeyManager()

    parser = argparse.ArgumentParser(prog="pbox")
    subparsers = parser.add_subparsers(dest='command')

    # 添加子命令 start
    parser_start = subparsers.add_parser('s', help='Start Pandora Box Server')
    parser_start.add_argument("--server", type=str, default="0.0.0.0", required=False, help="Server address")
    parser_start.add_argument("--port", type=int, default=9501, required=False, help="Port")
    parser_start.set_defaults(func=lambda args: start(args), needs_args=True)

    # 添加子命令 addkey
    parser_addkey = subparsers.add_parser('a', help='Add new API KEY')
    parser_addkey.set_defaults(func=lambda :print(f"{api_key_manager.add_api_key()} created."), needs_args=False)

    # 添加子命令 lookkeys
    parser_keys = subparsers.add_parser('l', help='List all API KEYS')
    parser_keys.set_defaults(func=lambda :print("\n".join(api_key_manager.show_api_keys())), needs_args=False)

    # 添加子命令 lookkeys
    parser_keys = subparsers.add_parser('d', help='Del API KEY')
    parser_keys.add_argument("api_key", help="The API KEY to delete")
    parser_keys.set_defaults(func=lambda args: api_key_manager.del_api_key(args.api_key), needs_args=True)

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