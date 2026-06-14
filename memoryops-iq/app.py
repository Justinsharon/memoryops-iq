from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from orchestrator import process_incident

app = FastAPI()

# ----------------------------------
# CORS CONFIGURATION
# ----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------
# REQUEST MODEL
# ----------------------------------

class IncidentRequest(BaseModel):
    incident_id: str
    incident_text: str

# ----------------------------------
# HEALTH CHECK
# ----------------------------------

@app.get("/")
def health():

    return {
        "status": "MemoryOps IQ API Running"
    }

# ----------------------------------
# INCIDENT ANALYSIS
# ----------------------------------

@app.post("/incident")
def analyze_incident(
    request: IncidentRequest
):

    #
    # Validate Incident ID
    #

    if not request.incident_id.startswith("INC"):

        return {
            "error":
            "Incident ID must start with INC"
        }

    #
    # Validate Description
    #

    if len(request.incident_text.strip()) == 0:

        return {
            "error":
            "Incident description cannot be empty"
        }

    #
    # Run MemoryOps IQ
    #

    result = process_incident(
        request.incident_id,
        request.incident_text
    )

    return result