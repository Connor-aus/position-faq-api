# src/main.py

import json
import os
import sys
from fastapi import FastAPI, Request, Depends
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
    from src.api.chat_request_model import ChatRequest
    from src.api.company_request_model import CompanyRequest
    from src.api.position_request_model import PositionRequest
    from src.database.file_db import get_positions_by_company_id, get_all_position_versions

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
        return {"message": "Welcome to Position FAQ API."}
        
    @app.post("/v1/chatRequest")
    async def chat_request(chat_request: ChatRequest):
        log.info(f"Received chat request for position ID: {chat_request.positionId}")
        try:
            result = handle_workflow_request(chat_request.question, chat_request.positionId)
            
            if result["success"]:
                return {"response": result["response"]}
            else:
                return JSONResponse(
                    status_code=400 if "validation" in result.get("error", "").lower() else 500,
                    content={"error": result["error"]}
                )
        except Exception as e:
            log.exception("Unhandled exception in chat request endpoint: %s", str(e))
            return JSONResponse(
                status_code=500, 
                content={"error": "An unexpected error occurred. Please try again later."}
            )
            
    @app.get("/v1/company/{company_id}/positions")
    async def get_company_positions(company_id: int):
        log.info(f"Received request for positions of company ID: {company_id}")
        try:
            positions = get_positions_by_company_id(company_id)
            
            if positions:
                return {"positions": positions}
            else:
                return JSONResponse(
                    status_code=404,
                    content={"error": f"No positions found for company ID: {company_id}"}
                )
        except Exception as e:
            log.exception("Unhandled exception in company positions endpoint: %s", str(e))
            return JSONResponse(
                status_code=500,
                content={"error": "An unexpected error occurred. Please try again later."}
            )
            
    @app.get("/v1/position/{position_id}/versions")
    async def get_position_versions(position_id: int):
        log.info(f"Received request for all versions of position ID: {position_id}")
        try:
            versions = get_all_position_versions(position_id)
            
            if versions:
                return {"versions": versions}
            else:
                return JSONResponse(
                    status_code=404,
                    content={"error": f"No versions found for position ID: {position_id}"}
                )
        except Exception as e:
            log.exception("Unhandled exception in position versions endpoint: %s", str(e))
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