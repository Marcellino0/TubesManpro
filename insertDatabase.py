import sys
import pyodbc as odbc
import random
import config

conn_string = f"""
    Driver={{{config.DRIVER_NAME}}};
    Server={config.SERVER_NAME};
    Database={config.DATABASE_NAME};
    Trust_Connection=yes;
"""

try:
    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
except Exception as e:
    print(e)
    print('Task is terminated')
    sys.exit()

# method Pelanggan
def customer():
    try:
        # Joining the Transaksi and MesinCuci tables
        query = """
            SELECT MesinCuci.Nama_Mesin_Cuci, MesinCuci.Merek, MesinCuci.Tarif, MesinCuci.Status
            FROM MesinCuci
        """
        cursor.execute(query)
        transaction_details = cursor.fetchall()

        if transaction_details:
            print("Daftar Mesin Cuci:")
            for detail in transaction_details:
                nama_mesin_cuci, merek, tarif, status = detail  # Ambil semua nilai dari detail
                # Assuming the rate is per 15 minutes
                total_biaya = tarif * random.randint(1, 4)  # Randomize biaya
                status_message = "Unavailable" if status == 1 else "Available"  # Ubah pesan status
                print(f"Nama Mesin Cuci: {nama_mesin_cuci}, Merek: {merek}, Tarif: {tarif:.0f}, Total Biaya: {total_biaya:.0f}, Status: {status_message}")
                
        else:
            print("Tidak ada detail transaksi yang ditemukan.")
    except Exception as e:
        print("Error in fetching transaction details:", e)


