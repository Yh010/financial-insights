# FastAPI Backend

## Setup Instructions

1. **Clone the repository** (if you haven't already):
   ```sh
   git clone <your-repo-url>
   cd financial/backend
   ```

2. **Create and activate a virtual environment**:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # Or, on Unix/MacOS:
   # source venv/bin/activate
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**:
   ```sh
   uvicorn app.main:app --reload
   ```

- The API will be available at: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs 