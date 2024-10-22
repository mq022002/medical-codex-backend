from sqlalchemy import text
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException

logger = logging.getLogger("translation")


def translate(db: Session, query) -> dict:
    try:
        term = query.translation_query.matching_name.lower()
        target_language = query.target_language

        logger.info(f"Translating '{term}' to '{target_language}'")

        language_columns = {
            "uk": "label_uk",
            "ru": "label_ru",
            "gr": "label_gr",
            "en": "label_en",
        }

        if target_language not in language_columns:
            raise ValueError(f"Invalid target language: {target_language}")

        sql_query = text(
            f"""
            SELECT label_uk, label_ru, label_gr, label_en
            FROM medicines
            WHERE LOWER(label_uk) = :term OR LOWER(label_ru) = :term
                  OR LOWER(label_gr) = :term OR LOWER(label_en) = :term
                  OR alias_list_uk LIKE :like_term OR alias_list_ru LIKE :like_term
                  OR alias_list_gr LIKE :like_term OR alias_list_en LIKE :like_term
        """
        )

        logger.info(f"Executing SQL query: {sql_query}")

        result = db.execute(
            sql_query, {"term": term, "like_term": f"%{term}%"}
        ).fetchone()

        logger.info(f"Query Result: {result}")

        if result:
            translated_term = result[
                list(language_columns.keys()).index(target_language)
            ]
            logger.info(f"Translation found: {translated_term}")
            return {
                "results": [
                    {
                        "translated_name": translated_term,
                        "translated_source": "local_db",
                        "translated_uid": 1,
                    }
                ]
            }
        else:
            logger.info(f"No translation found for term '{term}'.")
            return {"results": []}

    except Exception as e:
        logger.error(f"Error during translation: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")
