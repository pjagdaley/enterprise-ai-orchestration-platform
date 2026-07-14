from app.core.config import settings

print("=" * 60)
print(settings.app_name)
print(settings.app_version)
print(settings.project_id)
print(settings.gemini_model)
print(settings.qdrant_collection)
print("=" * 60)

from app.core.logging.logger import configure_logging, get_logger

configure_logging()

logger = get_logger(__name__)

logger.debug("Debug Message")
logger.info("Information")
logger.warning("Warning")
logger.error("Error")
logger.critical("Critical")