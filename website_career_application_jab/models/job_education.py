# -*- coding: utf-8 -*-
# License LGPL-3

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CareerApplicationEducation(models.Model):
    """
    Model to store education history for job applications.
    Includes school name, dates, and location.
    """
    _name = 'coflow.career.application.education'
    _description = 'Career Application - Education'
    _order = 'application_id, date_start desc'

    application_id = fields.Many2one(
        'coflow.career.application',
        string='Application',
        required=True,
        ondelete='cascade',
        help='Reference to the main job application'
    )

    # Date range
    date_start = fields.Date(
        string='Başlangıç Tarihi',
        required=True,
        help='Start date of education'
    )
    date_end = fields.Date(
        string='Bitiş Tarihi',
        help='End date of education (leave empty if currently studying)'
    )
    is_current = fields.Boolean(
        string='Halen Devam Ediyor',
        default=False,
        help='Check if currently studying'
    )

    # School information
    school = fields.Char(
        string='Okul Adı',
        required=True,
        help='Name of the school/institution'
    )
    city = fields.Char(
        string='Şehir',
        required=True,
        help='City where the school is located'
    )

    # Computed field for display name
    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
        help='Computed display name for the education record'
    )

    @api.depends('school', 'date_start')
    def _compute_name(self):
        """Compute a display name for the education record"""
        for record in self:
            if record.school:
                record.name = record.school
            else:
                record.name = 'New Education'

    @api.constrains('date_start', 'date_end', 'is_current')
    def _check_dates(self):
        """Validate date logic"""
        for record in self:
            if record.date_start and record.date_start > fields.Date.today():
                raise ValidationError('Eğitim başlangıç tarihi gelecekte olamaz!')

            if not record.is_current and record.date_end:
                if record.date_end < record.date_start:
                    raise ValidationError('Bitiş tarihi başlangıç tarihinden önce olamaz!')
                if record.date_end > fields.Date.today():
                    raise ValidationError('Eğitim bitiş tarihi gelecekte olamaz!')

    @api.onchange('is_current')
    def _onchange_is_current(self):
        """Clear end date if currently studying"""
        if self.is_current:
            self.date_end = False
