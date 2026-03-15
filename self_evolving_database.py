import sqlite3
import hashlib

class EvolvingSchema:
    def __init__(self, db_name="angelica_brain.db"):
        self.conn = sqlite3.connect(db_name)
        self._init_meta()

    def _init_meta(self):
        """Initializes the Trustless Schema Log."""
        self.conn.execute("CREATE TABLE IF NOT EXISTS schema_log (version_hash TEXT, timestamp DATETIME)")

    def auto_evolve(self, data_packet: dict, table_name="synthesis_logs"):
        """Detects new keys in XIVX data and auto-updates the relational schema."""
        cursor = self.conn.execute(f"PRAGMA table_info({table_name})")
        existing_columns = {row[1] for row in cursor.fetchall()}
        
        for key in data_packet.keys():
            if key not in existing_columns:
                # Type inference: defaulting to TEXT for safety in void state
                print(f"🧬 Auto-Advancing Schema: Adding column {key} to {table_name}")
                self.conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {key} TEXT")
        
        # Anchor the new schema state
        new_state = hashlib.sha3_256(str(sorted(data_packet.keys())).encode()).hexdigest()
        self.conn.execute("INSERT INTO schema_log VALUES (?, ?)", (new_state, datetime.now()))
        self.conn.commit()
