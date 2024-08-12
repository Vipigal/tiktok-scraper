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
      cur.execute("CREATE TABLE videos (video_id INT AUTO_INCREMENT PRIMARY KEY, description TEXT, hashtags TEXT)")

  def test_has_data(self):
    try:
      with self.conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM videos")
        return cur.fetchone()[0] > 0
    except:
      return False
    
  def count(self):
    with self.conn.cursor() as cur:
      cur.execute("SELECT COUNT(*) FROM videos")
      return cur.fetchone()[0]

  def add_tiktok(self, video_id, description, hashtags):
    with self.conn.cursor() as cur:
      cur.execute("INSERT INTO videos (video_id, description, hashtags) VALUES (%s, %s, %s)", (video_id, description, hashtags))

  def get_all(self):
    with self.conn.cursor() as cur:
      cur.execute("SELECT * FROM videos")
      return cur.fetchall()
    
  def get_by_id(self, video_id):
    with self.conn.cursor() as cur:
      cur.execute("SELECT * FROM videos WHERE video_id = %s", (video_id,))
      return cur.fetchone()
