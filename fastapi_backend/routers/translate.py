import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import dependancies
import schemas
from func import translation
from config import LOGGER_NAME

router = APIRouter(prefix="/translate", tags=["translate"])
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.Translation)
def get_translation(
    query: schemas.TranslationQuery, db: Session = Depends(dependancies.get_db)
):
    logger.info("Received translation request")
    results = translation(db, query)
    return results


@router.post("/test", response_model=schemas.Translation)
def get_translation_test(
    query: schemas.TranslationQuery, db: Session = Depends(dependancies.get_db)
):
    logger.info(query)
    logger.info(db.info)
    logger.info("Received test translation request")

    def result(number):
        return {
            "translated_name": f"translated_name{number}",
            "translated_source": f"translated_source{number}",
            "translated_uid": number,
        }

    return {"results": [result(i) for i in range(5)]}
