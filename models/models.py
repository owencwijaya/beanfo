import datetime
from math import floor
from odoo import models, fields, api


class Customer(models.Model):
    _name = 'beanfo.customer'
    _description = 'Information about customer'
    _rec_name = 'nama'

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

    @api.model
    def create(self,vals):
        #Todo code
        #query to mailing_contact insert name and email
        self.env.cr.execute("INSERT INTO mailing_contact (name,email,email_normalized) VALUES (%s,%s,%s)",(vals['nama'],vals['email'],vals['email']))
        self.env.cr.execute("SELECT id FROM mailing_contact WHERE name = %s AND email = %s",(vals['nama'],vals['email']))
        if(vals['boleh_dikontak']):
            #query to mailing_contact_list insert contact_id and list_id
            self.env.cr.execute("INSERT INTO mailing_contact_list_rel (contact_id,list_id,opt_out) VALUES (%s,%s,%s)",(self.env.cr.fetchone()[0],1,'f'))
        else:
            self.env.cr.execute("INSERT INTO mailing_contact_list_rel (contact_id,list_id,opt_out) VALUES (%s,%s,%s)",(self.env.cr.fetchone()[0],1,'t'))
        res = super(Customer, self).create(vals)
        return res 


class Promotion(models.Model):
    _name = 'beanfo.promotion'
    _description = 'Information about promotion'
    _rec_name = 'nama_promo'

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

    @api.model
    def create(self,vals):
        #Get Promotion
        self.env.cr.execute("SELECT * FROM beanfo_promotion WHERE id = %s",(vals['id_promo_umum'],))
        promo = self.env.cr.fetchone()
        #check if promo is valid
        if(promo):
            #check validity date
            print(type(promo[2]))
            print(type(vals['tanggal']))
            if(promo[2] > datetime.datetime.strptime(vals['tanggal'],'%Y-%m-%d').date()):
                #promo havent started yet
                raise Warning("Promo belum dimulai")
            elif(promo[3] < datetime.datetime.strptime(vals['tanggal'],'%Y-%m-%d').date()):
                #promo already ended
                raise Warning("Promo sudah berakhir")
            elif(promo[4] <= 0):
                #promo already used
                raise Warning("Promo sudah habis")
            else:
                #promo is valid
                #update promo kuota
                self.env.cr.execute("UPDATE beanfo_promotion SET kuota = %s WHERE nama_promo = %s",(promo[4]-1,promo[1]))
                #update customer point
                vals['poin'] = floor(vals['total']/1000)
                self.env.cr.execute("UPDATE beanfo_customer SET jumlah_point = jumlah_point + %s WHERE id = %s",(vals['poin'],vals['nama_pelanggan']))
                #save transaction
                return super(Transaction, self).create(vals)
                