import psycopg2


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS db_client(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(40) NOT NULL,
                    last_name VARCHAR(40) NOT NULL,
                    email VARCHAR(20) UNIQUE
                    );
            """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS clientphones(
                    id SERIAL PRIMARY KEY,
                    client_id SERIAL NOT NULL REFERENCES db_client(id),
                    phones SERIAL
                    );
            """)
    conn.commit()


def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO db_client(first_name, last_name, email)
            VALUES(%s, %s, %s) RETURNING id;
        """)
    conn.commit()


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clientphones(client_id, phone)
            VALUES(%s, %s) RETURNING id;
        """)
    conn.commit()


def change_client_firstname(conn, id, first_name):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE db_client
            SET first_name = %s
            WHERE id = %s;
        """)
        cur.execute("""
            SELECT * FROM db_client;
        """)
    return cur.fetchall()


def change_client_lastname(conn, id, last_name):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE db_client
            SET last_name = %s
            WHERE id = %s;
        """)
        cur.execute("""
            SELECT * FROM db_client;
        """)
    return cur.fetchall()


def change_client_email(conn, id, email):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE db_client
            SET email = %s
            WHERE id = %s;
        """)
        cur.execute("""
            SELECT * FROM db_client;
        """)
    return cur.fetchall()


def change_client_phone(conn, client_id, phones):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clientphones
            SET phone = %s
            WHERE client_id = %s;
        """)
        cur.execute("""
            SELECT * FROM clientphones;
        """)
    return cur.fetchall()


def delete_phone(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM clientphones
            WHERE id = %s;
        """, (1,))
        cur.execute("""
            SELECT * FROM clientphones;
        """)
    return cur.fetchall()


def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM db_client
            WHERE id = %s;
        """, (1,))
        cur.execute("""
            SELECT * FROM db_client;
        """)
    return cur.fetchall()


def find_client_firstname(conn, first_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM db_client
            JOIN clientphones ON client.id = clientphones.client_id
            WHERE first_name = %s;
        """, (first_name,))
    return cur.fetchone()[0]


def find_client_lastname(conn, last_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM db_client
            JOIN clientphones ON client.id = clientphones.client_id
            WHERE last_name = %s;
        """, (last_name,))
    return cur.fetchone()[0]


def find_client_email(conn, email):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM db_client
            JOIN clientphones ON db_client.id = clientphones.client_id
            WHERE email = %s;
        """, (email,))
    return cur.fetchone()[0]


def find_client_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM phone
            JOIN db_client ON clientphones.client_id = db_client.id
            WHERE phone = %s;
        """, (phone,))
    return cur.fetchone()[0]


with psycopg2.connect(database="db_client", user="postgres", password="7u9I367ty0") as conn:
    create_table(conn)
    add_client(conn, 'Алексей', 'Аристархов', 'alexey@yandex.ru')
    add_client(conn, 'Алёна', 'Михай', 'alenamih@mail.ru')
    add_phone(conn, '1', '89122367891')
    add_phone(conn, '2', '89344359865')
    add_phone(conn, '2', '89233192435')
    change_client_firstname(conn, '1', 'Михаил')
    change_client_lastname(conn, '2', 'Карманова')
    change_client_email(conn, '2', 'alenakar@mail.ru')
    change_client_phone(conn, '1', '89122403892')
    delete_phone(conn, '2')
    delete_client(conn, '2')
    find_client_firstname(conn, 'Алексей')
    find_client_lastname(conn, 'Михай')
    find_client_email(conn, 'alexey@yandex.ru')
    find_client_phone(conn, '89233192435')
    conn.close()
