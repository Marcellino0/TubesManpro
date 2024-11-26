import sys
import pyodbc as odbc
import config

conn_string = f"""
    Driver={{{config.DRIVER_NAME}}};
    Server={config.SERVER_NAME};
    Database={config.DATABASE_NAME};
    Trust_Connection=yes;
"""

conn = None
try:
    conn = odbc.connect(conn_string)
except Exception as e:
    print(e)
    print('Task terminated')
    sys.exit()

cursor = conn.cursor()

def insert_record(table_name, record):
    insert_statement = f"""
        INSERT INTO {table_name} VALUES (?, ?, ?, ?)
    """
    try:
        cursor.execute(insert_statement, record)
        print('Record inserted successfully.')
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Failed to insert record: {e}')

def get_table_name():
    while True:
        choice = input("Masukkan jenis data (Pemilik/Pelanggan): ").strip().lower()
        if choice == 'pemilik':
            return 'Pemilik'
        elif choice == 'pelanggan':
            return 'Pelanggan'
        else:
            print('Pilihan tidak valid, coba lagi.')

table_name = get_table_name()

if table_name == 'Pemilik':
    IdPegawai = input("Id Pegawai: ")
    Nama = input("Nama: ")
    Username = input("Username: ")
    Password = input("Password: ")
    record = [IdPegawai, Nama, Username, Password]
    insert_record(table_name, record)
elif table_name == 'Pelanggan':
    IdPelanggan = input("Id Pelanggan: ")
    NomorTelepon = input("Nomor Telepon: ")
    Email = input("Email: ")
    Alamat = input("Alamat: ")
    record = [IdPelanggan, NomorTelepon, Email, Alamat]
    insert_record(table_name, record)

cursor.close()
conn.close()
