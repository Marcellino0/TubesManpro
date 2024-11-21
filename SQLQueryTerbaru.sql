DROP TABLE IF EXISTS Transaksi
DROP TABLE IF EXISTS Pelanggan
DROP TABLE IF EXISTS MesinCuci
DROP TABLE IF EXISTS Kelurahan
DROP TABLE IF EXISTS Kecamatan
DROP TABLE IF EXISTS Pegawai
DROP TABLE IF EXISTS Session

CREATE TABLE Kecamatan (
    ID_Kecamatan INT IDENTITY (1,1) NOT NULL PRIMARY KEY,
    Nama_Kecamatan VARCHAR(50) NOT NULL
)
INSERT INTO Kecamatan (Nama_Kecamatan)
VALUES ('Andir'),('Astana Anyar'),('Antapani'),('Arcamanik'),('Babakan Ciparay'),('Bandung Kidul'),('Bandung Kulon'),('Bandung Wetan'),('Batununggal'),('Bojongloa Kaler')
	,('Bojongloa Kidul'),('Buahbatu'),('Cibeunying Kaler'),('Cibeunying Kidul'),('Cibiru'),('Cicendo'),('Cidadap'),('Cinambo'),('Coblong'),('Gedebage'),('Kiaracondong'),('Lengkong')
	,('Mandalajati'),('Panyileukan'),('Rancasari'),('Regol'),('Sukajadi'),('Sukasari'),('Sumur Bandunng'),('Ujungberung')


CREATE TABLE Kelurahan (
    ID_Kelurahan INT IDENTITY (1,1) NOT NULL PRIMARY KEY,
    Nama_Kelurahan VARCHAR(50) NOT NULL,
    ID_Kecamatan INT NOT NULL FOREIGN KEY (ID_Kecamatan) REFERENCES Kecamatan(ID_Kecamatan)
)

INSERT INTO Kelurahan (Nama_Kelurahan,ID_Kecamatan)
VALUES
	('Campaka', 1),
	('Ciroyom', 1),
	('Dunguscariang', 1),
	('Garuda', 1),
	('Kebonjeruk', 1),
	('Maleber', 1),

	('Cibadak', 2),
	('Karanganyar', 2),
	('Karasak', 2),
	('Nyengseret', 2),
	('Panjunan', 2),
	('Pelindunghewan', 2),

	('Antapani Kidul', 3),
	('Antapani Kulon', 3),
	('Antapani Tengah', 3),
	('Antapani Wetan', 3),

	('Cisaranten Bina Harapan', 4),
	('Cisaranten Endah', 4),
	('Cisaranten Kulon', 4),
	('Sukamiskin', 4),

	('Babakan', 5),
	('Babakanciparay', 5),
	('Cirangrang', 5),
	('Margahayu Utara', 5),
	('Margasuka', 5),
	('Sukahaji', 5),

	('Batununggal', 6),
	('Kujangsari', 6),
	('Mengger', 6),
	('Wates', 6),

	('Caringin', 7),
	('Cibuntu', 7),
	('Cigondewah Kaler', 7),
	('Cigondewah Kidul', 7),
	('Cigondewah Rahayu', 7),
	('Cijerah', 7),
	('Gempolsari', 7),
	('Warungmuncang', 7),

	('Cihapit', 8),
	('Citarum', 8),
	('Tamansari', 8),

	('Binong', 9),
	('Cibangkong', 9),
	('Gumuruh', 9),
	('Kacapiring', 9),
	('Kebongedang', 9),
	('Kebonwaru', 9),
	('Maleer', 9),
	('Samoja', 9),

	('Babakan Asih', 10),
	('Babakan Tarogong', 10),
	('Jamika', 10),
	('Kopo', 10),
	('Suka Asih', 10),

	('Cibaduyut', 11),
	('Cibaduyut Kidul', 11),
	('Cibaduyut Wetan', 11),
	('Kebon Lega', 11),
	('Mekarwangi', 11),
	('Situsaeur', 11),

	('Cijawura', 12),
	('Jatisari', 12),
	('Margasari', 12),
	('Sekejati', 12),

	('Cigadung', 13),
	('Cihaurgeulis', 13),
	('Neglasari', 13),
	('Sukaluyu', 13),

	('Cicadas', 14),
	('Cikutra', 14),
	('Padasuka', 14),
	('Pasirlayung', 14),
	('Sukamaju', 14),
	('Sukapada', 14),

	('Cipadung', 15),
	('Cisurupan', 15),
	('Palasari', 15),
	('Pasirbiru', 15),

	('Arjuna', 16),
	('Husen Sastranegara', 16),
	('Pajajaran', 16),
	('Pamoyanan', 16),
	('Pasirkaliki', 16),
	('Sukaraja', 16),

	('Ciumbuleuit', 17),
	('Hegarmanah', 17),
	('Ledeng', 17),

	('Babakan Penghulu', 18),
	('Cisaranten Wetan', 18),
	('Pakemitan', 18),
	('Sukamulya', 18),

	('Cipaganti', 19),
	('Dago', 19),
	('Lebakgede', 19),
	('Lebaksiliwangi', 19),
	('Sadangserang', 19),
	('Sekeloa', 19),

	('Cimincrang', 20),
	('Cisaranten Kidul', 20),
	('Rancabolang', 20),
	('Rancanumpang', 20),

	('Babakansari', 21),
	('Babakansurabaya', 21),
	('Cicaheum', 21),
	('Kebonkangkung', 21),
	('Kebunjayanti', 21),
	('Sukapura', 21),

	('Burangrang', 22),
	('Cijagra', 22),
	('Cikawao', 22),
	('Lingkar Selatan', 22),
	('Malabar', 22),
	('Paledang', 22),
	('Turangga', 22),

	('Jatihandap', 23),
	('Karangpamulang', 23),
	('Pasir Impun', 23),
	('Sidangjaya', 23),

	('Cipandung Kidul', 24),
	('Cipandung Kulon', 24),
	('Cipandung Wetan', 24),
	('Mekarmulya', 24),

	('Cipamokolan', 25),
	('Darwati', 25),
	('Manjahlega', 25),
	('Mekar Jaya', 25),

	('Ancol', 26),
	('Balonggede', 26),
	('Ciateul', 26),
	('Cigereleng', 26),
	('Ciseureuh', 26),
	('Pasirluyu', 26),
	('Pungkur', 26),

	('Cipedes', 27),
	('Pasteur', 27),
	('Sukabungah', 27),
	('Sukagalih', 27),
	('Sukawarna', 27),

	('Gegerkalong', 28),
	('Isola', 28),
	('Sarijadi', 28),
	('Sukarasa', 28),

	('Babakanciamis', 29),
	('Braga', 29),
	('Kebonpisang', 29),
	('Merdeka', 29),

	('Cigending', 30),
	('Pasanggrahan', 30),
	('Pasirendah', 30),
	('Pasirjati', 30),
	('Pasirwangi', 30)

CREATE TABLE Pegawai (
    ID_Pegawai INT NOT NULL PRIMARY KEY IDENTITY(1,1),
    Nama_Pegawai VARCHAR(50) NOT NULL,
    Username VARCHAR(50) NOT NULL,
    Password VARCHAR(50) NOT NULL
)
INSERT INTO Pegawai (Nama_Pegawai, Username, Password)
VALUES ('Clarence', 'admin', 'admin')


CREATE TABLE Pelanggan (
    ID_Pelanggan INT NOT NULL PRIMARY KEY IDENTITY(1,1),
    Nama_Pelanggan VARCHAR(50) NOT NULL,
    Nomor_Telepon VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NULL,
    Alamat VARCHAR(50) NOT NULL,
    ID_Kelurahan INT NOT NULL FOREIGN KEY (ID_Kelurahan) REFERENCES Kelurahan(ID_Kelurahan)
)

-- Membuat tabel MesinCuci
CREATE TABLE MesinCuci (
    ID_Mesin_Cuci INT NOT NULL PRIMARY KEY IDENTITY(1,1),
    Nama_Mesin_Cuci VARCHAR(50) NOT NULL,
    Merek VARCHAR(50) NOT NULL,
    Kapasitas INT NOT NULL,
    Tarif MONEY NULL,
	Status INT NULL
)

CREATE TABLE Transaksi (
    ID_Transaksi INT  NOT NULL PRIMARY KEY IDENTITY(1,1),
    Tanggal_Transaksi DATE NOT NULL,
    Waktu_Mulai TIME NOT NULL,
    Waktu_Selesai TIME NOT NULL,
	ID_Mesin_Cuci INT NOT NULL FOREIGN KEY (ID_Mesin_Cuci) REFERENCES MesinCuci(ID_Mesin_Cuci),
    ID_Pelanggan INT NOT NULL FOREIGN KEY (ID_Pelanggan) REFERENCES Pelanggan(ID_Pelanggan),
	Total_Biaya MONEY NOT NULL

)



SELECT *
FROM Kecamatan
SELECT *
FROM Kelurahan

SELECT *
FROM Pegawai
SELECT *
FROM Pelanggan
SELECT *
FROM Transaksi

SELECT *
FROM MesinCuci


BULK INSERT Pelanggan
FROM 'C:\Users\MARCELL\Downloads\Download\MIBD\Pelanggan.csv'
WITH (FORMAT = 'CSV')
GO

BULK INSERT MesinCuci
FROM 'C:\Users\MARCELL\Downloads\Download\MIBD\MesinCuci.csv'
WITH (FORMAT = 'CSV')
GO

BULK INSERT Transaksi
FROM 'C:\Users\MARCELL\Downloads\Download\MIBD\Transaksi.csv'
WITH (FORMAT = 'CSV')
GO