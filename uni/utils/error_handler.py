from fastapi import HTTPException

import logging


logger = logging.getLogger(__name__)


async def handle_exception(db, e, action: str):
    logger.error(f"Error {action}: {str(e)}")
    await db.rollback()
    raise HTTPException(status_code=500, detail=f"Error {action}: {str(e)}")
