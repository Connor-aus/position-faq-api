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
    from src.api.position_details_model import PositionDetailsRequest
    from src.database.file_db import get_positions_by_company_id, get_all_position_versions, get_position_data, save_position_data

    app = FastAPI(
        title="Position FAQ API",
        json_encoder=json.JSONEncoder,
        default_response_class=JSONResponse
    )

    # Configure CORS
    origins = ["*"]  # Allow all origins for local development
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add middleware to ensure proper JSON encoding
    @app.middleware("http")
    async def ensure_proper_encoding(request: Request, call_next):
        response = await call_next(request)
        if isinstance(response, JSONResponse):
            response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    @app.get("/")
    async def root():
        return JSONResponse(
            status_code=200,
            content={"message": "Welcome to Position FAQ API."},
            media_type="application/json; charset=utf-8"
        )
        
    @app.post("/v1/chatRequest")
    async def chat_request(chat_request: ChatRequest):
        log.info(f"Received chat request for position ID: {chat_request.positionId}")
        try:
            result = handle_workflow_request(chat_request.question, chat_request.positionId)
            
            if result["success"]:
                return JSONResponse(
                    status_code=200,
                    content={"response": result["response"]},
                    media_type="application/json; charset=utf-8"
                )
            else:
                return JSONResponse(
                    status_code=400 if "validation" in result.get("error", "").lower() else 500,
                    content={"error": result["error"]},
                    media_type="application/json; charset=utf-8"
                )
        except Exception as e:
            log.exception("Unhandled exception in chat request endpoint: %s", str(e))
            return JSONResponse(
                status_code=500, 
                content={"error": "An unexpected error occurred. Please try again later."},
                media_type="application/json; charset=utf-8"
            )
            
    @app.get("/v1/company/{company_id}/positions")
    async def get_company_positions(company_id: int):
        log.info(f"Received request for positions of company ID: {company_id}")
        try:
            positions = get_positions_by_company_id(company_id)
            
            if positions:
                return JSONResponse(
                    status_code=200,
                    content={"positions": positions},
                    media_type="application/json; charset=utf-8"
                )
            else:
                return JSONResponse(
                    status_code=404,
                    content={"error": f"No positions found for company ID: {company_id}"},
                    media_type="application/json; charset=utf-8"
                )
        except Exception as e:
            log.exception("Unhandled exception in company positions endpoint: %s", str(e))
            return JSONResponse(
                status_code=500,
                content={"error": "An unexpected error occurred. Please try again later."},
                media_type="application/json; charset=utf-8"
            )
            
    @app.get("/v1/position/{position_id}/versions")
    async def get_position_versions(position_id: int):
        log.info(f"Received request for all versions of position ID: {position_id}")
        try:
            versions = get_all_position_versions(position_id)
            
            if versions:
                return JSONResponse(
                    status_code=200,
                    content={"versions": versions},
                    media_type="application/json; charset=utf-8"
                )
            else:
                return JSONResponse(
                    status_code=404,
                    content={"error": f"No versions found for position ID: {position_id}"},
                    media_type="application/json; charset=utf-8"
                )
        except Exception as e:
            log.exception("Unhandled exception in position versions endpoint: %s", str(e))
            return JSONResponse(
                status_code=500,
                content={"error": "An unexpected error occurred. Please try again later."},
                media_type="application/json; charset=utf-8"
            )

    @app.put("/v1/position/{position_id}/details")
    async def update_position_details(position_id: int, details: PositionDetailsRequest):
        log.info(f"Received request to update details for position ID: {position_id}")
        try:
            # Get the current position data
            current_data = get_position_data(position_id)
            
            if not current_data:
                return JSONResponse(
                    status_code=404,
                    content={"error": f"Position not found with ID: {position_id}"},
                    media_type="application/json; charset=utf-8"
                )
            
            # Create a new version with updated data
            new_data = current_data.copy()
            
            # Update position details
            if details.position:
                new_data["position"] = details.position
                # Ensure position ID is preserved
                new_data["position"]["id"] = position_id
            
            # Update FAQs if provided
            if details.positionFAQs:
                new_data["positionFAQs"] = details.positionFAQs
                # Ensure position ID is set for all FAQs
                for faq in new_data["positionFAQs"]:
                    faq["positionId"] = position_id
            
            # Update position info if provided
            if details.positionInfo:
                new_data["positionInfo"] = details.positionInfo
                # Ensure position ID is set for all info items
                for info in new_data["positionInfo"]:
                    info["positionId"] = position_id
            
            # Save the updated position data
            success, saved_id, version = save_position_data(new_data, position_id)
            
            if success:
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": f"Position details updated successfully",
                        "positionId": saved_id,
                        "version": version
                    },
                    media_type="application/json; charset=utf-8"
                )
            else:
                return JSONResponse(
                    status_code=500,
                    content={"error": "Failed to save position details"},
                    media_type="application/json; charset=utf-8"
                )
        except Exception as e:
            log.exception("Unhandled exception in update position details endpoint: %s", str(e))
            return JSONResponse(
                status_code=500,
                content={"error": "An unexpected error occurred. Please try again later."},
                media_type="application/json; charset=utf-8"
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