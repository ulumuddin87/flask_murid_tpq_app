import sqlite3
import shutil

# Backup dulu biar aman
shutil.copy("murid.db", "murid_backup.db")

try:
    conn_old = sqlite3.connect("murid.db")
    conn_new = sqlite3.connect("murid_fixed.db")

    dump = "\n".join(conn_old.iterdump())   # ambil seluruh isi
    conn_new.executescript(dump)            # tulis ulang ke db baru

    conn_old.close()
    conn_new.close()

    print("✅ Database berhasil diperbaiki. Coba pakai murid_fixed.db")
except Exception as e:
    print("❌ Gagal perbaiki:", e)
