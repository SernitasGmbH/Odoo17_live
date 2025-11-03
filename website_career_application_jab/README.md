# Website Career Application Module

## Overview

This Odoo 17 module provides a comprehensive career application form on the website with extensive personal information, experience, education tracking, and document management capabilities.

## Features

* **Public Website Application Form** - Accessible at `/kariyer/basvuru`
* **Personal Information Collection** - Includes address, passport, disability status
* **Military Status Tracking** - For male applicants
* **Family Reunion Details** - Spouse and children information (up to 2 children)
* **Language Certificates** - German language level and recognition status
* **Work Experience** - Track departments and medical devices used
* **Education History** - Academic background tracking
* **Document Uploads** - With validation (max 10MB, PDF/JPG/PNG)
* **Backend Management Interface** - Complete CRUD operations

## Installation

1. Copy the `website_career_application_jab` folder to your Odoo addons directory
2. Update the apps list in Odoo
3. Install the "Website Career Application" module

## Configuration

### Master Data

The module automatically loads:
- **16 Hospital Departments** (including "Diğer")
- **15 Medical Devices** (including "Diğer")
- **16 German States** for recognition tracking

### Access Rights

- **User Group**: Can read and write applications
- **Manager Group**: Full access including delete permissions

## Usage

### Frontend (Website)

1. Navigate to `/kariyer/basvuru`
2. Fill out the comprehensive application form
3. Upload required documents
4. Submit the application
5. View thank you page at `/kariyer/tesekkurler`

### Backend (Admin)

Access the module from the main menu: **Kariyer Başvuruları**

Submenus:
- **Başvurular** → Tüm Başvurular / Deneyimler / Eğitimler / Çocuklar
- **Yapılandırma** → Hastane Bölümleri / Tıbbi Cihazlar

## Technical Details

### Models

- `coflow.career.application` - Main application record
- `coflow.career.application.experience` - Work experience
- `coflow.career.application.education` - Education history
- `coflow.career.application.child` - Children information
- `coflow.hospital.department` - Master data for hospital departments
- `coflow.medical.device` - Master data for medical devices

### Validation

The module includes comprehensive server-side validation:
- Required field validation based on conditional logic
- File size and extension validation
- Email and phone format validation
- Date validation (birth date, passport validity, etc.)
- Unique choice validation (job preferences must be different)
- Age validation (minimum 18 years)

### File Uploads

- Maximum file size: 10MB
- Allowed extensions: PDF, JPG, JPEG, PNG
- Files are stored as `ir.attachment` records

## Module Information

- **Version**: 17.0.1.0.0
- **Category**: Website
- **License**: LGPL-3
- **Author**: Coflow Teknoloji
- **Website**: https://coflow.com.tr

## Dependencies

- `website`
- `mail`

## Support

For issues and questions, please contact Coflow Teknoloji.
