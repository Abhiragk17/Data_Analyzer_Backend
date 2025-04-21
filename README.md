# Data Analyzer API

A powerful FastAPI-based backend service for analyzing and visualizing data, with integrated AI capabilities for data insights and natural language interaction.

## Features

- 📊 Data Analysis and Visualization
- 🤖 AI-powered Data Insights
- 💬 Natural Language Query Interface
- 📈 Interactive Data Visualization
- 🔄 Real-time Data Processing

## Tech Stack

- **Backend Framework**: FastAPI
- **Data Processing**: Pandas
- **AI Integration**: LangChain with Google's Gemini
- **Visualization**: Plotly
- **API Documentation**: Swagger UI / ReDoc

## Prerequisites

- Python 3.8+
- Google API Key for Gemini AI
- Virtual Environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd data-analyzer-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- Main API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Documentation: http://localhost:8000/redoc

## API Endpoints

- `POST /upload-data`: Upload Excel data files
- `GET /generate-summary`: Generate AI-powered data summary
- `GET /visualize-data`: Create interactive visualizations
- `POST /generate-response`: Get AI responses to data queries

## Project Structure

```
backend/
├── app.py                 # Main FastAPI application
├── services/
│   ├── data_processor.py  # Data processing and analysis
│   ├── visualizer.py      # Data visualization
│   └── chatbot.py         # AI chat interface
├── utils/                 # Utility functions
├── requirements.txt       # Project dependencies
└── .env                  # Environment variables
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 