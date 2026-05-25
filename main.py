import uvicorn
import os
import argparse
from utils.logger import logger

def main():
    parser = argparse.ArgumentParser(description="MiSi Screener AI Trading Platform")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable uvicorn reload")

    args = parser.parse_args()

    logger.info("Initializing MiSi Screener AI Trading Framework...")

    # In a production environment, we might want to pre-load some agents here
    # or perform database migrations.

    logger.info(f"Starting MiSi Terminal on http://{args.host}:{args.port}")

    uvicorn.run(
        "dashboard.backend.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()
