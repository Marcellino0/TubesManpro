from flask import Flask, render_template, request, redirect, url_for
import pyodbc as odbc
import random
from datetime import datetime

app = Flask(__name__)

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-H14LBAC\SQLEXPRESS'
DATABASE_NAME ='ProjectMIBD'

conn_string = f"""
    Driver={{{DRIVER_NAME}}};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trust_Connection=yes;
"""

conn = odbc.connect(conn_string)
cursor = conn.cursor()

# Routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor.execute("SELECT ID_Pegawai, Nama_Pegawai FROM Pegawai WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchone()
        if result:
            return redirect(url_for('dashboard'))
        else:
            error = "Username atau Password salah"
    
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/function_tambah')
def function_tambah():
    return render_template('functionTambah.html')

@app.route('/function_delete')
def function_delete():
    return render_template('functionDelete.html')

@app.route('/function_update')
def function_update():
    return render_template('functionUpdate.html')

@app.route('/pelanggan', methods=['GET'])
def pelanggan():
    query = """
        SELECT Nama_Mesin_Cuci, Merek, Tarif, Status FROM MesinCuci
    """
    cursor.execute(query)
    transaction_details = cursor.fetchall()
    
    mesin_cuci_list = []
    for detail in transaction_details:
        nama_mesin_cuci, merek, tarif, status = detail
        
        status_message = "Unavailable" if status == 1 else "Available"
        mesin_cuci_list.append((nama_mesin_cuci, merek, tarif, status_message))
    
    return render_template('pelanggan.html', mesin_cuci_list=mesin_cuci_list)

@app.route('/laporan_Transaksi', methods=['GET'])
def laporan_Transaksi():
    query = """
            SELECT Pelanggan.Nama_Pelanggan, MesinCuci.Nama_Mesin_Cuci, Transaksi.Tanggal_Transaksi, SUM(Transaksi.Total_Biaya) 
            FROM Pelanggan JOIN Transaksi ON Pelanggan.ID_Pelanggan = Transaksi.ID_Pelanggan
            JOIN MesinCuci ON Transaksi.ID_Mesin_Cuci = MesinCuci.ID_Mesin_Cuci
            GROUP BY Transaksi.Tanggal_Transaksi, Pelanggan.Nama_Pelanggan, MesinCuci.Nama_Mesin_Cuci
        """
    cursor.execute(query)
    list_laporan = cursor.fetchall()
        
    list_Laporan = []
    for detail in list_laporan:
        nama_pelanggan, nama_mesin_cuci, tanggal_transaksi, total_biaya = detail
        list_Laporan.append((nama_pelanggan, nama_mesin_cuci, tanggal_transaksi, total_biaya))
        
    return render_template('functionLaporan.html', list_laporan=list_Laporan)

@app.route('/add_pegawai', methods=['GET', 'POST'])
def add_pegawai():
    if request.method == 'POST':
        NamaPegawai = request.form['NamaPegawai']
        Username = request.form['Username']
        Password = request.form['Password']
        
        # Query untuk memeriksa apakah ID Pegawai sudah ada di database
        check_query = "SELECT * FROM Pegawai WHERE Nama_Pegawai = ?"
        cursor.execute(check_query, (NamaPegawai,))
        existing_pegawai = cursor.fetchone()
        
        if existing_pegawai:
            error = "Nama yang digunakan sudah ada."
            return render_template('add_pegawai.html', error=error)
        else:
            insert_statement = """
            INSERT INTO Pegawai (Nama_Pegawai, Username, Password)
            VALUES (?,?,?)
        """
        try:
            cursor.execute(insert_statement, (NamaPegawai, Username, Password))
            conn.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            conn.rollback()
            return str(e)
    return render_template('add_pegawai.html')

