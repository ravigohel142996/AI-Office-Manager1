"""Data Analytics routes"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
import io
import json
from backend.services.ai_service import ai_service
from backend.models.schemas import ForecastRequest

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and analyze CSV file"""
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Basic analysis
        analysis = {
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "summary_stats": df.describe().to_dict() if not df.empty else {},
            "missing_values": df.isnull().sum().to_dict(),
            "sample_data": df.head(5).to_dict('records')
        }
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

@router.post("/analyze-trends")
async def analyze_trends(data: ForecastRequest):
    """Analyze trends in data"""
    if not data.data or len(data.data) < 2:
        raise HTTPException(status_code=400, detail="Insufficient data for trend analysis")
    
    forecast_result = await ai_service.generate_forecast(data.data)
    
    # Calculate additional metrics
    avg = sum(data.data) / len(data.data)
    max_val = max(data.data)
    min_val = min(data.data)
    volatility = pd.Series(data.data).std()
    
    return {
        "historical_data": data.data,
        "forecast": forecast_result,
        "metrics": {
            "average": round(avg, 2),
            "maximum": round(max_val, 2),
            "minimum": round(min_val, 2),
            "volatility": round(volatility, 2)
        }
    }

@router.post("/generate-insights")
async def generate_insights(data: dict):
    """Generate AI insights from data"""
    prompt = f"Analyze this data and provide key insights:\n\n{json.dumps(data, indent=2)}"
    context = "You are a data analyst. Provide clear, actionable insights from the data."
    
    insights = await ai_service.generate_response(prompt, context)
    return {"insights": insights}

@router.get("/sample-data/{dataset}")
async def get_sample_data(dataset: str):
    """Get sample dataset for testing"""
    if dataset == "sales":
        data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Revenue": [45000, 52000, 48000, 61000, 58000, 67000],
            "Units": [150, 175, 160, 203, 195, 223]
        }
    elif dataset == "performance":
        data = {
            "Employee": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "Tasks_Completed": [45, 38, 52, 41, 48],
            "Productivity": [92, 85, 95, 88, 90]
        }
    elif dataset == "support":
        data = {
            "Date": ["2024-01", "2024-02", "2024-03", "2024-04"],
            "Tickets": [120, 135, 108, 142],
            "Resolved": [115, 128, 102, 135]
        }
    else:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return data
