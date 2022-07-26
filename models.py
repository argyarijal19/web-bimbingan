from colorama import Cursor
import config

def data(TahunID):
    conn = config.Siapdb()
    cursor = conn.cursor()
    query = """SELECT TahunID FROM simak_mst_tahun WHERE ProgramID = 'REG' AND ProdiID = 14 AND TahunID = ifnull(%s, '20212') """
    # query = """SELECT TahunID, ProdiID, Nama, ProgramID FROM simak_mst_tahun WHERE ProgramID = 'REG' AND ProgramID = %s """
    cursor.execute(query, (TahunID,))
    hasil = cursor.fetchall()
    return hasil

def dataJoin(Tahun_id, tipe):
    conn = config.iteungDB()
    cursor = conn.cursor()
    query = """SELECT npm, pembimbing1, pembimbing2, judul, tipe_bimbingan, tahun_id, approval_pembimbing1, approval_pembimbing2 FROM bimbingan_data WHERE prodi_id = 14 AND tahun_id = %s AND tipe_bimbingan = %s """
    cursor.execute(query,(Tahun_id, tipe) )
    hasil = cursor.fetchall()
    return hasil

def namaMhs():
    conn = config.Siapdb()
    cursor = conn.cursor()
    query = """SELECT MhswID, Nama FROM simak_mst_mahasiswa WHERE ProdiID = 14 """
    # query = """SELECT TahunID, ProdiID, Nama, ProgramID FROM simak_mst_tahun WHERE ProgramID = 'REG' AND ProgramID = %s """
    cursor.execute(query)
    hasil = cursor.fetchall()
    return hasil

def namaDosen():
    conn = config.Siapdb()
    cursor = conn.cursor()
    query = """SELECT Login, Nama FROM simak_mst_dosen """
    cursor.execute(query)
    hasil = cursor.fetchall()
    return hasil


def jumlahPertemuan():
    conn = config.Siapdb()
    cursor = conn.cursor()
    query = """SELECT MhswID, COUNT(Pertemuan_), Tipe FROM simak_croot_bimbingan GROUP BY Tipe, MhswID """
    cursor.execute(query)
    hasil = cursor.fetchall()
    return hasil