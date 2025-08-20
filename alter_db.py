import sqlite3

conn = sqlite3.connect("murid.db")
cursor = conn.cursor()

sql_commands = [
    "ALTER TABLE murid ADD COLUMN nama_depan TEXT;",
    "ALTER TABLE murid ADD COLUMN nama_belakang TEXT;",
    "ALTER TABLE murid ADD COLUMN jilid TEXT;",
    "ALTER TABLE murid ADD COLUMN no_induk TEXT;",
    "ALTER TABLE murid ADD COLUMN nik TEXT;",
    "ALTER TABLE murid ADD COLUMN tempat_tanggal_lahir TEXT;",
    "ALTER TABLE murid ADD COLUMN jenis_kelamin TEXT;",
    "ALTER TABLE murid ADD COLUMN status_dalam_keluarga TEXT;",
    "ALTER TABLE murid ADD COLUMN anak_ke INTEGER;",
    "ALTER TABLE murid ADD COLUMN nama_ayah TEXT;",
    "ALTER TABLE murid ADD COLUMN no_tlp_ayah TEXT;",
    "ALTER TABLE murid ADD COLUMN pekerjaan_ayah TEXT;",
    "ALTER TABLE murid ADD COLUMN nama_ibu TEXT;",
    "ALTER TABLE murid ADD COLUMN no_tlp_ibu TEXT;",
    "ALTER TABLE murid ADD COLUMN pekerjaan_ibu TEXT;",
    "ALTER TABLE murid ADD COLUMN dusun TEXT;",
    "ALTER TABLE murid ADD COLUMN rt TEXT;",
    "ALTER TABLE murid ADD COLUMN rw TEXT;",
    "ALTER TABLE murid ADD COLUMN desa TEXT;",
    "ALTER TABLE murid ADD COLUMN kecamatan TEXT;",
    "ALTER TABLE murid ADD COLUMN kabupaten_kota TEXT;",
    "ALTER TABLE murid ADD COLUMN provinsi TEXT;"
]

for cmd in sql_commands:
    try:
        cursor.execute(cmd)
        print(f"✅ Berhasil: {cmd}")
    except Exception as e:
        print(f"⚠️ Lewati: {cmd} -> {e}")

conn.commit()
conn.close()

print("🎉 Selesai update database murid.db")
