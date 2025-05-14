from college_bot.services.external_db import ExternalDB
import logging

logger = logging.getLogger(__name__)

class GroupCrud:
    def __init__(self, db: ExternalDB):
        self.db = db

    def get_user_group(self, user_id: int) -> list:
        try:
            return self.db.query("""
                            SELECT
                            group_id,
                            username
                            FROM all_users
                            WHERE id_user = %s
                            AND group_id IS NOT NULL""", (user_id,))
        except Exception as e:
            logger.error(f"Error fetch user {e}")

    def get_all_groups(self) -> list:
        try:
            result = self.db.query("""
                                SELECT DISTINCT
                                group_id
                                FROM scheudle
                                """)
            return [{"name": item["group_id"]} for item in result]
        except Exception as e:
            logger.error(f"Error fetch groups {e}")