@app.route('/add_pelanggan', methods=['GET', 'POST'])
def add_pelanggan():
    if request.method == 'POST':
        Nama = request.form['Nama']
        NomorTelepon = request.form['NomorTelepon']
        Email = request.form['Email']
        Alamat = request.form['Alamat']
        IDKelurahan = request.form['IDKelurahan']
        
        # Query untuk memeriksa apakah ID Pelanggan sudah ada di database
        check_query = "SELECT * FROM Pelanggan WHERE Nama_Pelanggan = ?"
        cursor.execute(check_query, (Nama,))
        existing_pelanggan = cursor.fetchone()
        
        if existing_pelanggan:
            error = "Nama yang digunakan sudah ada."
            return render_template('add_pelanggan.html', error=error)
        else:
             insert_statement = """
            INSERT INTO Pelanggan (Nama_Pelanggan, Nomor_Telepon, Email, Alamat, ID_Kelurahan)
            VALUES (?,?,?,?,?)
        """
        try:
            cursor.execute(insert_statement, (Nama, NomorTelepon, Email, Alamat, IDKelurahan))
            conn.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            conn.rollback()
            return str(e)
    return render_template('add_pelanggan.html')

@app.route('/add_mesin_cuci', methods=['GET', 'POST'])
def add_mesin_cuci():
    if request.method == 'POST':
        NamaMesinCuci = request.form['NamaMesinCuci']
        Merek = request.form['Merek']
        Kapasitas = request.form['Kapasitas']
        
        Tarif = request.form['Tarif']
        # if Merek == "LG":
        #     Tarif = 5000
        # elif Merek == "Samsung":
        #     Tarif = 5250
        # elif Merek == "Panasonic":
        #     Tarif = 4500
        # elif Merek == "Sharp":
        #     Tarif = 3500
        # elif Merek == "Toshiba":
        #     Tarif = 3500
        # elif Merek == "Electrolux":
        #     Tarif = 7500
        # elif Merek == "Midea":
        #     Tarif = 8000
        # elif Merek == "Beko":
        #     Tarif = 6000
        # elif Merek == "Whirlpool":
        #     Tarif = 5000
        # elif Merek == "Haier":
        #     Tarif = 7000

        Status = request.form['Status']
        
        insert_statement = """
            INSERT INTO MesinCuci (Nama_Mesin_Cuci, Merek, Kapasitas, Tarif, Status)
            VALUES (?,?,?,?,?)
        """
        try:
            cursor.execute(insert_statement, (NamaMesinCuci, Merek, Kapasitas, Tarif, Status))
            conn.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            conn.rollback()
            return str(e)
    return render_template('add_mesin_cuci.html')

@app.route('/add_transaksi', methods=['GET', 'POST'])
def add_transaksi():
    if request.method == 'POST':
        Tanggal = request.form['Tanggal']
        WaktuMulai = request.form['WaktuMulai']
        WaktuSelesai = request.form['WaktuSelesai']
        NamaMesinCuci = request.form['NamaMesinCuci']
        NamaPelanggan = request.form['NamaPelanggan']

        # Mengambil ID Mesin Cuci dari nama mesin cuci
        cursor.execute("SELECT ID_Mesin_Cuci, Tarif, Status FROM MesinCuci WHERE Nama_Mesin_Cuci = ?", (NamaMesinCuci,))
        result = cursor.fetchone()
        if result:
            # Mengambil status dari tabel MesinCuci
            
            IDMesinCuci, Tarif, status_mesin = result
            Tarifs = float(Tarif)
            if status_mesin == 0:  # Jika status mesin adalah 0 (tidak digunakan)
                # Mengambil ID Pelanggan dari nama pelanggan
                cursor.execute("SELECT ID_Pelanggan FROM Pelanggan WHERE Nama_Pelanggan = ?", (NamaPelanggan,))
                existing_pelanggan = cursor.fetchone()
                if existing_pelanggan:
                    IDPelanggan = existing_pelanggan[0]

                    time_format = "%H:%M"
                    try:
                        WaktuMulai_dt = datetime.strptime(WaktuMulai, time_format)
                        WaktuSelesai_dt = datetime.strptime(WaktuSelesai, time_format)
                        time_diff = (WaktuSelesai_dt - WaktuMulai_dt).total_seconds() / 60
                        TotalBiaya = Tarifs * (time_diff / 15)
                        TotalBiayas = int(TotalBiaya)
                    except Exception as e:
                        return str(e)

                    # Memasukkan transaksi ke dalam database
                    insert_statement = """
                        INSERT INTO Transaksi (Tanggal_Transaksi, Waktu_Mulai, Waktu_Selesai, ID_Mesin_Cuci, ID_Pelanggan, Total_Biaya)
                        VALUES (?,?,?,?,?,?)
                    """
                    try:
                        cursor.execute(insert_statement, (Tanggal, WaktuMulai, WaktuSelesai, IDMesinCuci, IDPelanggan, TotalBiayas))
                        # Update status mesin cuci menjadi 1 setelah transaksi berhasil
                        update_status_query = "UPDATE MesinCuci SET Status = 1 WHERE ID_Mesin_Cuci = ?"
                        cursor.execute(update_status_query, (IDMesinCuci,))
                        conn.commit()
                        return redirect(url_for('dashboard'))
                    except Exception as e:
                        conn.rollback()
                        return str(e)
                else:
                    error = "Nama Pelanggan tidak terdaftar."
                    return render_template('add_transaksi.html', error=error)
            else:
                error = "Mesin cuci sedang digunakan."
                return render_template('add_transaksi.html', error=error)
        else:
            error = "Nama Mesin Cuci tidak valid."
            return render_template('add_transaksi.html', error=error)

    return render_template('add_transaksi.html')



