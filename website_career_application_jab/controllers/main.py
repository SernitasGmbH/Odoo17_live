# -*- coding: utf-8 -*-
# License LGPL-3

import base64
import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

# File size limit (10 MB in bytes)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'pdf': ['application/pdf'],
    'jpg': ['image/jpeg', 'image/jpg'],
    'jpeg': ['image/jpeg', 'image/jpg'],
    'png': ['image/png'],
}


class CareerApplicationController(http.Controller):
    """
    Website controller for career application form.
    Handles GET (form display) and POST (form submission).
    """

    @http.route('/kariyer/basvuru', type='http', auth='public', website=True, methods=['GET'], csrf=False)
    def career_application_form(self, **kwargs):
        """
        Display the career application form.
        """
        # Get master data for form selections
        departments = request.env['coflow.hospital.department'].sudo().search([
            ('active', '=', True)
        ], order='sequence, name')

        devices = request.env['coflow.medical.device'].sudo().search([
            ('active', '=', True)
        ], order='sequence, name')

        # Filter departments for job preferences (exclude "Diğer")
        preference_departments = departments.filtered(lambda d: not d.is_other)

        values = {
            'departments': departments,
            'devices': devices,
            'preference_departments': preference_departments,
            'errors': {},
            'form_data': kwargs,  # In case of validation errors, repopulate form
        }

        return request.render('website_career_application_jab.career_application_form_template', values)

    @http.route('/kariyer/basvuru', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def career_application_submit(self, **post):
        """
        Process the career application form submission.
        Validates all fields, handles file uploads, and creates the application record.
        """
        errors = {}
        form_params = request.httprequest.form
        attachment_env = request.env['ir.attachment'].sudo()
        application_env = request.env['coflow.career.application'].sudo()

        try:
            # ==================== COLLECT AND VALIDATE BASIC DATA ====================

            # Personal information
            full_name = post.get('full_name', '').strip()
            gender = post.get('gender', '').strip()
            birth_date = post.get('birth_date', '').strip()
            birth_place = post.get('birth_place', '').strip()
            birth_country = post.get('birth_country', '').strip()

            # Address
            addr_mahalle = post.get('addr_mahalle', '').strip()
            addr_cadde = post.get('addr_cadde', '').strip()
            addr_sokak = post.get('addr_sokak', '').strip()
            addr_apt_no = post.get('addr_apt_no', '').strip()
            addr_daire_no = post.get('addr_daire_no', '').strip()
            addr_postcode = post.get('addr_postcode', '').strip()
            addr_district = post.get('addr_district', '').strip()
            addr_city = post.get('addr_city', '').strip()
            addr_country = post.get('addr_country', '').strip()

            # Contact
            phone = post.get('phone', '').strip()
            email = post.get('email', '').strip()
            marital_status = post.get('marital_status', '').strip()

            # Passport
            passport_has = post.get('passport_has', '').strip()
            passport_no = post.get('passport_no', '').strip() if passport_has == 'evet' else False
            passport_valid_until = post.get('passport_valid_until', '').strip() if passport_has == 'evet' else False

            # Disability
            disability = post.get('disability', '').strip()
            disability_note = post.get('disability_note', '').strip() if disability == 'var' else False

            # Military (for males)
            military_status = post.get('military_status', '').strip() if gender == 'erkek' else False
            military_postpone_until = post.get('military_postpone_until', '').strip() if military_status == 'tecilli' else False

            # Criminal record
            criminal_record = post.get('criminal_record', '').strip()

            # Family reunion
            family_reunion = post.get('family_reunion', '').strip()
            has_spouse = post.get('has_spouse') == 'on' if family_reunion == 'evet' else False
            children_count = int(post.get('children_count', 0)) if family_reunion == 'evet' else 0

            # Spouse information
            spouse_name = post.get('spouse_name', '').strip() if has_spouse else False
            spouse_birth_date = post.get('spouse_birth_date', '').strip() if has_spouse else False
            spouse_birth_place = post.get('spouse_birth_place', '').strip() if has_spouse else False
            spouse_phone = post.get('spouse_phone', '').strip() if has_spouse else False
            spouse_email = post.get('spouse_email', '').strip() if has_spouse else False
            spouse_passport_has = post.get('spouse_passport_has', '').strip() if has_spouse else False
            spouse_passport_no = post.get('spouse_passport_no', '').strip() if spouse_passport_has == 'evet' else False
            spouse_passport_valid_until = post.get('spouse_passport_valid_until', '').strip() if spouse_passport_has == 'evet' else False
            spouse_german_certificate = post.get('spouse_german_certificate', '').strip() if has_spouse else False

            # Language & Certificate
            german_level = post.get('german_level', '').strip()
            has_language_certificate = post.get('has_language_certificate', '').strip()
            language_certificate_type = post.get('language_certificate_type', '').strip() if has_language_certificate == 'evet' else False

            # Recognition
            recognition_status = post.get('recognition_status', '').strip()
            recognition_state = post.get('recognition_state', '').strip() if recognition_status in ('evet', 'devam-ediyor') else False
            recognition_applied_at = post.get('recognition_applied_at', '').strip() if recognition_status in ('evet', 'devam-ediyor') else False
            recognition_received_at = post.get('recognition_received_at', '').strip() if recognition_status in ('evet', 'devam-ediyor') else False

            # Job preferences
            choice1 = int(post.get('choice1', 0))
            choice2 = int(post.get('choice2', 0))
            choice3 = int(post.get('choice3', 0))
            accept_other_department = post.get('accept_other_department') == 'on'

            # Motivation & Extra
            motivation_text = post.get('motivation_text', '').strip()
            extra_info = post.get('extra_info', '').strip() or False

            # Consent
            consent_ok = post.get('consent_ok') == 'on'
            consent_date = post.get('consent_date', '').strip()
            consent_name = post.get('consent_name', '').strip()

            # ==================== FILE UPLOADS ====================

            def process_file_upload(file_field_name, file_name_prefix):
                """Helper function to process file uploads with validation"""
                file_data = request.httprequest.files.get(file_field_name)
                if not file_data or not file_data.filename:
                    return False

                # Check file size
                file_data.seek(0, 2)  # Seek to end
                file_size = file_data.tell()
                file_data.seek(0)  # Seek back to start

                if file_size > MAX_FILE_SIZE:
                    errors[file_field_name] = f'Dosya boyutu çok büyük (maksimum 10MB). Yüklenen: {file_size / 1024 / 1024:.2f}MB'
                    return False

                # Check file extension
                filename = file_data.filename.lower()
                extension = filename.rsplit('.', 1)[-1] if '.' in filename else ''

                if extension not in ALLOWED_EXTENSIONS:
                    errors[file_field_name] = f'Geçersiz dosya uzantısı. İzin verilenler: PDF, JPG, PNG'
                    return False

                # Read file content
                file_content = base64.b64encode(file_data.read())

                # Create attachment
                attachment = attachment_env.create({
                    'name': f"{file_name_prefix}_{filename}",
                    'datas': file_content,
                    'mimetype': file_data.content_type,
                    'res_model': 'coflow.career.application',
                })

                return attachment.id

            # Process all file uploads
            passport_photo_id = process_file_upload('passport_photo', 'passport') if passport_has == 'evet' else False
            disability_doc_id = process_file_upload('disability_doc', 'disability') if disability == 'var' else False
            military_postpone_doc_id = process_file_upload('military_postpone_doc', 'military') if military_status == 'tecilli' else False
            criminal_record_doc_id = process_file_upload('criminal_record_doc', 'criminal_record')
            spouse_passport_photo_id = process_file_upload('spouse_passport_photo', 'spouse_passport') if spouse_passport_has == 'evet' else False
            language_certificate_doc_id = process_file_upload('language_certificate_doc', 'language_cert') if has_language_certificate == 'evet' else False
            formul_a_b_doc_id = process_file_upload('formul_a_b_doc', 'formul_ab') or False

            # If there are file upload errors, re-render form with errors
            if errors:
                return self._render_form_with_errors(errors, post)

            # ==================== PREPARE APPLICATION VALUES ====================

            application_vals = {
                # Personal
                'full_name': full_name,
                'gender': gender,
                'birth_date': birth_date,
                'birth_place': birth_place,
                'birth_country': birth_country,
                'marital_status': marital_status,

                # Address
                'addr_mahalle': addr_mahalle,
                'addr_cadde': addr_cadde,
                'addr_sokak': addr_sokak,
                'addr_apt_no': addr_apt_no,
                'addr_daire_no': addr_daire_no,
                'addr_postcode': addr_postcode,
                'addr_district': addr_district,
                'addr_city': addr_city,
                'addr_country': addr_country,

                # Contact
                'phone': phone,
                'email': email,

                # Passport
                'passport_has': passport_has,
                'passport_no': passport_no,
                'passport_valid_until': passport_valid_until,
                'passport_photo_id': passport_photo_id,

                # Disability
                'disability': disability,
                'disability_note': disability_note,
                'disability_doc_id': disability_doc_id,

                # Military
                'military_status': military_status,
                'military_postpone_until': military_postpone_until,
                'military_postpone_doc_id': military_postpone_doc_id,

                # Criminal record
                'criminal_record': criminal_record,
                'criminal_record_doc_id': criminal_record_doc_id,

                # Family reunion
                'family_reunion': family_reunion,
                'has_spouse': has_spouse,
                'children_count': children_count,

                # Spouse
                'spouse_name': spouse_name,
                'spouse_birth_date': spouse_birth_date,
                'spouse_birth_place': spouse_birth_place,
                'spouse_phone': spouse_phone,
                'spouse_email': spouse_email,
                'spouse_passport_has': spouse_passport_has,
                'spouse_passport_no': spouse_passport_no,
                'spouse_passport_valid_until': spouse_passport_valid_until,
                'spouse_passport_photo_id': spouse_passport_photo_id,
                'spouse_german_certificate': spouse_german_certificate,

                # Language
                'german_level': german_level,
                'has_language_certificate': has_language_certificate,
                'language_certificate_type': language_certificate_type,
                'language_certificate_doc_id': language_certificate_doc_id,

                # Recognition
                'recognition_status': recognition_status,
                'recognition_state': recognition_state,
                'recognition_applied_at': recognition_applied_at,
                'recognition_received_at': recognition_received_at,

                # Preferences
                'choice1': choice1,
                'choice2': choice2,
                'choice3': choice3,
                'accept_other_department': accept_other_department,

                # Motivation
                'motivation_text': motivation_text,
                'extra_info': extra_info,

                # Documents
                'formul_a_b_doc_id': formul_a_b_doc_id,

                # Consent
                'consent_ok': consent_ok,
                'consent_date': consent_date,
                'consent_name': consent_name,

                # State
                'state': 'submitted',
            }

            # ==================== CREATE APPLICATION ====================

            application = application_env.create(application_vals)

            # ==================== CREATE CHILDREN RECORDS ====================

            if family_reunion == 'evet' and children_count > 0:
                child_env = request.env['coflow.career.application.child'].sudo()
                for i in range(1, children_count + 1):
                    child_name = post.get(f'child_name_{i}', '').strip()
                    child_age = int(post.get(f'child_age_{i}', 0))
                    child_birth_date = post.get(f'child_birth_date_{i}', '').strip()
                    child_birth_place = post.get(f'child_birth_place_{i}', '').strip()
                    child_passport_has = post.get(f'child_passport_has_{i}', '').strip()
                    child_passport_no = post.get(f'child_passport_no_{i}', '').strip() if child_passport_has == 'evet' else False
                    child_passport_valid_until = post.get(f'child_passport_valid_until_{i}', '').strip() if child_passport_has == 'evet' else False

                    # Process child passport photo
                    child_passport_photo_id = process_file_upload(f'child_passport_photo_{i}', f'child_{i}_passport') if child_passport_has == 'evet' else False

                    child_vals = {
                        'application_id': application.id,
                        'name': child_name,
                        'age': child_age,
                        'birth_date': child_birth_date,
                        'birth_place': child_birth_place,
                        'passport_has': child_passport_has,
                        'passport_no': child_passport_no,
                        'passport_valid_until': child_passport_valid_until,
                        'passport_photo_id': child_passport_photo_id,
                    }

                    child_env.create(child_vals)

            # ==================== CREATE EXPERIENCE RECORDS ====================

            # Count experience entries
            experience_count = 0
            for key in post.keys():
                if key.startswith('experience_company_'):
                    idx = key.replace('experience_company_', '')
                    if idx.isdigit():
                        experience_count = max(experience_count, int(idx))

            if experience_count > 0:
                experience_env = request.env['coflow.career.application.experience'].sudo()
                for i in range(1, experience_count + 1):
                    company = post.get(f'experience_company_{i}', '').strip()
                    if not company:  # Skip empty entries
                        continue

                    position = post.get(f'experience_position_{i}', '').strip()
                    city = post.get(f'experience_city_{i}', '').strip()
                    date_start = post.get(f'experience_date_start_{i}', '').strip()
                    date_end = post.get(f'experience_date_end_{i}', '').strip() or False
                    is_current = post.get(f'experience_is_current_{i}') == 'on'
                    duties = post.get(f'experience_duties_{i}', '').strip()

                    # Get selected departments (many2many)
                    department_ids = []
                    dept_field = f'experience_departments_{i}'
                    dept_values = []
                    if hasattr(form_params, 'getlist'):
                        dept_values = [val for val in form_params.getlist(dept_field) if val]
                    if not dept_values:
                        dept_raw = post.get(dept_field)
                        if isinstance(dept_raw, (list, tuple, set)):
                            dept_values = [val for val in dept_raw if val]
                        elif dept_raw:
                            dept_values = [dept_raw]
                    if dept_values:
                        department_ids = [int(str(val)) for val in dept_values if str(val).isdigit()]

                    departments_other = post.get(f'experience_departments_other_{i}', '').strip() or False

                    # Get selected devices (many2many)
                    device_ids = []
                    device_field = f'experience_devices_{i}'
                    device_values = []
                    if hasattr(form_params, 'getlist'):
                        device_values = [val for val in form_params.getlist(device_field) if val]
                    if not device_values:
                        device_raw = post.get(device_field)
                        if isinstance(device_raw, (list, tuple, set)):
                            device_values = [val for val in device_raw if val]
                        elif device_raw:
                            device_values = [device_raw]
                    if device_values:
                        device_ids = [int(str(val)) for val in device_values if str(val).isdigit()]

                    devices_other = post.get(f'experience_devices_other_{i}', '').strip() or False

                    experience_vals = {
                        'application_id': application.id,
                        'company': company,
                        'position': position,
                        'city': city,
                        'date_start': date_start,
                        'date_end': date_end,
                        'is_current': is_current,
                        'duties': duties,
                        'department_ids': [(6, 0, department_ids)],
                        'departments_other': departments_other,
                        'device_ids': [(6, 0, device_ids)],
                        'devices_other': devices_other,
                    }

                    experience_env.create(experience_vals)

            # ==================== CREATE EDUCATION RECORDS ====================

            # Count education entries
            education_count = 0
            for key in post.keys():
                if key.startswith('education_school_'):
                    idx = key.replace('education_school_', '')
                    if idx.isdigit():
                        education_count = max(education_count, int(idx))

            if education_count > 0:
                education_env = request.env['coflow.career.application.education'].sudo()
                for i in range(1, education_count + 1):
                    school = post.get(f'education_school_{i}', '').strip()
                    if not school:  # Skip empty entries
                        continue

                    city = post.get(f'education_city_{i}', '').strip()
                    date_start = post.get(f'education_date_start_{i}', '').strip()
                    date_end = post.get(f'education_date_end_{i}', '').strip() or False
                    is_current = post.get(f'education_is_current_{i}') == 'on'

                    education_vals = {
                        'application_id': application.id,
                        'school': school,
                        'city': city,
                        'date_start': date_start,
                        'date_end': date_end,
                        'is_current': is_current,
                    }

                    education_env.create(education_vals)

            # ==================== REDIRECT TO THANK YOU PAGE ====================

            return request.redirect('/kariyer/tesekkurler')

        except ValidationError as e:
            _logger.error(f"Validation error in career application: {e}")
            errors['general'] = str(e)
            return self._render_form_with_errors(errors, post)

        except Exception as e:
            _logger.exception(f"Error creating career application: {e}")
            errors['general'] = 'Başvuru sırasında bir hata oluştu. Lütfen tekrar deneyin.'
            return self._render_form_with_errors(errors, post)

    def _render_form_with_errors(self, errors, form_data):
        """Helper method to re-render the form with errors"""
        departments = request.env['coflow.hospital.department'].sudo().search([
            ('active', '=', True)
        ], order='sequence, name')

        devices = request.env['coflow.medical.device'].sudo().search([
            ('active', '=', True)
        ], order='sequence, name')

        preference_departments = departments.filtered(lambda d: not d.is_other)

        values = {
            'departments': departments,
            'devices': devices,
            'preference_departments': preference_departments,
            'errors': errors,
            'form_data': form_data,
        }

        return request.render('website_career_application_jab.career_application_form_template', values)

    @http.route('/kariyer/tesekkurler', type='http', auth='public', website=True)
    def career_application_thank_you(self, **kwargs):
        """
        Thank you page after successful application submission.
        """
        return request.render('website_career_application_jab.career_application_thank_you_template')
