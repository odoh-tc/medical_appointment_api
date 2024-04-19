import time

from fastapi import Request
from fastapi.responses import JSONResponse

from logger import logger


async def appointment_middleware(request: Request, call_next):
    logger.info("Starting request processing...")
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"Request processing completed. Process time: {process_time}")
        return response
    except Exception as e:
        logger.error("An error occurred while processing the request:", exc_info=True)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
