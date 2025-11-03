# -*- coding: utf-8 -*-
# License LGPL-3

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CareerApplicationExperience(models.Model):
    """
    Model to store work experience information for job applications.
    Includes company, position, departments, and medical devices used.
    """
    _name = 'coflow.career.application.experience'
    _description = 'Career Application - Work Experience'
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
        help='Start date of employment'
    )
    date_end = fields.Date(
        string='Bitiş Tarihi',
        help='End date of employment (leave empty if currently working)'
    )
    is_current = fields.Boolean(
        string='Halen Devam Ediyor',
        default=False,
        help='Check if currently working in this position'
    )

    # Company information
    company = fields.Char(
        string='Kurum Adı',
        required=True,
        help='Name of the company/institution'
    )
    city = fields.Char(
        string='Şehir',
        required=True,
        help='City where the company is located'
    )
    position = fields.Char(
        string='Pozisyon',
        required=True,
        help='Job position/title'
    )
    duties = fields.Text(
        string='Yapılan İşler',
        required=True,
        help='Description of duties and responsibilities'
    )

    # Departments (Many2many relation)
    department_ids = fields.Many2many(
        'coflow.hospital.department',
        'experience_department_rel',
        'experience_id',
        'department_id',
        string='Çalışılan Bölümler',
        help='Hospital departments worked in'
    )
    departments_other = fields.Char(
        string='Diğer Bölüm',
        help='Other department name (required if "Diğer" is selected in departments)'
    )

    # Medical devices (Many2many relation)
    device_ids = fields.Many2many(
        'coflow.medical.device',
        'experience_device_rel',
        'experience_id',
        'device_id',
        string='Kullanılan Cihazlar',
        help='Medical devices used during this employment'
    )
    devices_other = fields.Char(
        string='Diğer Cihaz',
        help='Other device name (required if "Diğer" is selected in devices)'
    )

    # Computed field for display name
    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
        help='Computed display name for the experience record'
    )

    @api.depends('company', 'position', 'date_start')
    def _compute_name(self):
        """Compute a display name for the experience record"""
        for record in self:
            if record.company and record.position:
                record.name = f'{record.position} - {record.company}'
            elif record.company:
                record.name = record.company
            else:
                record.name = 'New Experience'

    @api.constrains('date_start', 'date_end', 'is_current')
    def _check_dates(self):
        """Validate date logic"""
        for record in self:
            if record.date_start and record.date_start > fields.Date.today():
                raise ValidationError('Başlangıç tarihi gelecekte olamaz!')

            if not record.is_current and record.date_end:
                if record.date_end < record.date_start:
                    raise ValidationError('Bitiş tarihi başlangıç tarihinden önce olamaz!')
                if record.date_end > fields.Date.today():
                    raise ValidationError('Bitiş tarihi gelecekte olamaz!')

    @api.constrains('department_ids', 'departments_other')
    def _check_departments(self):
        """
        Validate that departments are selected.
        If "Diğer" (Other) is selected, departments_other must be filled.
        """
        for record in self:
            if not record.department_ids:
                raise ValidationError('En az bir bölüm seçilmelidir!')

            # Check if "Diğer" (Other) department is selected
            other_dept = record.department_ids.filtered(lambda d: d.is_other)
            if other_dept and not record.departments_other:
                raise ValidationError(
                    '"Diğer" bölüm seçildi, lütfen bölüm adını belirtiniz!'
                )

    @api.constrains('device_ids', 'devices_other')
    def _check_devices(self):
        """
        Validate that devices are selected.
        If "Diğer" (Other) is selected, devices_other must be filled.
        """
        for record in self:
            if not record.device_ids:
                raise ValidationError('En az bir cihaz seçilmelidir!')

            # Check if "Diğer" (Other) device is selected
            other_device = record.device_ids.filtered(lambda d: d.is_other)
            if other_device and not record.devices_other:
                raise ValidationError(
                    '"Diğer" cihaz seçildi, lütfen cihaz adını belirtiniz!'
                )

    @api.onchange('is_current')
    def _onchange_is_current(self):
        """Clear end date if currently working"""
        if self.is_current:
            self.date_end = False