@app.route('/update_customer', methods=['GET', 'POST'])
def update_customer():
    if request.method == 'POST':
        try:
            NamaPelanggan = request.form['PelangganLama']
            column_name = request.form['column_name']
            new_value = request.form['new_value']
            
            # Query untuk memeriksa apakah nama pelanggan ada di database
            check_query = "SELECT ID_Pelanggan FROM Pelanggan WHERE Nama_Pelanggan = ?"
            cursor.execute(check_query, (NamaPelanggan,))
            existing_updateCustomer = cursor.fetchone()
            
            if existing_updateCustomer:
                IDPelanggan = existing_updateCustomer[0]
                cursor.execute(f"UPDATE Pelanggan SET {column_name} = ? WHERE ID_Pelanggan = ?", (new_value, IDPelanggan))
                conn.commit()
                return redirect(url_for('function_update'))
            else:
                error = "Nama Pelanggan yang digunakan tidak ada."
                return render_template('update_pelanggan.html', error=error)
                
        except Exception as e:
            return f"Error: {e}"
    return render_template("update_pelanggan.html")


@app.route('/update_machine', methods=['GET', 'POST'])
def update_machine():
    if request.method == 'POST':
        query = """
        SELECT Nama_Mesin_Cuci, Merek, Tarif, Status FROM MesinCuci
        """
        cursor.execute(query)
        transaction_details = cursor.fetchall()
    
        mesin_cuci_list = []
        for detail in transaction_details:
            nama_mesin_cuci, merek, tarif, status = detail
        
            status_message = "Unavailable" if status == 1 else "Available"
            mesin_cuci_list.append((nama_mesin_cuci, merek, tarif, status_message))
        try:
            NamaMesinCuci = request.form['MesinCuciLama']
            column_name = request.form['column_name']
            new_value = request.form['new_value']
            
            # Query untuk memeriksa apakah nama mesin cuci ada di database
            check_query = "SELECT ID_Mesin_Cuci FROM MesinCuci WHERE Nama_Mesin_Cuci = ?"
            cursor.execute(check_query, (NamaMesinCuci,))
            existing_updateMachine = cursor.fetchone()
            
            if existing_updateMachine:
                IDMesinCuci = existing_updateMachine[0]
                cursor.execute(f"UPDATE MesinCuci SET {column_name} = ? WHERE ID_Mesin_Cuci = ?", (new_value, IDMesinCuci))
                conn.commit()
                return redirect(url_for('function_update'))
            else:
                error = "Nama Mesin Cuci yang digunakan tidak terdaftar."
                return render_template('update_mesin_cuci.html', error=error)
        except Exception as e:
            return f"Error: {e}"
            
    return render_template("update_mesin_cuci.html", mesin_cuci_list=mesin_cuci_list)


if __name__ == '__main__':
    app.run(debug=True)
