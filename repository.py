from db_config import load_config
from db_connect import db_connect


class TiktokRepository:
    def __init__(self):
        config = load_config()
        conn = db_connect(config)
        conn.autocommit = True
        self.conn = conn

    def close(self):
        self.conn.close()

    def create_videos_table(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
              CREATE TABLE videos (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  video_id TEXT NOT NULL,
                  account_name TEXT,
                  description TEXT,
                  hashtags TEXT,
                  batch_number INT,
                  video_number INT,
                  ia_analysis TEXT,
                  liked BOOLEAN,
                  watch_time TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
              );
          """
            )

    def test_has_data(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM videos")
                result = cur.fetchall()
                print("[INFO] Banco de dados possui dados. Videos ate entao:", result)
                return True
        except:
            return False

    def count(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM videos")
            return cur.fetchone()[0]

    def add_tiktok(
        self,
        video_id,
        description,
        hashtags,
        ia_analysis,
        liked,
        watch_time,
        account_name,
        video_number,
    ):
        with self.conn.cursor() as cur:
            cur.execute("SELECT MAX(batch_number) FROM videos")
            batch_number = cur.fetchone()[0] or 0

            cur.execute(
                "INSERT INTO videos (video_id, description, hashtags, batch_number, ia_analysis, liked, watch_time, account_name, video_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    video_id,
                    description,
                    hashtags,
                    batch_number,
                    ia_analysis,
                    liked,
                    watch_time,
                    account_name,
                    video_number,
                ),
            )

    def get_all(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM videos")
            rows = cur.fetchall()
            return [rows, cur.description]

    def get_by_id(self, video_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM videos WHERE video_id = %s", (video_id,))
            return cur.fetchone()

    def clear_data(self):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM videos")


if __name__ == "__main__":
    from main import export_to_json

    repository = TiktokRepository()
    # repository.clear_data()
    [all_data, desc] = repository.get_all()
    export_to_json(all_data, desc, "data.json")
    repository.close()
