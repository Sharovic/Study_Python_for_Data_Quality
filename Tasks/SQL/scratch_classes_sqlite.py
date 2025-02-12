class DatabaseManager:
    def __init__(self):
        self.conn_str = (
            "Driver=SQLite3 ODBC Driver;"
            "Database=content_db.sqlite;"
        )
        self.create_tables()

    def create_tables(self):
        """Create necessary tables if they don't exist"""
        with self.connect() as conn:
            cursor = conn.cursor()
            
            # Create News table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    city TEXT NOT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    content_hash TEXT NOT NULL UNIQUE
                )
            """)
            
            # Create Ads table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    expiration_date DATE NOT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    content_hash TEXT NOT NULL UNIQUE
                )
            """)
            
            # Create Jokes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jokes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    funny_rating INTEGER NOT NULL CHECK (funny_rating BETWEEN 1 AND 10),
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    content_hash TEXT NOT NULL UNIQUE
                )
            """)
            
            conn.commit()

    def generate_content_hash(self, content):
        """Generate hash from content only"""
        return hashlib.md5(content.lower().strip().encode()).hexdigest()

    def is_duplicate(self, content, table_name):
        """Generic duplicate check for any table"""
        content_hash = self.generate_content_hash(content)
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id FROM {table_name} WHERE content_hash = ?", 
                         (content_hash,))
            return cursor.fetchone() is not None

    def save_news(self, news_content):
        """Save news content to database"""
        if self.is_duplicate(news_content.text, 'news'):
            raise ValueError("This content already exists in the database")
        
        content_hash = self.generate_content_hash(news_content.text)
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO news (content, city, created_at, content_hash) 
                   VALUES (?, ?, ?, ?)""",
                (news_content.text, news_content.city, 
                 news_content.timestamp, content_hash)
            )
            conn.commit()

    def save_ad(self, ad_content):
        """Save ad content to database"""
        if self.is_duplicate(ad_content.text, 'ads'):
            raise ValueError("This content already exists in the database")
        
        content_hash = self.generate_content_hash(ad_content.text)
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO ads (content, expiration_date, created_at, content_hash) 
                   VALUES (?, ?, ?, ?)""",
                (ad_content.text, ad_content.expiration_date, 
                 ad_content.timestamp, content_hash)
            )
            conn.commit()

    def save_joke(self, joke_content):
        """Save joke content to database"""
        if self.is_duplicate(joke_content.text, 'jokes'):
            raise ValueError("This content already exists in the database")
        
        content_hash = self.generate_content_hash(joke_content.text)
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO jokes (content, funny_rating, created_at, content_hash) 
                   VALUES (?, ?, ?, ?)""",
                (joke_content.text, joke_content.funny_rating, 
                 joke_content.timestamp, content_hash)
            )
            conn.commit()