from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

import pandas as pd
from services.data_processor import DataProcessor
from services.visualizer import DataVisualizer
from services.chatbot import DataChatbot
import json
import io
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Data Analyzer API")
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://datanalyzer.netlify.app"
]
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_processor = DataProcessor()
data_visualizer = DataVisualizer()
data_chatbot = DataChatbot()

# Store the current DataFrame in memory (in production, use a proper database)
current_df = None
current_summary = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    """Upload and process the Excel file"""
    global current_df, current_summary
    try:
        contents = await file.read()
        
        # Get file extension from filename
        _, file_extension = os.path.splitext(file.filename)
        file_extension = file_extension.lower()

        if file_extension == '.csv':
            current_df = pd.read_csv(io.BytesIO(contents))
        elif file_extension in ['.xls', '.xlsx']:
            current_df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file_extension}. Please upload a CSV or Excel file."
            )

        current_summary = None  # Reset summary when new data is uploaded
        return {"message": "Data uploaded successfully"}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/generate-summary")
async def generate_summary():
    """Generate summary of the uploaded dataset"""
    global current_summary
    if current_df is None:
        raise HTTPException(status_code=400, detail="Please upload a dataset first")
    
    try:
        if current_summary is None:
            current_summary = data_processor.generate_summary(current_df)
        return current_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/visualize-data")
async def visualize_data():
    """Generate visualizations for the uploaded dataset"""
    global current_summary
    if current_df is None:
        raise HTTPException(status_code=400, detail="Please upload a dataset first")
    
    try:
        # Use existing summary if available, otherwise generate new one
        if current_summary is None:
            current_summary = data_processor.generate_summary(current_df)
        
        # Ensure important_cols exists in the summary
        if not hasattr(current_summary, 'important_cols') or not current_summary.important_cols:
            print("Warning: No important columns found in summary. Using all columns.")
            important_cols = current_df.columns.tolist()
        else:
            important_cols = current_summary.important_cols
        
        plots = data_visualizer.create_basic_plots(current_df, important_cols)
        
        # Convert plots to JSON
        plots_json = {}
        for plot_name, plot in plots.items():
            try:
                plots_json[plot_name] = plot.to_json()
            except Exception as plot_error:
                print(f"Error converting plot {plot_name} to JSON: {str(plot_error)}")
                continue
        
        if not plots_json:
            raise HTTPException(status_code=500, detail="Failed to generate any plots")
        
        return plots_json
    except Exception as e:
        print(f"Error in visualize_data: {str(e)}")
        print(f"Current DataFrame shape: {current_df.shape if current_df is not None else 'None'}")
        print(f"Current Summary: {current_summary}")
        raise HTTPException(status_code=500, detail=f"Error generating visualizations: {str(e)}")

@app.post("/generate-response")
async def generate_response(request: Request):
    """Generate streaming response for user queries"""
    if current_df is None:
        raise HTTPException(status_code=400, detail="Please upload a dataset first")
    
    try:
        # Get JSON body
        body = await request.json()
        query = body.get('query')
        
        if not query:
            raise HTTPException(status_code=422, detail="Query parameter is required")
        
        # Setup the chatbot with current data
        try:
            data_chatbot.setup_database(current_df)
            print(f'Chatbot setup complete')
        except Exception as e:
            print(f"Error setting up chatbot: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error setting up chatbot: {str(e)}")
        
        async def generate():
            try:
                response = data_chatbot.chat(query)
                yield f"data: {json.dumps({'response': response})}\n\n"
            except Exception as e:
                print(f"Error generating response: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    except Exception as e:
        print(f"Error in generate_response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn app:app --host 0.0.0.0 --port 8000 --reload --workers 4
