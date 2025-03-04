import os
import uvicorn
from main import app
from config.logger import logger  # Import the logger instance instead of file_formatter
from config.configuration import settings

if __name__ == "__main__":
    port = int(settings.PORT)
    
    # Configure uvicorn logging to use our custom logger
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    
    try:
        # # Check database connection before starting server
        # check_connection()
        # logger.info("Database connection established")
        
        # Start server
        logger.info(f"Starting server on port {port}")  # Use logger instead of file_formatter
        uvicorn.run(
            app="server:app",
            host="127.0.0.1",
            port=port,
            reload=os.getenv("ENV") != "production",
            log_config=log_config,
            loop="asyncio"  # Explicitly specify the event loop
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")  # Use logger instead of file_formatter
        exit(1)
