from services.external_db import ExternalDB
from config import settings



def get_user_group(user_id: int) -> list:
    with ExternalDB(settings.DB_CONFIG) as db:
        result = db.query('SELECT group_id, username FROM all_users WHERE id_user = %s AND group_id IS NOT NULL', (user_id,))
        return result

