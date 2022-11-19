from odoo import models, fields

class Customer(models.Model):
    _name = 'beanfo.customer'
    _description = 'Information about customer'

    nama = fields.Char(
        string = 'Nama',
        required = True
    )

    email = fields.Char(
        string = 'E-mail',
        required = True
    )

    nomor_telpon = fields.Char(
        string = 'Nomor Telpon',
        required = True
    )

    jumlah_point = fields.Integer(
        string = 'Jumlah Poin',
        default = 0
    )

    boleh_dikontak = fields.Boolean(
        string = 'Apakah pelanggan ingin menerima promosi?',
        default = True
    )

class Promotion(models.Model):
    _name = 'beanfo.promotion'
    _description = 'Information about promotion'

    nama_promo = fields.Char(
        string = 'Nama Promo',
        required = True
    )

    tanggal_mulai = fields.Date(
        string = 'Tanggal Mulai',
        required = True
    )

    tanggal_selesai = fields.Date(
        string = 'Tanggal Selesai',
        required = True
    )

    kuota = fields.Integer(
        string = 'Kuota Pemakaian',
        required = True
    )

    deskripsi = fields.Text(
        string = 'Deskripsi Promo',
        required = True
    )

class Transaction(models.Model):
    _name = 'beanfo.transaction'
    _description = 'Information about transaction'

    nama_pelanggan = fields.Many2one(
        'beanfo.customer',
        string = 'Nama Pelanggan',
        required = True
    )

    tanggal = fields.Date(
        string = 'Tanggal Transaksi',
        required = True
    )

    total = fields.Integer(
        string = 'Total Transaksi',
        required = True
    )

    poin = fields.Integer(
        string = 'Poin yang didapat',
        required = True
    )

    id_promo_umum = fields.Many2one(
        'beanfo.promotion',
        string = 'Kode Promo Umum',
        default = ''
    )