import json
import logging
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler

# Configure logging to output JSON
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_data)

# Apply JSON formatter to logging
logger = logging.getLogger("scheduler")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log_timestamp():
    """Logs a timestamp in JSON format."""
    log_data = {
        "message": "Cron Job Executed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "success"
    }
    logger.info(log_data)

# APScheduler Setup
scheduler = BackgroundScheduler()
scheduler.add_job(log_timestamp, "interval", hours=6)
