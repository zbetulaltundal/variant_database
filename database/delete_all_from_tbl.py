import psycopg2
from common_functions import db_connect
import db_config
import timeit

def delete_all_from_tbl(db_name, tbl_name):
    conn = None
    rows_deleted = 0
    try:
        conn = db_connect(db_name)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(f"DELETE FROM {tbl_name};")
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


t_0 = timeit.default_timer()
n_deleted = delete_all_from_tbl(db_config.CLINVAR_DB_NAME, "INFO")
print(f"{n_deleted} rows deleted from INFO table")
t_1 = timeit.default_timer()

elapsed_time = round((t_1 - t_0) * 10 ** 3, 3)
print(f"elapsed time: {elapsed_time} ms")


