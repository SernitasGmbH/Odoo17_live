# -*- coding: utf-8 -*-
# License LGPL-3

import re
import base64
from odoo import models, fields, api
from odoo.exceptions import ValidationError

# Constants for selections
GENDER_SELECTION = [
    ('kadin', 'Kadın'),
    ('erkek', 'Erkek'),
    ('diger', 'Diğer'),
]

MARITAL_STATUS_SELECTION = [
    ('bekar', 'Bekar'),
    ('evli', 'Evli'),
    ('bosanmis', 'Boşanmış'),
    ('dul', 'Dul'),
]

YES_NO_SELECTION = [
    ('evet', 'Evet'),
    ('hayir', 'Hayır'),
]

MILITARY_STATUS_SELECTION = [
    ('yapildi', 'Yapıldı'),
    ('muaf', 'Muaf'),
    ('tecilli', 'Tecilli'),
]

CRIMINAL_RECORD_SELECTION = [
    ('var', 'Var'),
    ('yok', 'Yok'),
]

COUNTRY_SELECTION = [
    ('tr', 'Türkiye'),
    ('de', 'Almanya'),
    ('sy', 'Suriye'),
    ('other', 'Diğer'),
]

GERMAN_LEVEL_SELECTION = [
    ('a1', 'A1'),
    ('a2', 'A2'),
    ('b1', 'B1'),
    ('b2', 'B2'),
    ('c1', 'C1'),
    ('c2', 'C2'),
]

LANGUAGE_CERTIFICATE_TYPE_SELECTION = [
    ('goethe', 'Goethe'),
    ('osd', 'ÖSD'),
    ('telc', 'TELC'),
    ('diger', 'Diğer'),
]

RECOGNITION_STATUS_SELECTION = [
    ('hayir', 'Hayır'),
    ('evet', 'Evet'),
    ('devam-ediyor', 'Devam Ediyor'),
]

GERMAN_STATES_SELECTION = [
    ('baden-wurttemberg', 'Baden-Württemberg'),
    ('bayern', 'Bayern (Bavyera)'),
    ('berlin', 'Berlin'),
    ('brandenburg', 'Brandenburg'),
    ('bremen', 'Bremen'),
    ('hamburg', 'Hamburg'),
    ('hessen', 'Hessen'),
    ('mecklenburg-vorpommern', 'Mecklenburg-Vorpommern'),
    ('niedersachsen', 'Niedersachsen (Aşağı Saksonya)'),
    ('nordrhein-westfalen', 'Nordrhein-Westfalen'),
    ('rheinland-pfalz', 'Rheinland-Pfalz'),
    ('saarland', 'Saarland'),
    ('sachsen', 'Sachsen (Saksonya)'),
    ('sachsen-anhalt', 'Sachsen-Anhalt'),
    ('schleswig-holstein', 'Schleswig-Holstein'),
    ('thuringen', 'Thüringen'),
]

# File size limit (10 MB in bytes)
MAX_FILE_SIZE = 10 * 1024 * 1024


