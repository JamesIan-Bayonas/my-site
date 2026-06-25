from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.ai_parser import AIParser
from core.math_engine import MathEngine
from core.archiver import DataArchiver

app = FastAPI(title="EcoRoute-AI Asynchronous Engine API")

# Define the expected JSON body structure for incoming network requests
class DispatchPayload(BaseModel):
    raw_log: str

@app.post("/api/v1/optimize")
async def trigger_automated_dispatch(payload: DispatchPayload):
    """
    Headless Webhook Endpoint.
    Ingests raw data asynchronously, feeds it through the AI + Math pipeline,
    and commits the optimized blueprint to disk automatically.
    """
    if not payload.raw_log.strip():
        raise HTTPException(status_code=400, detail="Payload raw_log cannot be empty.")
    
    try:
        # 1. Pipeline execution
        ai = AIParser(model_name="qwen2.5-coder")
        extracted_nodes = ai.extract_logistics_data(payload.raw_log)
        
        math_engine = MathEngine()
        optimized_manifest, total_cost = math_engine.optimize_route(extracted_nodes)
        
        # 2. Automated background archiving
        archiver = DataArchiver()
        json_path, map_path = archiver.archive_session(optimized_manifest, total_cost)
        
        return {
            "status": "success",
            "computed_distance": total_cost,
            "total_nodes_processed": len(extracted_nodes),
            "saved_assets": {
                "interactive_map": map_path
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Asynchronous pipeline failure: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Boot up the server locally on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)