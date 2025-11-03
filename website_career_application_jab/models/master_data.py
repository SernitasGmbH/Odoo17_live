# -*- coding: utf-8 -*-
# License LGPL-3

from odoo import models, fields, api


class HospitalDepartment(models.Model):
    """
    Master data model for hospital departments.
    Used in experience records and job preferences.
    """
    _name = 'coflow.hospital.department'
    _description = 'Hospital Department'
    _order = 'sequence, name'

    name = fields.Char(
        string='Department Name',
        required=True,
        translate=True,
        help='Name of the hospital department'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Used to order departments in selection lists'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this department will be hidden from selection lists'
    )
    is_other = fields.Boolean(
        string='Is Other',
        default=False,
        help='Mark this as the "Other" option'
    )

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Department name must be unique!')
    ]


class MedicalDevice(models.Model):
    """
    Master data model for medical devices.
    Used in experience records to track device usage.
    """
    _name = 'coflow.medical.device'
    _description = 'Medical Device'
    _order = 'sequence, name'

    name = fields.Char(
        string='Device Name',
        required=True,
        translate=True,
        help='Name of the medical device'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Used to order devices in selection lists'
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, this device will be hidden from selection lists'
    )
    is_other = fields.Boolean(
        string='Is Other',
        default=False,
        help='Mark this as the "Other" option'
    )

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Device name must be unique!')
    ]
