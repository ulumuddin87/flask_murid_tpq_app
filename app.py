from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import sqlite3, csv, io
from fpdf import FPDF
from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)
app.secret_key = "rahasia_tpq"

DB_NAME = "murid.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn





@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return redirect(url_for("data_murid"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "admin":
            session["user"] = username
            return redirect(url_for("data_murid"))
        else:
            flash("Username atau password salah", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/murid")
def data_murid():
    if not session.get("user"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    murid = conn.execute("SELECT * FROM murid").fetchall()
    kelas_list = conn.execute("SELECT DISTINCT kelas FROM murid").fetchall()
    conn.close()
    return render_template("data_murid.html", murid=murid, kelas_list=kelas_list)


# Route biodata murid
@app.route("/biodata/<int:id>", methods=["GET", "POST"])
def biodata_murid(id):
    conn = get_db_connection()
    murid = conn.execute("SELECT * FROM murid WHERE id = ?", (id,)).fetchone()

    if murid is None:
        conn.close()
        return "Data murid tidak ditemukan", 404

    if request.method == "POST":
        nama_lengkap = request.form["nama_lengkap"]  # ambil dari form
        no_induk = request.form["no_induk"]
        nik = request.form["nik"]
        tempat_tanggal_lahir = request.form["tempat_tanggal_lahir"]
        jenis_kelamin = request.form["jenis_kelamin"]
        status_dalam_keluarga = request.form["status_dalam_keluarga"]
        anak_ke = request.form["anak_ke"]
        nama_ayah = request.form["nama_ayah"]
        no_tlp_ayah = request.form["no_tlp_ayah"]
        pekerjaan_ayah = request.form["pekerjaan_ayah"]
        nama_ibu = request.form["nama_ibu"]
        no_tlp_ibu = request.form["no_tlp_ibu"]
        pekerjaan_ibu = request.form["pekerjaan_ibu"]
        dusun = request.form["dusun"]
        rt = request.form["rt"]
        rw = request.form["rw"]
        desa = request.form["desa"]
        kecamatan = request.form["kecamatan"]
        kabupaten_kota = request.form["kabupaten_kota"]
        provinsi = request.form["provinsi"]

        conn.execute("""
            UPDATE murid SET 
                nama=?, no_induk=?, nik=?, tempat_tanggal_lahir=?, jenis_kelamin=?, 
                status_dalam_keluarga=?, anak_ke=?,
                nama_ayah=?, no_tlp_ayah=?, pekerjaan_ayah=?, nama_ibu=?, pekerjaan_ibu=?, no_tlp_ibu=?,
                dusun=?, rt=?, rw=?, desa=?, kecamatan=?, kabupaten_kota=?, provinsi=?
            WHERE id=?
        """, (nama_lengkap, nik, tempat_tanggal_lahir, jenis_kelamin,
              status_dalam_keluarga, anak_ke,
              nama_ayah, no_tlp_ayah, pekerjaan_ayah, nama_ibu, pekerjaan_ibu, no_tlp_ibu,              dusun, rt, rw, desa, kecamatan, kabupaten_kota, provinsi, id))
        conn.commit()
        conn.close()
        return redirect(url_for("data_murid"))

    conn.close()
    return render_template("biodata_murid.html", murid=murid)



@app.route("/add", methods=["GET", "POST"])
def add_murid():
    if request.method == "POST":
        nama = request.form["nama"]
        jilid = request.form["jilid"]
        kelas = request.form["kelas"]
        alamat = request.form["alamat"]
        wali_murid = request.form["wali_murid"]
        wali_kelas = request.form["wali_kelas"]
        conn = get_db_connection()
        conn.execute("INSERT INTO murid (nama, jilid, kelas, alamat, wali_murid, wali_kelas) VALUES (?, ?, ?, ?, ?, ?)",
                     (nama, jilid, kelas, alamat, wali_murid, wali_kelas))
        conn.commit()
        conn.close()
        return redirect(url_for("data_murid"))
    return render_template("add_murid.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_murid(id):
    conn = get_db_connection()
    murid = conn.execute("SELECT * FROM murid WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        nama = request.form["nama"]
        jilid = request.form["jilid"]
        kelas = request.form["kelas"]
        alamat = request.form["alamat"]
        wali_murid = request.form["wali_murid"]
        wali_kelas = request.form["wali_kelas"]
        conn.execute("UPDATE murid SET nama=?, jilid=?, kelas=?, alamat=?, wali_murid=?, wali_kelas=? WHERE id=?",
                     (nama, jilid, kelas, alamat, wali_murid, wali_kelas, id))
        conn.commit()
        conn.close()
        return redirect(url_for("data_murid"))
    conn.close()
    return render_template("edit_murid.html", murid=murid)

@app.route("/delete/<int:id>")
def delete_murid(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM murid WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("data_murid"))
#
#@app.route("/biodata/<int:id>")
#def biodata_murid(id):
#    conn = get_db_connection()
#    murid = conn.execute("SELECT * FROM murid WHERE id = ?", (id,)).fetchone()
#    conn.close()
#    if murid is None:
#        return "Data murid tidak ditemukan", 404
#    return render_template("biodata_murid.html", murid=murid)


@app.route("/cetak")
def cetak_data():
    conn = get_db_connection()
    murid = conn.execute("SELECT * FROM murid").fetchall()
    conn.close()
    return render_template("cetak.html", murid=murid)

@app.route("/export/csv")
def export_csv():
    conn = get_db_connection()
    murid = conn.execute("SELECT * FROM murid").fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Nama", "jilid", "Kelas", "Alamat", "Wali Murid", "Wali Kelas"])
    for m in murid:
        writer.writerow([m["id"], m["nama"], m["jilid"], m["kelas"], m["alamat"], m["wali_murid"], m["wali_kelas"]])

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode("utf-8")),
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="murid.csv")

@app.route("/export/pdf")
def export_pdf():
    conn = get_db_connection()
    murid = conn.execute("SELECT * FROM murid").fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Data Murid", ln=True, align="C")
    pdf.ln(10)

    for m in murid:
        pdf.cell(200, 10, f"{m['id']} - {m['nama']} - {m['kelas']}", ln=True)

    pdf_output = io.BytesIO(pdf.output(dest="S").encode("latin1"))
    pdf_output.seek(0)
    return send_file(pdf_output, mimetype="application/pdf", as_attachment=True, download_name="murid.pdf")

#if __name__ == "__main__":
#    app.run(debug=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

