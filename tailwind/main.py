from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uuid
import asyncio

from crewai import Crew
from tailwind_agentic.agents import (
    researcher, analyst, risk_officer, portfolio_constructor, validator
)
from tailwind_agentic.tasks import task1, task2, task3, task4, task5

app = FastAPI(title="Tailwind Agentic")

# "template" matches the actual folder name (no trailing s)
templates = Jinja2Templates(directory="template")

# In-memory job store — fine for a single-user demo
# For production: replace with Redis or a database
jobs: dict[str, dict] = {}


class RunRequest(BaseModel):
    topic: str


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/healthz")
async def health_check():
    return {"status": "ok"}


@app.post("/run")
async def run_agent(body: RunRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status":      "running",
        "progress":    5,
        "message":     "Initializing crew…",
        "result":      "",
        "agent_index": 0,
    }
    background_tasks.add_task(run_crew, job_id, body.topic)
    return {"job_id": job_id}


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    return jobs.get(job_id, {"status": "not_found"})


# ── Background worker ─────────────────────────────────────────────────────────
# crew.kickoff() is blocking (sync), so we run it in a thread pool via
# asyncio.to_thread() — this keeps FastAPI responsive while the crew works.

def _run_crew_sync(job_id: str, topic: str) -> None:
    """
    Runs in a background thread. Safe to call synchronous/blocking code here.
    Uses CrewAI's task_callback to update the jobs dict after each task completes,
    so the frontend shows real, incremental progress.
    """
    # Each entry: (progress %, status message, agent_index for the frontend)
    # Shown AFTER the corresponding task (1-5) finishes, indicating what's next.
    post_task_updates = [
        (20,  "Tailwind Finder identifying catalysts…",     1),
        (40,  "Risk Analyst stress-testing…",                2),
        (60,  "Portfolio Specialist sizing positions…",      3),
        (80,  "Validator running final review…",             4),
        (95,  "Finalizing memo…",                            4),
    ]

    task_counter = {"n": 0}   # mutable container so the closure can increment

    def on_task_complete(output):
        """Called by CrewAI after each task finishes."""
        idx = task_counter["n"]
        if idx < len(post_task_updates):
            progress, message, agent_idx = post_task_updates[idx]
            jobs[job_id].update(
                progress=progress,
                message=message,
                agent_index=agent_idx,
            )
        task_counter["n"] += 1

    try:
        # Initial state — Scout is working
        jobs[job_id].update(progress=10, message="Scout scanning market universe…", agent_index=0)

        crew = Crew(
            agents=[researcher, analyst, risk_officer, portfolio_constructor, validator],
            tasks=[task1, task2, task3, task4, task5],
            verbose=True,
            memory=False,          # Set to True only after adding a vector store
            task_callback=on_task_complete,
        )

        # This is the long-running call — can take 2-5 minutes
        result = crew.kickoff(inputs={"topic": topic})

        jobs[job_id].update(
            status="completed",
            progress=100,
            message="✅ Mogul Approval Memo ready",
            result=str(result),
        )

    except Exception as exc:
        jobs[job_id].update(
            status="failed",
            progress=100,
            message=f"❌ {exc}",
            result=f"**Error**\n\n```\n{exc}\n```",
        )


async def run_crew(job_id: str, topic: str) -> None:
    """Async wrapper — hands off blocking work to a thread pool."""
    await asyncio.to_thread(_run_crew_sync, job_id, topic)

if __name__ == "__main__":
    import uvicorn
    import os
    # Render and other cloud providers inject a dynamic $PORT environment variable.
    # We MUST listen to 0.0.0.0 and capture that dynamic port for the web service to route correctly.
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)