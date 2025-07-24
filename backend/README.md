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
4. **Install Google Cloud CLI**:
   ```sh
   pip install google-cloud-aiplatform[agent_engines,adk,langchain,ag2,llama_index]>=1.88.0
   ```

5. **Autheticate Google Cloud Account**:
   ```sh
   gcloud auth application-default login

   If it doesnt work try the running the below command
   gcloud auth application-default login --scopes=https://www.googleapis.com/auth/cloud-platform
   ```
4. **Run the FastAPI server**:
   ```sh
   uvicorn app.main:app --reload
   ```


- The API will be available at: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs 