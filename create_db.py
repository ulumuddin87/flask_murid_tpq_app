import sqlite3

# Buat koneksi ke file murid.db (akan dibuat baru kalau belum ada)
conn = sqlite3.connect("murid.db")
c = conn.cursor()

# Hapus tabel murid kalau sudah ada sebelumnya (biar clean)
c.execute("DROP TABLE IF EXISTS murid")

# Buat tabel sesuai struktur yang kamu kasih
c.execute("""
CREATE TABLE murid (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    jilid TEXT,
    kelas TEXT,
    alamat TEXT,
    wali_murid TEXT,
    wali_kelas TEXT,
    nik TEXT,
    tempat_tanggal_lahir TEXT,
    jenis_kelamin TEXT,
    status_dalam_keluarga TEXT,
    anak_ke INTEGER,
    nama_ayah TEXT,
    tlp_ayah TEXT,
    pekerjaan_ayah TEXT,
    nama_ibu TEXT,
    tlp_ibu TEXT,
    pekerjaan_ibu TEXT,
    dusun TEXT,
    rt TEXT,
    rw TEXT,
    desa TEXT,
    kecamatan TEXT,
    kabupaten_kota TEXT,
    provinsi TEXT
);
""")

conn.commit()
conn.close()

print("✅ Database murid.db berhasil dibuat ulang dengan tabel murid")
