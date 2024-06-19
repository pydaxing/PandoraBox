import uvicorn
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, validator
import json

from sandbox import CodeSandBoxManager
from utils import validate_api_key, validate_kernel_id
from utils import Logger

logger = Logger()



app = FastAPI()
# 创建自定义 OpenAPI 函数
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Python Box",
        version="1.0",  # 修改这里来自定义版本信息
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
    
    @validator('code')
    def validate_code(cls, value):
        if value is None or not value.strip():
            logger.error("Invalid code")
            raise ValueError("Invalid code")
        return value

    
    
@app.get('/health', status_code=200)
def health():
    return 'success'



@app.get('/create', status_code=200)
def create_sandbox(api_key: str = Depends(validate_api_key)):        
    kernel_id = sandbox_manager.create_sandbox(api_key)
    if kernel_id:
        logger.info(json.dumps({"api_key": api_key, "kernel_id": kernel_id}, ensure_ascii=False, indent=4))
        return {"kernel_id": kernel_id}
    else:
        logger.error(f"Failed to create a new sandbox. API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail="Failed to create a new sandbox.")

    
    
@app.post('/execute', status_code=200)
def execute_code(request: ExecuteRequest, api_key: str = Depends(validate_api_key), kernel_id: str = Depends(validate_kernel_id)):
    code = request.code
    execution_result = sandbox_manager.execute_code(api_key, kernel_id, code)
    if not execution_result:
        logger.error(f"Failed to execute code. API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail="Failed to execute code.")
    elif isinstance(execution_result, str):
        logger.error(execution_result + f" API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail=execution_result)
    else:
        res = execution_result.json()
        res["API_KEY"] = api_key
        logger.info(json.dumps(res, ensure_ascii=False, indent=4))
        return {"result": res}
    

    
@app.get('/close', status_code=200)
def close_sandbox(api_key: str = Depends(validate_api_key), kernel_id: str = Depends(validate_kernel_id)):    
    status = sandbox_manager.close_sandbox(api_key, kernel_id)
    if not status:
        logger.error(f"Failed to close Sandbox. API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail="Failed to close Sandbox.")
    elif isinstance(status, str):
        logger.error(status + f" API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail=status)
    else:
        logger.info(json.dumps({"message": "Sandbox closed.", "api_key": api_key}, ensure_ascii=False, indent=4))
        return {"message": "Sandbox closed."}

    
    
@app.get('/kernels', status_code=200)
def get_kernel_ids(api_key: str = Depends(validate_api_key)):
    kernel_ids = sandbox_manager.get_kernel_ids_by_api_key(api_key)
    if not kernel_ids:
        logger.error(f"Failed to get kernels. API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail="Failed to get kernels.")
    elif isinstance(kernel_ids, str):  # 如果返回了错误消息
        logger.error(kernel_ids + f" API_KEY: {api_key}")
        raise HTTPException(status_code=500, detail=kernel_ids)
    else:
        logger.info(json.dumps({"kernel_ids": kernel_ids, "api_key": api_key}, ensure_ascii=False, indent=4))
        return {"kernel_ids": kernel_ids}

    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)