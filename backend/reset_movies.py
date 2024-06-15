from app import create_app, db
import os
from sqlalchemy import text # type: ignore
# from app.models import Movie

run_flag = os.getenv("RUN_FLAG")

app = create_app()
app.app_context().push()

def reset_movies_table():
    try:
        db.session.execute(text('TRUNCATE TABLE movies RESTART IDENTITY CASCADE'))
        db.session.commit()
        print("Movies table has been reset.")
    except Exception as e:
        db.session.rollback()
        print(f"Error resetting the movies table: {e}")

if __name__ == "__main__":
    print("run flag = " + str(run_flag))
    if(run_flag == "True"):
        reset_movies_table()