def login():
    username = input("Masukkan Username: ")
    password = input("Masukkan Password: ")
    
    try:
        cursor.execute("SELECT ID_Pegawai, Nama_Pegawai FROM Pegawai WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchone()
        if result:
            ID_Pegawai, Nama_Pegawai = result
            cursor.execute("INSERT INTO Session (ID_Pegawai, Status) VALUES (?, ?)", (ID_Pegawai, 'Masuk'))
            conn.commit()
            print(f"Login berhasil")
            return ID_Pegawai
        else:
            print("Username atau Password salah")
            return None
    except Exception as e:
        print(e)
        return None

def logout(ID_Pegawai):
    try:
        cursor.execute("UPDATE Session SET Status = ? WHERE ID_Pegawai = ? AND Status = ?", ('Keluar', ID_Pegawai, 'Masuk'))
        conn.commit()
        print("Logout berhasil.")
    except Exception as e:
        print(e)

def delete_data(table_name, record_id):
    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE ID_{table_name.split()[0]} = ?", (record_id,))
        conn.commit()
        print("Data berhasil dihapus.")
    except Exception as e:
        cursor.rollback()
        print(f"Error saat menghapus data: {e}")

def update_data(table_name, record_id, column_name, new_value):
    try:
        cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE ID_{table_name.split()[0]} = ?", (new_value, record_id))
        conn.commit()
        print("Data berhasil diperbarui.")
    except Exception as e:
        cursor.rollback()
        print(f"Error saat memperbarui data: {e}")

current_user = None


while True:
    if current_user is None:
        print("1. Pelanggan")
        print("2. Login")
        print("3. Keluar")
    else:
        print("1. Logout")
        print("2. Tambah")
        print("3. Delete")
        print("4. Update")
        print("5. Transaksi")
        

    
    pilihan = input("Masukkan Pilihan: ")
    
    if current_user is None:
        if pilihan == "1":
            customer()
        if pilihan == "2":
            current_user = login()
        elif pilihan == "3":
            break
        
    else:
        if pilihan == "1":
            logout(current_user)
            current_user = None
            
        elif pilihan == "2": #Tambah Data
            print("Pilihan Tabel:")
            print("1. Pegawai")
            print("2. Pelanggan")
            print("3. Mesin Cuci")
            print("4. Transaksi")
            tabel_pilihan = input("Pilih Tabel: ")
            if tabel_pilihan == "1":
                IDPegawai = input("Masukkan ID Pegawai: ")
                NamaPegawai = input("Masukkan Nama Pegawai: ")
                Username = input("Masukkan Username: ")
                Password = input("Masukkan Password: ")

                records = [
                    [IDPegawai, NamaPegawai, Username, Password]
                ]

                insert_statement = """
                    INSERT INTO Pegawai (ID_Pegawai, Nama_Pegawai, Username, Password)
                    VALUES (?,?,?,?)
                """
                try:
                    for record in records:
                        cursor.execute(insert_statement, record)
                    conn.commit()
                    print('Record berhasil ditambahkan.')
                except Exception as e:
                    cursor.rollback()
                    print(e)

            elif tabel_pilihan == "2":
                IDPelanggan = input("Masukkan ID Pelanggan: ")
                Nama = input("Masukkan Nama Pelanggan: ")
                NomorTelepon = input("Masukkan Nomor Telepon Pelanggan: ")
                Email = input("Masukkan Email Pelanggan: ")
                Alamat = input("Masukkan Alamat Pelanggan: ")
                IDKelurahan = input("Masukkan ID Kelurahan: ")

                records = [
                    [IDPelanggan, Nama, NomorTelepon, Email, Alamat, IDKelurahan]
                ]

                insert_statement = """
                    INSERT INTO Pelanggan (ID_Pelanggan, Nama_Pelanggan, Nomor_Telepon, Email, Alamat, ID_Kelurahan)
                    VALUES (?,?,?,?,?,?)
                """
                try:
                    for record in records:
                        cursor.execute(insert_statement, record)
                    conn.commit()
                    print('Record berhasil ditambahkan.')
                except Exception as e:
                    cursor.rollback()
                    print(e)

            elif tabel_pilihan == "3":
                IDMesinCuci = input("Masukkan ID Mesin Cuci: ")
                NamaMesinCuci = input("Masukkan Nama Mesin Cuci: ")
                Merek = input("Masukkan Merek Mesin Cuci: ")
                Kapasitas = input("Masukkan Kapasitas Mesin Cuci: ")
                if Merek == "LG":
                    Tarif = 5000
                elif Merek == "Samsung":
                    Tarif = 5250
                elif Merek == "Panasonic":
                    Tarif = 4500
                elif Merek == "Sharp":
                    Tarif = 3500
                elif Merek == "Toshiba":
                    Tarif = 3500
                elif Merek == "Electrolux":
                    Tarif = 7500
                elif Merek == "Midea":
                    Tarif = 8000
                elif Merek == "Beko":
                    Tarif = 6000
                elif Merek == "Whirlpool":
                    Tarif = 5000
                elif Merek == "Haier":
                    Tarif = 7000
                Status = input("Masukkan Status Mesin Cuci: ")
                records = [
                    [IDMesinCuci, NamaMesinCuci, Merek, Kapasitas, Tarif,Status]
                ]

                insert_statement = """
                    INSERT INTO MesinCuci (ID_Mesin_Cuci, Nama_Mesin_Cuci, Merek, Kapasitas, Tarif,Status)
                    VALUES (?,?,?,?,?,?)
                """
                try:
                    for record in records:
                        cursor.execute(insert_statement, record)
                    conn.commit()
                    print('Record berhasil ditambahkan.')
                except Exception as e:
                    cursor.rollback()
                    print(e)
            elif tabel_pilihan == "4":
                IDTransaksi = input("Masukkan ID Transaksi: ")
                Tanggal = input("Masukkan Tanggal Transaksi (YYYY-MM-DD): ")
                WaktuMulai = input("Masukkan Waktu Mulai (HH:MM): ")
                WaktuSelesai = input("Masukkan Waktu Selesai (HH:MM): ")
                IDMesinCuci = input("Masukkan ID Mesin Cuci: ")
                
                # Fetching the tariff for the given machine ID
                try:
                    cursor.execute("SELECT Tarif FROM MesinCuci WHERE ID_Mesin_Cuci = ?", (IDMesinCuci,))
                    result = cursor.fetchone()
                    if result:
                        Tarif = float(result[0])  # Convert to float
                    else:
                        print("ID Mesin Cuci tidak ditemukan.")
                        continue
                except Exception as e:
                    print(e)
                    continue
                
                # Calculating the total cost
                from datetime import datetime
                time_format = "%H:%M"
                try:
                    WaktuMulai_dt = datetime.strptime(WaktuMulai, time_format)
                    WaktuSelesai_dt = datetime.strptime(WaktuSelesai, time_format)
                    time_diff = (WaktuSelesai_dt - WaktuMulai_dt).total_seconds() / 60  # Convert to minutes
                    TotalBiaya = Tarif * (time_diff / 15)  # Assuming the rate is per 15 minutes
                    TotalBiaya = int(TotalBiaya)
                    print("Rp.",TotalBiaya)
                except Exception as e:
                    print("Error in calculating total cost:", e)
                    continue
                
                
                IDPelanggan = input("Masukkan ID Pelanggan: ")
                
                records = [
                    [IDTransaksi, Tanggal, WaktuMulai, WaktuSelesai, IDMesinCuci,IDPelanggan,TotalBiaya]
                ]

                insert_statement = """
                    INSERT INTO Transaksi (ID_Transaksi, Tanggal_Transaksi, Waktu_Mulai, Waktu_Selesai, ID_Mesin_Cuci, ID_Pelanggan,Total_Biaya)
                    VALUES (?,?,?,?,?,?,?)
                """
                try:
                    for record in records:
                        cursor.execute(insert_statement, record)
                    conn.commit()
                    print('Record berhasil ditambahkan.')
                except Exception as e:
                    cursor.rollback()
                    print(e)
            else:
                    print("Tabel tidak valid.")

        elif pilihan == "6":  # Hapus Data
            print("Pilihan Tabel:")
            print("1. Pegawai")
            print("2. Pelanggan")
            print("3. Mesin Cuci")
            print("4. Transaksi")
            tabel_pilihan = input("Pilih Tabel: ")
            record_id = input("Masukkan ID data yang akan dihapus: ")
            if tabel_pilihan == "1":
                delete_data("Pegawai", record_id)
            elif tabel_pilihan == "2":
                delete_data("Pelanggan", record_id)
            elif tabel_pilihan == "3":
                delete_data("MesinCuci", record_id)
            elif tabel_pilihan == "4":
                delete_data("Transaksi", record_id)
            else:
                print("Tabel tidak valid.")

        elif pilihan == "7":  # Perbarui Data
            print("Pilihan Tabel:")
            print("1. Pegawai")
            print("2. Pelanggan")
            print("3. Mesin Cuci")
            print("4. Transaksi")
            tabel_pilihan = input("Pilih Tabel: ")
            record_id = input("Masukkan ID data yang akan diperbarui: ")
            column_name = input("Masukkan nama kolom yang akan diperbarui: ")
            new_value = input("Masukkan nilai baru: ")
            if tabel_pilihan == "1":
                update_data("Pegawai", record_id, column_name, new_value)
            elif tabel_pilihan == "2":
                update_data("Pelanggan", record_id, column_name, new_value)
            elif tabel_pilihan == "3":
                update_data("MesinCuci", record_id, column_name, new_value)
            elif tabel_pilihan == "4":
                update_data("Transaksi", record_id, column_name, new_value)
            else:
                print("Tabel tidak valid.")
        else:
            print("Pilihan tidak valid")


cursor.close()
conn.close()
