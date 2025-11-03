# -*- coding: utf-8 -*-
{
    'name': 'Website Career Application',
    'version': '17.0.1.0.6',
    'category': 'Website',
    'summary': 'Career Application Form for Website with comprehensive candidate data collection',
    'description': """
        Website Career Application Module
        ==================================
        This module provides a comprehensive career application form on the website
        with extensive personal information, experience, education tracking and
        document management capabilities.

        Features:
        ---------
        * Public website application form
        * Personal information collection (address, passport, disability, etc.)
        * Military status tracking (for male applicants)
        * Family reunion details (spouse and children)
        * Language certificates and recognition status
        * Work experience with departments and medical devices
        * Education history
        * Document uploads with validation
        * Backend management interface
    """,
    'author': 'Coflow Teknoloji',
    'website': 'https://coflow.com.tr',
    'live_test_url': 'https://coflow.com.tr',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/master_data.xml',
        'views/job_application_views.xml',
        'views/website_form_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_career_application_jab/static/src/css/application_form.css',
            'website_career_application_jab/static/src/js/application_form.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
