from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
from python.email import realtime_reading_emails

print("SYSTEM STARTED...")
background_task = None


app = FastAPI(
    title="Purchase Order Approval System",
    version="1.1.1"
)

@app.get("/")
async def health_check():
    return JSONResponse(content={"status":"API is working"}, status_code=200)


@app.post("/start-email-reading-process")
async def start_email_reading_process():
    global background_task

    if background_task and not background_task.done():
        return {"message": "Task already running"}

    background_task = asyncio.create_task(realtime_reading_emails())
    return {"message": "Background process started"}


@app.post("/stop-email-reading-process")
async def stop_email_reading_process():
    global background_task

    if background_task and not background_task.done():
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            return {"message": "Task cancelled"}

    return {"message": "No running task"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)