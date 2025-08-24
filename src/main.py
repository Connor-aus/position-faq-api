# src/main.py

import json
import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add the parent directory to sys.path so we can import modules properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()

try:
    from src.utils.logger import log
    from src.handlers.workflow_handler import handle_workflow_request

    app = FastAPI(title="Position FAQ API")

    # Configure CORS
    origins = ["*"]  # Allow all origins for local development
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {"message": "Welcome to Position FAQ API. Use /workflow or /contact endpoints."}

    @app.post("/workflow")
    async def invoke_workflow(request: Request):
        log.info("Received workflow request")
        try:
            body = await request.json()
            input_text = body.get("message", "")
            result = handle_workflow_request(input_text)
            
            if result["success"]:
                return {"response": result["response"]}
            else:
                return JSONResponse(
                    status_code=400 if "validation" in result.get("error", "").lower() else 500,
                    content={"error": result["error"]}
                )
        except Exception as e:
            log.exception("Unhandled exception in workflow endpoint: %s", str(e))
            return JSONResponse(
                status_code=500, 
                content={"error": "An unexpected error occurred. Please try again later."}
            )

except Exception as e:
    import traceback
    print("Fatal error upon startup:", e)
    traceback.print_exc()
    raise

# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)