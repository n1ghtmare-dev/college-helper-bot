from services.external_db import ExternalDB
from config import settings



def get_user_group(user_id: int) -> list:
    with ExternalDB(settings.DB_CONFIG) as db:
        result = db.query('SELECT group_id, username FROM all_users WHERE id_user = %s AND group_id IS NOT NULL', (user_id,))
        return result
    
def get_all_groups() -> list:
    with ExternalDB(settings.DB_CONFIG) as db:
        result = db.query('SELECT DISTINCT group_id FROM schedule')
        return result
    
def get_schedule(date: str) -> list:
    with ExternalDB(settings.DB_CONFIG) as db:
        result = db.query("""
			SELECT group_id, time, teacher_id
			FROM schedule
			WHERE lesson_type NOT LIKE %s AND date = %s AND group_id LIKE %s
			ORDER BY time, group_id ASC
		""", ('%Д%', date, 'К%'))
        return result


