import psycopg2
from datetime import datetime

# QuestDB connection details
QUESTDB_HOST = "localhost"
QUESTDB_PORT = 8812
QUESTDB_USER = "admin"
QUESTDB_PASSWORD = "quest"
QUESTDB_DBNAME = "qdb"

MAX_ROWS = 200

# --- Database Connection Utility ---

def get_connection():
    return psycopg2.connect(
        host=QUESTDB_HOST,
        port=QUESTDB_PORT,
        user=QUESTDB_USER,
        password=QUESTDB_PASSWORD,
        dbname=QUESTDB_DBNAME
    )

# --- Table Utilities ---
def ensure_device_table(device_id: str):
    table_name = device_id
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    timestamp TIMESTAMP,
                    temperature DOUBLE,
                    humidity DOUBLE
                ) timestamp(timestamp);
            """)
            conn.commit()

def clear_if_exceeds(device_id: str):
    table_name = device_id
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cur.fetchone()[0]

            if row_count > MAX_ROWS:
                # Truncate the table (QuestDB supports TRUNCATE)
                cur.execute(f"TRUNCATE TABLE {table_name};")
                conn.commit()

# --- Core Data Functions ---

def save_sensor_data(device_id: str, temperature: float, humidity: float):
    table_name = device_id
    ensure_device_table(device_id)
    timestamp = datetime.now().isoformat()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {table_name} (timestamp, temperature, humidity) VALUES (%s, %s, %s);",
                (timestamp, temperature, humidity)
            )
            conn.commit()

    clear_if_exceeds(device_id)

    return {
        "device_id": device_id,
        "temperature": temperature,
        "humidity": humidity,
        "last_updated": timestamp
    }

def get_latest_data(device_id: str):
    table_name = device_id
    ensure_device_table(device_id)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT timestamp, temperature, humidity
                FROM {table_name}
                ORDER BY timestamp DESC
                LIMIT 1;
            """)
            result = cur.fetchone()

    if not result:
        return {"message": f"No data available for {device_id}"}

    timestamp, temperature, humidity = result
    return {
        "device_id": device_id,
        "temperature": temperature,
        "humidity": humidity,
        "last_updated": timestamp.isoformat()
    }

def get_recent_sensor_data(device_id: str, n: int = 10):
    table_name = device_id
    ensure_device_table(device_id)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT timestamp, temperature, humidity
                FROM {table_name}
                ORDER BY timestamp DESC
                LIMIT %s;
            """, (n,))
            results = cur.fetchall()

    if not results:
        return {"message": f"No data available for {device_id}"}

    timestamps, temperatures, humidities = [], [], []
    for ts, temp, hum in reversed(results):
        timestamps.append(ts.isoformat())
        temperatures.append(temp)
        humidities.append(hum)

    return {
        "device_id": device_id,
        "temperatures": temperatures,
        "humidities": humidities,
        "timestamps": timestamps
    }