class CareerApplication(models.Model):
    """
    Main model for career applications submitted through the website.
    Contains comprehensive personal information, experience, education,
    and document management.
    """
    _name = 'coflow.career.application'
    _description = 'Career Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'full_name'
    _order = 'submission_date desc, id desc'

    # ==================== PERSONAL INFORMATION ====================

    full_name = fields.Char(
        string='İsim Soyisim',
        required=True,
        tracking=True,
        help='Full name of the applicant'
    )

    gender = fields.Selection(
        GENDER_SELECTION,
        string='Cinsiyet',
        required=True,
        tracking=True,
        help='Gender of the applicant'
    )

    birth_date = fields.Date(
        string='Doğum Tarihi',
        required=True,
        tracking=True,
        help='Date of birth'
    )

    birth_place = fields.Char(
        string='Doğum Yeri',
        required=True,
        help='Place of birth'
    )

    birth_country = fields.Char(
        string='Doğum Ülkesi',
        required=True,
        help='Country of birth'
    )

    # ==================== ADDRESS INFORMATION ====================

    addr_mahalle = fields.Char(
        string='Mahalle',
        required=True,
        help='Neighborhood'
    )

    addr_cadde = fields.Char(
        string='Cadde',
        required=True,
        help='Avenue/Street'
    )

    addr_sokak = fields.Char(
        string='Sokak',
        required=True,
        help='Street'
    )

    addr_apt_no = fields.Char(
        string='Apartman No',
        required=True,
        help='Apartment number'
    )

    addr_daire_no = fields.Char(
        string='Daire No',
        required=True,
        help='Flat number'
    )

    addr_postcode = fields.Char(
        string='Posta Kodu',
        required=True,
        help='Postal code'
    )

    addr_district = fields.Char(
        string='İlçe',
        required=True,
        help='District'
    )

    addr_city = fields.Char(
        string='İl',
        required=True,
        help='City'
    )

    addr_country = fields.Selection(
        COUNTRY_SELECTION,
        string='Ülke',
        required=True,
        help='Country'
    )

    # ==================== CONTACT INFORMATION ====================

    phone = fields.Char(
        string='Telefon',
        required=True,
        help='Phone number'
    )

    email = fields.Char(
        string='E-posta',
        required=True,
        help='Email address'
    )

    marital_status = fields.Selection(
        MARITAL_STATUS_SELECTION,
        string='Medeni Hal',
        required=True,
        tracking=True,
        help='Marital status'
    )

    # ==================== PASSPORT INFORMATION ====================

    passport_has = fields.Selection(
        YES_NO_SELECTION,
        string='Pasaport Var mı?',
        required=True,
        default='hayir',
        help='Does the applicant have a passport?'
    )

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

    # ==================== DISABILITY INFORMATION ====================

    disability = fields.Selection(
        [('yok', 'Yok'), ('var', 'Var')],
        string='Engellilik',
        required=True,
        default='yok',
        help='Disability status'
    )

    disability_note = fields.Text(
        string='Engellilik Açıklaması',
        help='Disability description (required if disability exists)'
    )

    disability_doc_id = fields.Many2one(
        'ir.attachment',
        string='Engellilik Belgesi',
        help='Disability certificate (required if disability exists)'
    )

    # ==================== MILITARY STATUS (For males only) ====================

    military_status = fields.Selection(
        MILITARY_STATUS_SELECTION,
        string='Askerlik Durumu',
        help='Military status (required for male applicants)'
    )

    military_postpone_until = fields.Date(
        string='Tecil Bitiş Tarihi',
        help='Military postponement end date (required if postponed)'
    )

    military_postpone_doc_id = fields.Many2one(
        'ir.attachment',
        string='Tecil Belgesi',
        help='Military postponement document (required if postponed)'
    )

    # ==================== CRIMINAL RECORD ====================

    criminal_record = fields.Selection(
        CRIMINAL_RECORD_SELECTION,
        string='Adli Sicil Kaydı',
        required=True,
        help='Criminal record status'
    )

    criminal_record_doc_id = fields.Many2one(
        'ir.attachment',
        string='Adli Sicil Belgesi',
        help='Criminal record certificate (always required)'
    )

    # ==================== FAMILY REUNION ====================

    family_reunion = fields.Selection(
        YES_NO_SELECTION,
        string='Aile Birleşimi Var mı?',
        required=True,
        default='hayir',
        help='Is there a family reunion?'
    )

    has_spouse = fields.Boolean(
        string='Eş Ekle',
        default=False,
        help='Add spouse information (only if family reunion exists)'
    )

    children_count = fields.Integer(
        string='Çocuk Sayısı',
        default=0,
        help='Number of children (0-2, only if family reunion exists)'
    )

    # ==================== SPOUSE INFORMATION ====================

    spouse_name = fields.Char(
        string='Eş Adı Soyadı',
        help='Spouse full name (required if spouse exists)'
    )

    spouse_birth_date = fields.Date(
        string='Eş Doğum Tarihi',
        help='Spouse birth date (required if spouse exists)'
    )

    spouse_birth_place = fields.Char(
        string='Eş Doğum Yeri',
        help='Spouse birth place (required if spouse exists)'
    )

    spouse_phone = fields.Char(
        string='Eş Telefon',
        help='Spouse phone number (required if spouse exists)'
    )

    spouse_email = fields.Char(
        string='Eş E-posta',
        help='Spouse email address (required if spouse exists)'
    )

    spouse_passport_has = fields.Selection(
        YES_NO_SELECTION,
        string='Eş Pasaport Var mı?',
        help='Does spouse have a passport? (required if spouse exists)'
    )

    spouse_passport_no = fields.Char(
        string='Eş Pasaport No',
        help='Spouse passport number (required if spouse has passport)'
    )

    spouse_passport_valid_until = fields.Date(
        string='Eş Pasaport Geçerlilik',
        help='Spouse passport validity (required if spouse has passport)'
    )

    spouse_passport_photo_id = fields.Many2one(
        'ir.attachment',
        string='Eş Pasaport Fotoğrafı',
        help='Spouse passport photo (required if spouse has passport)'
    )

    spouse_german_certificate = fields.Selection(
        YES_NO_SELECTION,
        string='Eş Almanca Sertifikası',
        help='Does spouse have German certificate? (required if spouse exists)'
    )

    # ==================== CHILDREN ====================

    child_ids = fields.One2many(
        'coflow.career.application.child',
        'application_id',
        string='Çocuklar',
        help='Children information (max 2)'
    )

    # ==================== LANGUAGE & CERTIFICATE ====================

    german_level = fields.Selection(
        GERMAN_LEVEL_SELECTION,
        string='Almanca Seviyesi',
        required=True,
        tracking=True,
        help='German language level'
    )

    has_language_certificate = fields.Selection(
        YES_NO_SELECTION,
        string='Dil Sertifikası Var mı?',
        required=True,
        default='hayir',
        help='Has language certificate?'
    )

    language_certificate_type = fields.Selection(
        LANGUAGE_CERTIFICATE_TYPE_SELECTION,
        string='Dil Sertifikası Türü',
        help='Language certificate type (required if certificate exists)'
    )

    language_certificate_doc_id = fields.Many2one(
        'ir.attachment',
        string='Dil Sertifikası Belgesi',
        help='Language certificate document (required if certificate exists)'
    )

    # ==================== RECOGNITION (Denklik) ====================

    recognition_status = fields.Selection(
        RECOGNITION_STATUS_SELECTION,
        string='Denklik Yapıldı mı?',
        required=True,
        default='hayir',
        help='Recognition status'
    )

    recognition_state = fields.Selection(
        GERMAN_STATES_SELECTION,
        string='Denklik Eyaleti',
        help='Recognition state (required if recognition done or in progress)'
    )

    recognition_applied_at = fields.Date(
        string='Denklik Başvuru Tarihi',
        help='Recognition application date (required if recognition done or in progress)'
    )

    recognition_received_at = fields.Date(
        string='Denklik Alış Tarihi',
        help='Recognition received date (required if recognition done or in progress)'
    )

    # ==================== JOB PREFERENCES ====================

    choice1 = fields.Many2one(
        'coflow.hospital.department',
        string='1. Tercih',
        required=True,
        domain="[('is_other', '=', False)]",
        help='First preference (cannot be "Diğer")'
    )

    choice2 = fields.Many2one(
        'coflow.hospital.department',
        string='2. Tercih',
        required=True,
        domain="[('is_other', '=', False)]",
        help='Second preference (cannot be "Diğer")'
    )

    choice3 = fields.Many2one(
        'coflow.hospital.department',
        string='3. Tercih',
        required=True,
        domain="[('is_other', '=', False)]",
        help='Third preference (cannot be "Diğer")'
    )

    accept_other_department = fields.Boolean(
        string='Farklı Birimde Çalışmayı Kabul Eder misiniz?',
        default=False,
        help='Accept working in a different department?'
    )

    # ==================== MOTIVATION & EXTRA INFO ====================

    motivation_text = fields.Text(
        string='Motivasyon Metni',
        required=True,
        help='Motivation text explaining why you want to work'
    )

    extra_info = fields.Text(
        string='Ek Bilgiler',
        help='Additional information (optional)'
    )

    # ==================== DOCUMENTS ====================

    formul_a_b_doc_id = fields.Many2one(
        'ir.attachment',
        string='Formül A/B Belgesi',
        help='Formul A/B document (PDF)'
    )

    # ==================== CONSENT ====================

    consent_ok = fields.Boolean(
        string='Onay',
        required=True,
        default=False,
        help='Consent checkbox (must be checked)'
    )

    consent_date = fields.Date(
        string='Onay Tarihi',
        required=True,
        default=fields.Date.context_today,
        help='Consent date'
    )

    consent_name = fields.Char(
        string='Onay İsim',
        required=True,
        help='Name for consent (defaults to full_name)'
    )

    # ==================== TECHNICAL FIELDS ====================

    experience_ids = fields.One2many(
        'coflow.career.application.experience',
        'application_id',
        string='Deneyimler',
        help='Work experience records'
    )

    education_ids = fields.One2many(
        'coflow.career.application.education',
        'application_id',
        string='Eğitimler',
        help='Education records'
    )

    submission_date = fields.Datetime(
        string='Başvuru Tarihi',
        default=fields.Datetime.now,
        readonly=True,
        tracking=True,
        help='Date and time when the application was submitted'
    )

    state = fields.Selection([
        ('draft', 'Taslak'),
        ('submitted', 'Gönderildi'),
        ('under_review', 'İnceleniyor'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    ], string='Durum', default='submitted', tracking=True,
       help='Application status')

    # ==================== COMPUTE METHODS ====================

    @api.onchange('full_name')
    def _onchange_full_name(self):
        """Auto-fill consent name with full name"""
        if self.full_name and not self.consent_name:
            self.consent_name = self.full_name

    # ==================== VALIDATION METHODS ====================

    @api.constrains('email')
    def _check_email(self):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError('Geçersiz e-posta adresi formatı!')

    @api.constrains('phone')
    def _check_phone(self):
        """Validate phone format"""
        phone_regex = r'^[\d\s\+\-\(\)]+$'
        for record in self:
            if record.phone and not re.match(phone_regex, record.phone):
                raise ValidationError('Geçersiz telefon numarası formatı!')
            if record.phone and len(record.phone.replace(' ', '').replace('+', '').replace('-', '').replace('(', '').replace(')', '')) < 10:
                raise ValidationError('Telefon numarası en az 10 rakam içermelidir!')

    @api.constrains('spouse_email')
    def _check_spouse_email(self):
        """Validate spouse email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for record in self:
            if record.spouse_email and not re.match(email_regex, record.spouse_email):
                raise ValidationError('Geçersiz eş e-posta adresi formatı!')

    @api.constrains('spouse_phone')
    def _check_spouse_phone(self):
        """Validate spouse phone format"""
        phone_regex = r'^[\d\s\+\-\(\)]+$'
        for record in self:
            if record.spouse_phone and not re.match(phone_regex, record.spouse_phone):
                raise ValidationError('Geçersiz eş telefon numarası formatı!')

    @api.constrains('birth_date')
    def _check_birth_date(self):
        """Validate birth date is in the past and applicant is old enough"""
        for record in self:
            if record.birth_date:
                if record.birth_date >= fields.Date.today():
                    raise ValidationError('Doğum tarihi bugünden önce olmalıdır!')

                # Check minimum age (e.g., 18 years)
                age = (fields.Date.today() - record.birth_date).days / 365.25
                if age < 18:
                    raise ValidationError('Başvuru sahibi en az 18 yaşında olmalıdır!')

    @api.constrains('gender', 'military_status')
    def _check_military_status(self):
        """Validate military status for male applicants"""
        for record in self:
            if record.gender == 'erkek' and not record.military_status:
                raise ValidationError('Erkek başvuru sahipleri için askerlik durumu zorunludur!')

    @api.constrains('military_status', 'military_postpone_until', 'military_postpone_doc_id')
    def _check_military_postponement(self):
        """Validate military postponement fields"""
        for record in self:
            if record.military_status == 'tecilli':
                if not record.military_postpone_until:
                    raise ValidationError('Tecilli askerlik için tecil bitiş tarihi zorunludur!')
                if not record.military_postpone_doc_id:
                    raise ValidationError('Tecilli askerlik için tecil belgesi zorunludur!')

    @api.constrains('passport_has', 'passport_no', 'passport_valid_until', 'passport_photo_id')
    def _check_passport_fields(self):
        """Validate passport fields"""
        for record in self:
            if record.passport_has == 'evet':
                if not record.passport_no:
                    raise ValidationError('Pasaport var olarak işaretlendi, pasaport numarası zorunludur!')
                if not record.passport_valid_until:
                    raise ValidationError('Pasaport var olarak işaretlendi, geçerlilik tarihi zorunludur!')
                if not record.passport_photo_id:
                    raise ValidationError('Pasaport var olarak işaretlendi, pasaport fotoğrafı zorunludur!')

    @api.constrains('passport_valid_until')
    def _check_passport_validity(self):
        """Check that passport is not expired"""
        for record in self:
            if record.passport_valid_until and record.passport_valid_until < fields.Date.today():
                raise ValidationError('Pasaport geçerlilik tarihi geçmiş olamaz!')

    @api.constrains('disability', 'disability_note', 'disability_doc_id')
    def _check_disability_fields(self):
        """Validate disability fields"""
        for record in self:
            if record.disability == 'var':
                if not record.disability_note:
                    raise ValidationError('Engellilik var olarak işaretlendi, açıklama zorunludur!')
                if not record.disability_doc_id:
                    raise ValidationError('Engellilik var olarak işaretlendi, belge zorunludur!')

    @api.constrains('criminal_record', 'criminal_record_doc_id')
    def _check_criminal_record(self):
        """Validate criminal record document is always provided"""
        for record in self:
            if record.criminal_record and not record.criminal_record_doc_id:
                raise ValidationError('Adli sicil belgesi zorunludur!')

    @api.constrains('family_reunion', 'children_count')
    def _check_children_count(self):
        """Validate children count"""
        for record in self:
            if record.family_reunion == 'evet':
                if record.children_count < 0 or record.children_count > 2:
                    raise ValidationError('Çocuk sayısı 0-2 arasında olmalıdır!')

    @api.constrains('family_reunion', 'has_spouse', 'spouse_name', 'spouse_birth_date',
                    'spouse_birth_place', 'spouse_phone', 'spouse_email',
                    'spouse_passport_has', 'spouse_german_certificate')
    def _check_spouse_fields(self):
        """Validate spouse fields"""
        for record in self:
            if record.family_reunion == 'evet' and record.has_spouse:
                if not record.spouse_name:
                    raise ValidationError('Eş ekle işaretlendi, eş adı soyadı zorunludur!')
                if not record.spouse_birth_date:
                    raise ValidationError('Eş ekle işaretlendi, eş doğum tarihi zorunludur!')
                if not record.spouse_birth_place:
                    raise ValidationError('Eş ekle işaretlendi, eş doğum yeri zorunludur!')
                if not record.spouse_phone:
                    raise ValidationError('Eş ekle işaretlendi, eş telefon zorunludur!')
                if not record.spouse_email:
                    raise ValidationError('Eş ekle işaretlendi, eş e-posta zorunludur!')
                if not record.spouse_passport_has:
                    raise ValidationError('Eş ekle işaretlendi, eş pasaport durumu zorunludur!')
                if not record.spouse_german_certificate:
                    raise ValidationError('Eş ekle işaretlendi, eş Almanca sertifikası durumu zorunludur!')

    @api.constrains('spouse_passport_has', 'spouse_passport_no',
                    'spouse_passport_valid_until', 'spouse_passport_photo_id')
    def _check_spouse_passport(self):
        """Validate spouse passport fields"""
        for record in self:
            if record.spouse_passport_has == 'evet':
                if not record.spouse_passport_no:
                    raise ValidationError('Eş pasaportu var olarak işaretlendi, pasaport numarası zorunludur!')
                if not record.spouse_passport_valid_until:
                    raise ValidationError('Eş pasaportu var olarak işaretlendi, geçerlilik tarihi zorunludur!')
                if not record.spouse_passport_photo_id:
                    raise ValidationError('Eş pasaportu var olarak işaretlendi, pasaport fotoğrafı zorunludur!')

    @api.constrains('family_reunion', 'children_count', 'child_ids')
    def _check_children_records(self):
        """Validate that number of child records matches children_count"""
        for record in self:
            if record.family_reunion == 'evet':
                if len(record.child_ids) != record.children_count:
                    raise ValidationError(
                        f'Çocuk sayısı {record.children_count} olarak belirtildi, '
                        f'ancak {len(record.child_ids)} çocuk kaydı var!'
                    )

    @api.constrains('has_language_certificate', 'language_certificate_type', 'language_certificate_doc_id')
    def _check_language_certificate(self):
        """Validate language certificate fields"""
        for record in self:
            if record.has_language_certificate == 'evet':
                if not record.language_certificate_type:
                    raise ValidationError('Dil sertifikası var olarak işaretlendi, sertifika türü zorunludur!')
                if not record.language_certificate_doc_id:
                    raise ValidationError('Dil sertifikası var olarak işaretlendi, sertifika belgesi zorunludur!')

    @api.constrains('recognition_status', 'recognition_state',
                    'recognition_applied_at', 'recognition_received_at')
    def _check_recognition_fields(self):
        """Validate recognition fields"""
        for record in self:
            if record.recognition_status in ('evet', 'devam-ediyor'):
                if not record.recognition_state:
                    raise ValidationError('Denklik yapıldı/devam ediyor olarak işaretlendi, eyalet zorunludur!')
                if not record.recognition_applied_at:
                    raise ValidationError('Denklik yapıldı/devam ediyor olarak işaretlendi, başvuru tarihi zorunludur!')
                if not record.recognition_received_at:
                    raise ValidationError('Denklik yapıldı/devam ediyor olarak işaretlendi, alış tarihi zorunludur!')

    @api.constrains('choice1', 'choice2', 'choice3')
    def _check_choices_unique(self):
        """Validate that all three choices are different"""
        for record in self:
            choices = [record.choice1.id, record.choice2.id, record.choice3.id]
            if len(choices) != len(set(choices)):
                raise ValidationError('Üç tercih de birbirinden farklı olmalıdır!')

    @api.constrains('consent_ok')
    def _check_consent(self):
        """Validate that consent is checked"""
        for record in self:
            if not record.consent_ok:
                raise ValidationError('Başvuruyu göndermek için onay kutusunu işaretlemelisiniz!')

    # ==================== CRUD METHODS ====================

    @api.model
    def create(self, vals):
        """Override create to set consent_name from full_name if not provided"""
        if 'full_name' in vals and 'consent_name' not in vals:
            vals['consent_name'] = vals['full_name']
        return super(CareerApplication, self).create(vals)

    def write(self, vals):
        """Override write to update consent_name if full_name changes"""
        if 'full_name' in vals and 'consent_name' not in vals:
            vals['consent_name'] = vals['full_name']
        return super(CareerApplication, self).write(vals)
