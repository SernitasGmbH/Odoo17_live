 # Website Career Application Module - Complete Structure

## Module: `website_career_application_jab`

### Directory Structure

```
website_career_application_jab/
├── __init__.py
├── __manifest__.py
├── README.md
├── MODULE_STRUCTURE.md
│
├── controllers/
│   ├── __init__.py
│   └── main.py                          # Web controller for public form (GET/POST)
│
├── models/
│   ├── __init__.py
│   ├── master_data.py                   # Hospital departments & medical devices
│   ├── child.py                         # Child information model
│   ├── job_experience.py                # Work experience model
│   ├── job_education.py                 # Education history model
│   └── job_application.py               # Main application model (400+ lines)
│
├── views/
│   ├── job_application_views.xml        # Backend views (tree, form, search)
│   └── website_form_templates.xml       # Frontend QWeb templates
│
├── data/
│   └── master_data.xml                  # Seed data (departments & devices)
│
├── security/
│   ├── security.xml                     # User groups and access rights
│   └── ir.model.access.csv             # Model access control
│
└── static/
    ├── description/
    │   └── index.html                   # Module description page
    └── src/
        ├── css/
        │   └── application_form.css     # Frontend styles
        └── js/
            └── application_form.js      # Frontend JavaScript

```

## Models Overview

### 1. Main Application Model
**Model**: `coflow.career.application`
**File**: `models/job_application.py`

**Field Groups**:
- **Personal Information** (11 fields)
  - full_name, gender, birth_date, birth_place, birth_country
  - marital_status, phone, email

- **Address** (9 fields)
  - mahalle, cadde, sokak, apt_no, daire_no
  - postcode, district, city, country (selection)

- **Passport** (4 fields)
  - passport_has, passport_no, passport_valid_until, passport_photo_id

- **Disability** (3 fields)
  - disability, disability_note, disability_doc_id

- **Military Status** (3 fields - males only)
  - military_status, military_postpone_until, military_postpone_doc_id

- **Criminal Record** (2 fields)
  - criminal_record, criminal_record_doc_id

- **Family Reunion** (3 + spouse fields)
  - family_reunion, has_spouse, children_count
  - Spouse: 9 fields (name, birth info, passport, German cert)

- **Language & Certificate** (4 fields)
  - german_level, has_language_certificate
  - language_certificate_type, language_certificate_doc_id

- **Recognition (Denklik)** (4 fields)
  - recognition_status, recognition_state
  - recognition_applied_at, recognition_received_at

- **Job Preferences** (4 fields)
  - choice1, choice2, choice3, accept_other_department

- **Motivation** (2 fields)
  - motivation_text, extra_info

- **Documents** (1 field)
  - formul_a_b_doc_id

- **Consent** (3 fields)
  - consent_ok, consent_date, consent_name

- **Relations**
  - experience_ids (One2many)
  - education_ids (One2many)
  - child_ids (One2many)

**Total Fields**: 70+ fields with comprehensive validation

### 2. Experience Model
**Model**: `coflow.career.application.experience`
**File**: `models/job_experience.py`

**Fields**:
- company, position, city
- date_start, date_end, is_current
- department_ids (M2M), departments_other
- device_ids (M2M), devices_other
- duties (Text)

### 3. Education Model
**Model**: `coflow.career.application.education`
**File**: `models/job_education.py`

**Fields**:
- school, city
- date_start, date_end, is_current

### 4. Child Model
**Model**: `coflow.career.application.child`
**File**: `models/child.py`

**Fields**:
- name, age, birth_date, birth_place
- passport_has, passport_no, passport_valid_until, passport_photo_id

### 5. Master Data Models
**Models**: `coflow.hospital.department`, `coflow.medical.device`
**File**: `models/master_data.py`

**Fields**:
- name, sequence, active, is_other

## Master Data Loaded

### Hospital Departments (16)
1. Acil Servis (Notaufnahme)
2. Yoğun Bakım (Intensivstation)
3. Ameliyathane (OP)
4. Anestezi (Anästhesie)
5. Dahiliye (Innere Medizin)
6. Cerrahi (Chirurgie)
7. Kardiyoloji (Kardiologie)
8. Nöroloji (Neurologie)
9. Ortopedi (Orthopädie)
10. Pediatri / Çocuk Hastalıkları
11. Kadın Doğum (Gynäkologie)
12. Psikiyatri (Psychiatrie)
13. Radyoloji (Radiologie)
14. Onkoloji (Onkologie)
15. Geriatri / Yaşlı Bakımı
16. **Diğer** (marked as is_other=True)

### Medical Devices (15)
1. EKG
2. Defibrilatör
3. Monitör
4. Enjektör Pompası
5. Ventilatör / Solunum Cihazı
6. Ultrason Cihazı
7. BT / Tomografi
8. MR / MRI
9. Röntgen
10. Kan Gazı Cihazı
11. Pulse Oksimetre
12. Tansiyon Aleti
13. Ateş Ölçer
14. Aspiratör
15. **Diğer** (marked as is_other=True)

