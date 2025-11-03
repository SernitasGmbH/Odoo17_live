# -*- coding: utf-8 -*-
# License LGPL-3

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CareerApplicationChild(models.Model):
    """
    Model to store child information for family reunion applications.
    Maximum 2 children per application.
    """
    _name = 'coflow.career.application.child'
    _description = 'Career Application - Child Information'
    _order = 'application_id, id'

    application_id = fields.Many2one(
        'coflow.career.application',
        string='Application',
        required=True,
        ondelete='cascade',
        help='Reference to the main job application'
    )

    # Child basic information
    name = fields.Char(
        string='Ad Soyad',
        required=True,
        help='Full name of the child'
    )
    age = fields.Integer(
        string='Yaş',
        required=True,
        help='Age of the child'
    )
    birth_date = fields.Date(
        string='Doğum Tarihi',
        required=True,
        help='Birth date of the child'
    )
    birth_place = fields.Char(
        string='Doğum Yeri',
        required=True,
        help='Birth place of the child'
    )

    # Passport information
    passport_has = fields.Selection([
        ('evet', 'Evet'),
        ('hayir', 'Hayır'),
    ], string='Pasaport Var mı?', required=True, default='hayir',
       help='Does the child have a passport?')

    passport_no = fields.Char(
        string='Pasaport No',
        help='Passport number (required if passport exists)'
    )
    passport_valid_until = fields.Date(
        string='Pasaport Geçerlilik Tarihi',
        help='Passport validity date (required if passport exists)'
    )
    passport_photo_id = fields.Many2one(
        'ir.attachment',
        string='Pasaport Fotoğrafı',
        help='Passport photo attachment (required if passport exists)'
    )

    @api.constrains('age')
    def _check_age(self):
        """Validate that age is positive and reasonable"""
        for record in self:
            if record.age < 0:
                raise ValidationError('Çocuğun yaşı negatif olamaz!')
            if record.age > 25:
                raise ValidationError('Çocuğun yaşı çok yüksek görünüyor (maksimum 25).')

    @api.constrains('birth_date')
    def _check_birth_date(self):
        """Validate that birth date is not in the future"""
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError('Doğum tarihi gelecekte olamaz!')

    @api.constrains('passport_has', 'passport_no', 'passport_valid_until', 'passport_photo_id')
    def _check_passport_fields(self):
        """
        Validate passport-related fields:
        If passport_has = 'evet', then passport_no, passport_valid_until,
        and passport_photo_id are required.
        """
        for record in self:
            if record.passport_has == 'evet':
                if not record.passport_no:
                    raise ValidationError(
                        f'{record.name}: Pasaport var olarak işaretlendi, '
                        'pasaport numarası zorunludur!'
                    )
                if not record.passport_valid_until:
                    raise ValidationError(
                        f'{record.name}: Pasaport var olarak işaretlendi, '
                        'pasaport geçerlilik tarihi zorunludur!'
                    )
                if not record.passport_photo_id:
                    raise ValidationError(
                        f'{record.name}: Pasaport var olarak işaretlendi, '
                        'pasaport fotoğrafı zorunludur!'
                    )

    @api.constrains('passport_valid_until')
    def _check_passport_validity(self):
        """Check that passport is not expired"""
        for record in self:
            if record.passport_valid_until and record.passport_valid_until < fields.Date.today():
                raise ValidationError(
                    f'{record.name}: Pasaport geçerlilik tarihi geçmiş olamaz!'
                )
