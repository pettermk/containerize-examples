import duckdb

if __name__ == '__main__':
    query = """
    CREATE TABLE IF NOT EXISTS projects (
        name VARCHAR,
        low INTEGER,
        medium INTEGER,
        high INTEGER,
        critical INTEGER,
        size INT
    ) 
    """
    conn = duckdb.connect('.duckdb')
    conn.execute(query)