### German States (16)
Used for recognition (Denklik) tracking

## Validation Rules

### Server-Side Constraints (`@api.constrains`)

1. **Email Format** - Validates email addresses
2. **Phone Format** - Validates phone numbers (min 10 digits)
3. **Birth Date** - Must be in past, minimum age 18
4. **Gender-Based Military** - Required for males
5. **Military Postponement** - Required if status is 'tecilli'
6. **Passport Fields** - Required if passport_has='evet'
7. **Passport Validity** - Cannot be expired
8. **Disability Fields** - Required if disability='var'
9. **Criminal Record Doc** - Always required
10. **Children Count** - Must be 0-2
11. **Spouse Fields** - Required if has_spouse=True
12. **Spouse Passport** - Required if spouse_passport_has='evet'
13. **Children Records** - Count must match children_count
14. **Language Certificate** - Required if has_language_certificate='evet'
15. **Recognition Fields** - Required if status is 'evet' or 'devam-ediyor'
16. **Unique Choices** - choice1, choice2, choice3 must be different
17. **Consent** - consent_ok must be True
18. **Department Other** - Required if "Diğer" selected
19. **Device Other** - Required if "Diğer" selected

### File Upload Validation

- **Max Size**: 10 MB
- **Allowed Extensions**: PDF, JPG, JPEG, PNG
- **Mime Type Check**: Yes
- **Storage**: `ir.attachment` model

## Controller Routes

### 1. Application Form (GET)
**Route**: `/kariyer/basvuru`
**Method**: GET
**Auth**: public
**Action**: Renders the application form with master data

### 2. Application Submit (POST)
**Route**: `/kariyer/basvuru`
**Method**: POST
**Auth**: public
**CSRF**: Enabled
**Action**:
- Validates all fields
- Processes file uploads
- Creates application record
- Creates related records (experience, education, children)
- Redirects to thank you page

### 3. Thank You Page
**Route**: `/kariyer/tesekkurler`
**Method**: GET
**Auth**: public
**Action**: Displays thank you message

## Backend Menu Structure

```
Kariyer Başvuruları (Root Menu)
├── Başvurular
│   ├── Tüm Başvurular       → action_career_application
│   ├── Deneyimler           → action_career_application_experience
│   ├── Eğitimler            → action_career_application_education
│   └── Çocuklar             → action_career_application_child
│
└── Yapılandırma
    ├── Hastane Bölümleri    → action_hospital_department
    └── Tıbbi Cihazlar       → action_medical_device
```

## Security Groups

1. **Career Application User** (`group_career_application_user`)
   - Read/Write access to all models
   - Cannot delete records

2. **Career Application Manager** (`group_career_application_manager`)
   - Full access (Read/Write/Create/Delete)
   - Inherits User group permissions

## Installation Steps

1. Copy module to Odoo addons directory
2. Update apps list: `odoo-bin -u all -d your_database`
3. Install module from Apps menu
4. Master data will be automatically loaded
5. Access form at: `http://your-domain/kariyer/basvuru`

## Module Metadata

- **Name**: Website Career Application
- **Version**: 17.0.1.0.0
- **Category**: Website
- **License**: LGPL-3
- **Author**: Coflow Teknoloji
- **Website**: https://coflow.com.tr
- **Depends**: website, mail

## Key Features Summary

✅ Comprehensive personal data collection
✅ Conditional field visibility (passport, military, family, etc.)
✅ File upload with validation
✅ Multiple experience entries
✅ Multiple education entries
✅ Up to 2 children with full details
✅ Spouse information tracking
✅ German language level and certificates
✅ Recognition (Denklik) status
✅ Job preferences (3 different choices)
✅ Master data for departments and devices
✅ Backend management with filters
✅ Email and activity tracking (mail.thread)
✅ State management (draft, submitted, under_review, approved, rejected)
✅ CSRF protection
✅ Comprehensive server-side validation
✅ Thank you page after submission

## Files Created Summary

- **Python Files**: 7 files (models + controllers)
- **XML Files**: 4 files (views + data + security)
- **CSV Files**: 1 file (access rights)
- **CSS Files**: 1 file (frontend styles)
- **JS Files**: 1 file (frontend logic)
- **Documentation**: 2 files (README + this structure doc)
- **Total Lines of Code**: ~2000+ lines

## Next Steps (Optional Enhancements)

1. **Email Notifications**: Send email to applicant on submission
2. **Email to HR**: Notify HR team of new applications
3. **PDF Report**: Generate application summary PDF
4. **Advanced Search**: Add more search filters in backend
5. **Dashboard**: Create statistics dashboard for applications
6. **Workflow**: Add approval workflow with stages
7. **Portal Access**: Allow applicants to track their application status
8. **Multi-language**: Add translation support
9. **File Preview**: Add preview functionality for uploaded documents
10. **Bulk Actions**: Add bulk approve/reject functionality

---

**Module Created Successfully! ✅**

All files have been created according to the specifications in the application_form.txt file.
