/** @odoo-module **/

// Career Application Form - Multi-Step JavaScript
console.log('=== Career Application Form JS Loaded ===');

(function() {
    'use strict';

    console.log('=== IIFE Started ===');

    function initializeForm() {
        console.log('=== Initializing Form ===');

        let currentStep = 1;
        const totalSteps = 10;

        // Step names for progress bar
        const stepNames = [
            'Kişisel Bilgiler',
            'Adres ve İletişim',
            'Pasaport Bilgileri',
            'Engellilik & Askerlik',
            'Adli Sicil',
            'Aile Birleşimi',
            'Dil & Sertifikalar',
            'İş Tercihleri',
            'Deneyim & Eğitim',
            'Motivasyon & Onay'
        ];

        // Get all form steps
        const formSteps = document.querySelectorAll('.form-step');
        const nextBtn = document.getElementById('nextBtn');
        const prevBtn = document.getElementById('prevBtn');
        const submitBtn = document.getElementById('submitBtn');
        const progressBar = document.getElementById('formProgressBar');
        const progressText = document.getElementById('progressText');

        function markInvalid(target) {
            if (!target) {
                return;
            }
            if (target instanceof NodeList || Array.isArray(target)) {
                Array.from(target).forEach(markInvalid);
                return;
            }
            if (target.classList) {
                target.classList.add('is-invalid');
            }
        }

        function showStepError(stepElement, messages) {
            if (!stepElement) {
                return;
            }
            const messageList = Array.isArray(messages) ? messages.filter(Boolean) : [messages];
            if (!messageList.length) {
                return;
            }

            let errorBox = stepElement.querySelector('.step-error');
            if (!errorBox) {
                errorBox = document.createElement('div');
                errorBox.className = 'alert alert-danger step-error';
                stepElement.insertBefore(errorBox, stepElement.firstChild);
            }

            errorBox.innerHTML = messageList.map((msg) => `<div>${msg}</div>`).join('');
            errorBox.style.display = 'block';
        }

        function clearStepError(stepElement) {
            if (!stepElement) {
                return;
            }
            const errorBox = stepElement.querySelector('.step-error');
            if (errorBox) {
                errorBox.style.display = 'none';
                errorBox.textContent = '';
            }
        }

        function getField(name) {
            return document.querySelector(`[name="${name}"]`);
        }

        function getFields(name) {
            return document.querySelectorAll(`[name="${name}"]`);
        }

        function getRadioValue(name) {
            const checked = document.querySelector(`input[name="${name}"]:checked`);
            return checked ? checked.value : '';
        }

        function hasFile(input) {
            return Boolean(input && input.files && input.files.length);
        }

        // Next button click
        if (nextBtn) {
            nextBtn.addEventListener('click', function() {
                console.log('Next button clicked, current step:', currentStep);
                if (currentStep >= totalSteps) {
                    console.log('Already at last step, cannot go forward');
                    return;
                }
                const validationResult = validateStep(currentStep);
                if (validationResult.valid) {
                    currentStep++;
                    console.log('Moving to step:', currentStep);
                    showStep(currentStep);
                } else {
                    console.log('Validation failed on step:', currentStep);
                    showStep(currentStep);
                }
            });
        }

        // Previous button click
        if (prevBtn) {
            prevBtn.addEventListener('click', function() {
                console.log('Previous button clicked, current step:', currentStep);
                currentStep--;
                console.log('Moving to step:', currentStep);
                showStep(currentStep);
            });
        }

        function showStep(step) {
            console.log('showStep called with step:', step);

            // Hide all steps
            formSteps.forEach(function(formStep) {
                formStep.style.display = 'none';
                formStep.classList.remove('active');
            });

            // Show current step
            const currentStepElement = document.querySelector(`.form-step[data-step="${step}"]`);
            if (currentStepElement) {
                currentStepElement.style.display = 'block';
                currentStepElement.classList.add('active');
                console.log('Step element found and activated:', step);
            } else {
                console.error('Step element not found for step:', step);
            }

            // Update progress bar
            const progress = (step / totalSteps) * 100;
            console.log('Updating progress bar:', progress + '%', 'Step:', step, '/', totalSteps);

            if (progressBar) {
                progressBar.style.width = progress + '%';
                progressBar.setAttribute('aria-valuenow', progress);
                console.log('Progress bar width set to:', progressBar.style.width);
            } else {
                console.error('Progress bar element not found');
            }

            if (progressText) {
                const stepName = stepNames[step - 1] || `Adım ${step}`;
                const newText = `${step}/${totalSteps}: ${stepName}`;
                progressText.textContent = newText;
                console.log('Progress text updated to:', newText);
            } else {
                console.error('Progress text element not found');
            }

            // Show/hide buttons
            console.log('Button visibility - step:', step, 'totalSteps:', totalSteps);
            if (prevBtn) {
                prevBtn.style.display = step === 1 ? 'none' : 'block';
                console.log('Prev button display:', prevBtn.style.display);
            }
            if (nextBtn) {
                if (step >= totalSteps) {
                    nextBtn.style.display = 'none';
                    console.log('Next button hidden (last step)');
                } else {
                    nextBtn.style.display = 'block';
                    console.log('Next button visible');
                }
            }
            if (submitBtn) {
                if (step >= totalSteps) {
                    submitBtn.style.display = 'block';
                    console.log('Submit button visible (last step)');
                } else {
                    submitBtn.style.display = 'none';
                    console.log('Submit button hidden');
                }
            }

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function validateStep(step, options = {}) {
            const currentStepElement = document.querySelector(`.form-step[data-step="${step}"]`);
            if (!currentStepElement) {
                return { valid: true, errors: [] };
            }

            // Get all required fields in current step
            const { scroll = true } = options;
            currentStepElement.querySelectorAll('.is-invalid').forEach((el) => el.classList.remove('is-invalid'));

            const requiredFields = currentStepElement.querySelectorAll('[required]');
            let missingRequired = false;

            requiredFields.forEach((field) => {
                let fieldValid = true;

                if (field.offsetParent === null) {
                    return;
                }

                if (field.type === 'radio') {
                    const group = currentStepElement.querySelectorAll(`[name="${field.name}"]`);
                    const isChecked = Array.from(group).some((radio) => radio.checked);
                    if (!isChecked) {
                        fieldValid = false;
                        markInvalid(group);
                    }
                } else if (field.type === 'checkbox') {
                    if (!field.checked) {
                        fieldValid = false;
                        markInvalid(field);
                    }
                } else if (field.type === 'file') {
                    if (!hasFile(field)) {
                        fieldValid = false;
                        markInvalid(field);
                    }
                } else if (!field.value || !field.value.toString().trim()) {
                    fieldValid = false;
                    markInvalid(field);
                }

                if (!fieldValid) {
                    missingRequired = true;
                }
            });

            const errors = [];
            if (missingRequired) {
                errors.push('Lutfen bu adimdaki zorunlu alanlari doldurun.');
            }

            const extraErrors = runStepValidations(step);
            if (extraErrors.length) {
                extraErrors.forEach((msg) => errors.push(msg));
            }

            if (errors.length) {
                showStepError(currentStepElement, errors);
                if (scroll) {
                    currentStepElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
                return { valid: false, errors };
            }

            clearStepError(currentStepElement);
            return { valid: true, errors: [] };
        }

        function validateAllSteps() {
            for (let step = 1; step <= totalSteps; step++) {
                const result = validateStep(step, { scroll: false });
                if (!result.valid) {
                    return { valid: false, firstInvalidStep: step };
                }
            }
            return { valid: true, firstInvalidStep: null };
        }

        function runStepValidations(step) {
            switch (step) {
                case 1:
                    return validatePersonalInfoStep();
                case 3:
                    return validatePassportStep();
                case 4:
                    return validateDisabilityAndMilitaryStep();
                case 5:
                    return validateCriminalRecordStep();
                case 6:
                    return validateFamilyStep();
                case 7:
                    return validateLanguageAndRecognitionStep();
                case 8:
                    return validateJobPreferencesStep();
                case 10:
                    return validateConsentStep();
                default:
                    return [];
            }
        }

        function validatePersonalInfoStep() {
            const errors = [];
            const birthDateInput = getField('birth_date');
            if (birthDateInput && birthDateInput.value) {
                const birthDate = new Date(birthDateInput.value);
                const today = new Date();
                birthDate.setHours(0, 0, 0, 0);
                today.setHours(0, 0, 0, 0);
                if (birthDate >= today) {
                    errors.push('Dogum tarihi bugunden once olmalidir!');
                    markInvalid(birthDateInput);
                } else {
                    const age = (today - birthDate) / (365.25 * 24 * 60 * 60 * 1000);
                    if (age < 18) {
                        errors.push('Basvuru sahibi en az 18 yasinda olmalidir!');
                        markInvalid(birthDateInput);
                    }
                }
            }

            const phoneInput = getField('phone');
            if (phoneInput && phoneInput.value) {
                const digits = phoneInput.value.replace(/[\s+\-()]/g, '');
                if (!/^[0-9\s+\-()]+$/.test(phoneInput.value)) {
                    errors.push('Gecersiz telefon numarasi formati!');
                    markInvalid(phoneInput);
                } else if (digits.length < 10) {
                    errors.push('Telefon numarasi en az 10 rakam icermelidir!');
                    markInvalid(phoneInput);
                }
            }

            const emailInput = getField('email');
            if (emailInput && emailInput.value) {
                const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                if (!emailRegex.test(emailInput.value)) {
                    errors.push('Gecersiz e-posta adresi formati!');
                    markInvalid(emailInput);
                }
            }

            return errors;
        }

        function validatePassportStep() {
            const errors = [];
            const passportStatus = getRadioValue('passport_has');

            if (!passportStatus) {
                errors.push('Pasaport durumu secilmelidir.');
                markInvalid(getFields('passport_has'));
                return errors;
            }

            if (passportStatus === 'evet') {
                const passportNo = getField('passport_no');
                if (!passportNo || !passportNo.value.trim()) {
                    errors.push('Pasaport var olarak isaretlendi, pasaport numarasi zorunludur!');
                    markInvalid(passportNo);
                }

                const validUntil = getField('passport_valid_until');
                if (!validUntil || !validUntil.value) {
                    errors.push('Pasaport var olarak isaretlendi, gecerlilik tarihi zorunludur!');
                    markInvalid(validUntil);
                } else {
                    const validDate = new Date(validUntil.value);
                    const today = new Date();
                    validDate.setHours(0, 0, 0, 0);
                    today.setHours(0, 0, 0, 0);
                    if (validDate < today) {
                        errors.push('Pasaport gecerlilik tarihi gecmis olamaz!');
                        markInvalid(validUntil);
                    }
                }

                const passportPhoto = getField('passport_photo');
                if (!hasFile(passportPhoto)) {
                    errors.push('Pasaport var olarak isaretlendi, pasaport fotografi zorunludur!');
                    markInvalid(passportPhoto);
                }
            }

            return errors;
        }

        function validateDisabilityAndMilitaryStep() {
            const errors = [];
            const disabilityStatus = getRadioValue('disability');

            if (!disabilityStatus) {
                errors.push('Engellilik durumu secilmelidir.');
                markInvalid(getFields('disability'));
            }

            if (disabilityStatus === 'var') {
                const disabilityNote = getField('disability_note');
                if (!disabilityNote || !disabilityNote.value.trim()) {
                    errors.push('Engellilik var olarak isaretlendi, aciklama zorunludur!');
                    markInvalid(disabilityNote);
                }
                const disabilityDoc = getField('disability_doc');
                if (!hasFile(disabilityDoc)) {
                    errors.push('Engellilik var olarak isaretlendi, belge zorunludur!');
                    markInvalid(disabilityDoc);
                }
            }

            const genderStatus = getRadioValue('gender');
            if (genderStatus === 'erkek') {
                const militaryStatus = getField('military_status');
                if (!militaryStatus || !militaryStatus.value) {
                    errors.push('Erkek basvuru sahipleri icin askerlik durumu zorunludur!');
                    markInvalid(militaryStatus);
                }

                if (militaryStatus && militaryStatus.value === 'tecilli') {
                    const postponeUntil = getField('military_postpone_until');
                    if (!postponeUntil || !postponeUntil.value) {
                        errors.push('Tecilli askerlik icin tecil bitis tarihi zorunludur!');
                        markInvalid(postponeUntil);
                    }

                    const postponeDoc = getField('military_postpone_doc');
                    if (!hasFile(postponeDoc)) {
                        errors.push('Tecilli askerlik icin tecil belgesi zorunludur!');
                        markInvalid(postponeDoc);
                    }
                }
            }

            return errors;
        }

        function validateCriminalRecordStep() {
            const errors = [];
            const criminalStatus = getRadioValue('criminal_record');

            if (!criminalStatus) {
                errors.push('Adli sicil durumu secilmelidir.');
                markInvalid(getFields('criminal_record'));
                return errors;
            }

            if (criminalStatus === 'var') {
                const criminalDoc = getField('criminal_record_doc');
                if (!hasFile(criminalDoc)) {
                    errors.push('Adli sicil belgesi zorunludur!');
                    markInvalid(criminalDoc);
                }
            }

            return errors;
        }

        function validateFamilyStep() {
            const errors = [];
            const familyStatus = getRadioValue('family_reunion');

            if (!familyStatus) {
                errors.push('Aile birlesimi durumu secilmelidir.');
                markInvalid(getFields('family_reunion'));
                return errors;
            }

            if (familyStatus === 'evet') {
                const childrenCountInput = getField('children_count');
                const childrenCountValue = parseInt(childrenCountInput && childrenCountInput.value ? childrenCountInput.value : '0', 10);
                if (Number.isNaN(childrenCountValue) || childrenCountValue < 0 || childrenCountValue > 2) {
                    errors.push('Cocuk sayisi 0 ile 2 arasinda olmalidir!');
                    markInvalid(childrenCountInput);
                }

                const hasSpouse = getField('has_spouse');
                if (hasSpouse && hasSpouse.checked) {
                    const spouseName = getField('spouse_name');
                    if (!spouseName || !spouseName.value.trim()) {
                        errors.push('Es ekle isaretlendi, es adi soyadi zorunludur!');
                        markInvalid(spouseName);
                    }

                    const spouseBirthDate = getField('spouse_birth_date');
                    if (!spouseBirthDate || !spouseBirthDate.value) {
                        errors.push('Es ekle isaretlendi, es dogum tarihi zorunludur!');
                        markInvalid(spouseBirthDate);
                    }

                    const spouseBirthPlace = getField('spouse_birth_place');
                    if (!spouseBirthPlace || !spouseBirthPlace.value.trim()) {
                        errors.push('Es ekle isaretlendi, es dogum yeri zorunludur!');
                        markInvalid(spouseBirthPlace);
                    }

                    const spousePhone = getField('spouse_phone');
                    if (!spousePhone || !spousePhone.value.trim()) {
                        errors.push('Es ekle isaretlendi, es telefon zorunludur!');
                        markInvalid(spousePhone);
                    } else if (!/^[0-9\s+\-()]+$/.test(spousePhone.value)) {
                        errors.push('Gecersiz es telefon numarasi formati!');
                        markInvalid(spousePhone);
                    }

                    const spouseEmail = getField('spouse_email');
                    if (!spouseEmail || !spouseEmail.value.trim()) {
                        errors.push('Es ekle isaretlendi, es e-posta zorunludur!');
                        markInvalid(spouseEmail);
                    } else {
                        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                        if (!emailRegex.test(spouseEmail.value)) {
                            errors.push('Gecersiz es e-posta adresi formati!');
                            markInvalid(spouseEmail);
                        }
                    }

                    const spousePassportHas = getField('spouse_passport_has');
                    if (!spousePassportHas || !spousePassportHas.value) {
                        errors.push('Es ekle isaretlendi, es pasaport durumu zorunludur!');
                        markInvalid(spousePassportHas);
                    } else if (spousePassportHas.value === 'evet') {
                        const spousePassportNo = getField('spouse_passport_no');
                        if (!spousePassportNo || !spousePassportNo.value.trim()) {
                            errors.push('Es pasaportu var olarak isaretlendi, pasaport numarasi zorunludur!');
                            markInvalid(spousePassportNo);
                        }

                        const spousePassportValid = getField('spouse_passport_valid_until');
                        if (!spousePassportValid || !spousePassportValid.value) {
                            errors.push('Es pasaportu var olarak isaretlendi, gecerlilik tarihi zorunludur!');
                            markInvalid(spousePassportValid);
                        }

                        const spousePassportPhoto = getField('spouse_passport_photo');
                        if (!hasFile(spousePassportPhoto)) {
                            errors.push('Es pasaportu var olarak isaretlendi, pasaport fotografi zorunludur!');
                            markInvalid(spousePassportPhoto);
                        }
                    }

                    const spouseGermanCertificate = getField('spouse_german_certificate');
                    if (!spouseGermanCertificate || !spouseGermanCertificate.value) {
                        errors.push('Es ekle isaretlendi, es Almanca sertifikasi durumu zorunludur!');
                        markInvalid(spouseGermanCertificate);
                    }
                }
            }

            return errors;
        }

        function validateLanguageAndRecognitionStep() {
            const errors = [];
            const certificateStatus = getRadioValue('has_language_certificate');

            if (certificateStatus === 'evet') {
                const certificateType = getField('language_certificate_type');
                if (!certificateType || !certificateType.value) {
                    errors.push('Dil sertifikasi var olarak isaretlendi, sertifika turu zorunludur!');
                    markInvalid(certificateType);
                }

                const certificateDoc = getField('language_certificate_doc');
                if (!hasFile(certificateDoc)) {
                    errors.push('Dil sertifikasi var olarak isaretlendi, sertifika belgesi zorunludur!');
                    markInvalid(certificateDoc);
                }
            }

            const recognitionStatus = getRadioValue('recognition_status');
            if (recognitionStatus === 'evet' || recognitionStatus === 'devam-ediyor') {
                const recognitionState = getField('recognition_state');
                if (!recognitionState || !recognitionState.value) {
                    errors.push('Denklik yapildi/devam ediyor olarak isaretlendi, eyalet zorunludur!');
                    markInvalid(recognitionState);
                }

                const recognitionApplied = getField('recognition_applied_at');
                if (!recognitionApplied || !recognitionApplied.value) {
                    errors.push('Denklik yapildi/devam ediyor olarak isaretlendi, basvuru tarihi zorunludur!');
                    markInvalid(recognitionApplied);
                }

                const recognitionReceived = getField('recognition_received_at');
                if (!recognitionReceived || !recognitionReceived.value) {
                    errors.push('Denklik yapildi/devam ediyor olarak isaretlendi, alis tarihi zorunludur!');
                    markInvalid(recognitionReceived);
                }
            }

            return errors;
        }

        function validateJobPreferencesStep() {
            const errors = [];
            const choice1 = getField('choice1');
            const choice2 = getField('choice2');
            const choice3 = getField('choice3');

            const selections = [choice1, choice2, choice3];
            let missingChoice = false;
            selections.forEach((field) => {
                if (!field || !field.value) {
                    missingChoice = true;
                    markInvalid(field);
                }
            });
            if (missingChoice) {
                errors.push('Uc tercih alanlarini doldurmalisiniz!');
            }

            const filledValues = selections.map((field) => (field && field.value ? field.value : '')).filter(Boolean);
            if (filledValues.length === 3) {
                const unique = new Set(filledValues);
                if (unique.size !== filledValues.length) {
                    errors.push('Uc tercih de birbirinden farkli olmalidir!');
                    markInvalid(choice1);
                    markInvalid(choice2);
                    markInvalid(choice3);
                }
            }

            return errors;
        }

        function validateConsentStep() {
            const errors = [];
            const consentCheckbox = getField('consent_ok');
            if (consentCheckbox && !consentCheckbox.checked) {
                errors.push('Basvuruyu gondermek icin onay kutusunu isaretlemelisiniz!');
                markInvalid(consentCheckbox);
            }
            return errors;
        }

        // Conditional field visibility handlers

        // Passport fields
        function togglePassportFields() {
            const passportRadios = document.querySelectorAll('input[name="passport_has"]');
            const passportFields = document.querySelector('.passport-fields');
            const checkedRadio = document.querySelector('input[name="passport_has"]:checked');

            if (passportFields) {
                passportFields.style.display = (checkedRadio && checkedRadio.value === 'evet') ? 'block' : 'none';
            }
        }

        const passportRadios = document.querySelectorAll('input[name="passport_has"]');
        passportRadios.forEach(radio => {
            radio.addEventListener('change', togglePassportFields);
        });

        // Disability fields
        function toggleDisabilityFields() {
            const checkedRadio = document.querySelector('input[name="disability"]:checked');
            const disabilityFields = document.querySelector('.disability-fields');
            if (disabilityFields) {
                disabilityFields.style.display = (checkedRadio && checkedRadio.value === 'var') ? 'block' : 'none';
            }
        }

        const disabilityRadios = document.querySelectorAll('input[name="disability"]');
        disabilityRadios.forEach(radio => {
            radio.addEventListener('change', toggleDisabilityFields);
        });
        

        // Military section (show for males)
        function toggleMilitarySection() {
            const checkedRadio = document.querySelector('input[name="gender"]:checked');
            const militarySection = document.querySelector('.military-section');
            if (militarySection) {
                militarySection.style.display = (checkedRadio && checkedRadio.value === 'erkek') ? 'block' : 'none';
            }
        }

        const genderRadios = document.querySelectorAll('input[name="gender"]');
        genderRadios.forEach(radio => {
            radio.addEventListener('change', toggleMilitarySection);
        });
        

        // Military postpone fields
        function toggleMilitaryPostponeFields() {
            const militarySelect = document.querySelector('select[name="military_status"]');
            const postponeFields = document.querySelector('.military-postpone-fields');
            if (militarySelect && postponeFields) {
                postponeFields.style.display = militarySelect.value === 'tecilli' ? 'block' : 'none';
            }
        }

        const militarySelect = document.querySelector('select[name="military_status"]');
        if (militarySelect) {
            militarySelect.addEventListener('change', toggleMilitaryPostponeFields);
            
        }

        // Family reunion fields
        function toggleFamilyFields() {
            const checkedRadio = document.querySelector('input[name="family_reunion"]:checked');
            const familyFields = document.querySelector('.family-fields');
            if (familyFields) {
                familyFields.style.display = (checkedRadio && checkedRadio.value === 'evet') ? 'block' : 'none';
            }
        }

        const familyRadios = document.querySelectorAll('input[name="family_reunion"]');
        familyRadios.forEach(radio => {
            radio.addEventListener('change', toggleFamilyFields);
        });
        

        // Spouse fields
        function toggleSpouseFields() {
            const hasSpouseCheckbox = document.querySelector('input[name="has_spouse"]');
            const spouseFields = document.querySelector('.spouse-fields');
            if (spouseFields && hasSpouseCheckbox) {
                spouseFields.style.display = hasSpouseCheckbox.checked ? 'block' : 'none';
            }
        }

        const hasSpouseCheckbox = document.querySelector('input[name="has_spouse"]');
        if (hasSpouseCheckbox) {
            hasSpouseCheckbox.addEventListener('change', toggleSpouseFields);
            
        }

        // Spouse passport fields
        function toggleSpousePassportFields() {
            const spousePassportSelect = document.querySelector('select[name="spouse_passport_has"]');
            const spousePassportFields = document.querySelector('.spouse-passport-fields');
            if (spousePassportSelect && spousePassportFields) {
                spousePassportFields.style.display = spousePassportSelect.value === 'evet' ? 'block' : 'none';
            }
        }

        const spousePassportSelect = document.querySelector('select[name="spouse_passport_has"]');
        if (spousePassportSelect) {
            spousePassportSelect.addEventListener('change', toggleSpousePassportFields);
            
        }

        // Children count - dynamic generation
        const childrenCountInput = document.querySelector('input[name="children_count"]');
        if (childrenCountInput) {
            childrenCountInput.addEventListener('change', function() {
                generateChildrenFields(parseInt(this.value) || 0);
            });
        }

        function generateChildrenFields(count) {
            const container = document.getElementById('childrenContainer');
            if (!container) return;

            container.innerHTML = '';

            for (let i = 1; i <= count; i++) {
                const childHtml = `
                    <div class="child-entry mb-3 p-3 border rounded bg-light">
                        <h6 class="mb-3">${i}. Çocuk Bilgileri</h6>
                        <div class="row">
                            <div class="col-md-6 mb-2">
                                <label class="form-label">Ad Soyad <span class="text-danger">*</span></label>
                                <input type="text" class="form-control" name="child_name_${i}" required/>
                            </div>
                            <div class="col-md-3 mb-2">
                                <label class="form-label">Yaş <span class="text-danger">*</span></label>
                                <input type="number" class="form-control" name="child_age_${i}" min="0" max="25" required/>
                            </div>
                            <div class="col-md-3 mb-2">
                                <label class="form-label">Doğum Tarihi <span class="text-danger">*</span></label>
                                <input type="date" class="form-control" name="child_birth_date_${i}" required/>
                            </div>
                            <div class="col-md-6 mb-2">
                                <label class="form-label">Doğum Yeri <span class="text-danger">*</span></label>
                                <input type="text" class="form-control" name="child_birth_place_${i}" required/>
                            </div>
                            <div class="col-md-6 mb-2">
                                <label class="form-label">Pasaport Var mı? <span class="text-danger">*</span></label>
                                <select class="form-select child-passport-select" name="child_passport_has_${i}" data-child="${i}" required>
                                    <option value="">Seçiniz...</option>
                                    <option value="evet">Evet</option>
                                    <option value="hayir">Hayır</option>
                                </select>
                            </div>
                            <div class="col-md-12 child-passport-fields-${i}" style="display:none;">
                                <div class="row">
                                    <div class="col-md-4 mb-2">
                                        <label class="form-label">Pasaport No <span class="text-danger">*</span></label>
                                        <input type="text" class="form-control" name="child_passport_no_${i}"/>
                                    </div>
                                    <div class="col-md-4 mb-2">
                                        <label class="form-label">Geçerlilik <span class="text-danger">*</span></label>
                                        <input type="date" class="form-control" name="child_passport_valid_until_${i}"/>
                                    </div>
                                    <div class="col-md-4 mb-2">
                                        <label class="form-label">Pasaport Foto <span class="text-danger">*</span></label>
                                        <input type="file" class="form-control" name="child_passport_photo_${i}" accept=".pdf,.jpg,.jpeg,.png"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', childHtml);
            }

            // Add event listeners for child passport fields
            const childPassportSelects = document.querySelectorAll('.child-passport-select');
            childPassportSelects.forEach(select => {
                select.addEventListener('change', function() {
                    const childNum = this.dataset.child;
                    const passportFields = document.querySelector(`.child-passport-fields-${childNum}`);
                    if (passportFields) {
                        passportFields.style.display = this.value === 'evet' ? 'block' : 'none';
                    }
                });
            });
        }

        // Language certificate fields
        function toggleCertificateFields() {
            const checkedRadio = document.querySelector('input[name="has_language_certificate"]:checked');
            const certFields = document.querySelector('.certificate-fields');
            if (certFields) {
                certFields.style.display = (checkedRadio && checkedRadio.value === 'evet') ? 'block' : 'none';
            }
        }

        const certRadios = document.querySelectorAll('input[name="has_language_certificate"]');
        certRadios.forEach(radio => {
            radio.addEventListener('change', toggleCertificateFields);
        });
        

        // Recognition fields
        function toggleRecognitionFields() {
            const checkedRadio = document.querySelector('input[name="recognition_status"]:checked');
            const recognitionFields = document.querySelector('.recognition-fields');
            if (recognitionFields) {
                recognitionFields.style.display = (checkedRadio && (checkedRadio.value === 'evet' || checkedRadio.value === 'devam-ediyor')) ? 'block' : 'none';
            }
        }

        const recognitionRadios = document.querySelectorAll('input[name="recognition_status"]');
        recognitionRadios.forEach(radio => {
            radio.addEventListener('change', toggleRecognitionFields);
        });
        

        // Add Experience Entry
        let experienceCount = 1;
        const addExperienceBtn = document.getElementById('addExperienceBtn');
        if (addExperienceBtn) {
            addExperienceBtn.addEventListener('click', function() {
                experienceCount++;
                const container = document.getElementById('experienceContainer');
                const departments = Array.from(document.querySelectorAll('select[name="experience_departments_1"] option'))
                    .map(opt => `<option value="${opt.value}">${opt.text}</option>`).join('');
                const devices = Array.from(document.querySelectorAll('select[name="experience_devices_1"] option'))
                    .map(opt => `<option value="${opt.value}">${opt.text}</option>`).join('');

                const html = `
                    <div class="experience-entry mb-3 p-3 border rounded">
                        <button type="button" class="btn btn-sm btn-danger float-end remove-experience">Sil</button>
                        <div class="row">
                            <div class="col-md-6 mb-2">
                                <label class="form-label">Kurum Adı</label>
                                <input type="text" class="form-control" name="experience_company_${experienceCount}"/>
                            </div>
                            <div class="col-md-6 mb-2">
                                <label class="form-label">Pozisyon</label>
                                <input type="text" class="form-control" name="experience_position_${experienceCount}"/>
                            </div>
                            <div class="col-md-6 mb-2">
                                <label class="form-label">Şehir</label>
                                <input type="text" class="form-control" name="experience_city_${experienceCount}"/>
                            </div>
                            <div class="col-md-3 mb-2">
                                <label class="form-label">Başlangıç</label>
                                <input type="date" class="form-control" name="experience_date_start_${experienceCount}"/>
                            </div>
                            <div class="col-md-3 mb-2">
                                <label class="form-label">Bitiş</label>
                                <input type="date" class="form-control" name="experience_date_end_${experienceCount}"/>
                            </div>
                            <div class="col-md-12 mb-2">
                                <label class="form-label">Bölümler</label>
                                <select class="form-select" multiple="multiple" name="experience_departments_${experienceCount}" size="4">
                                    ${departments}
                                </select>
                            </div>
                            <div class="col-md-12 mb-2">
                                <label class="form-label">Cihazlar</label>
                                <select class="form-select" multiple="multiple" name="experience_devices_${experienceCount}" size="4">
                                    ${devices}
                                </select>
                            </div>
                            <div class="col-md-12 mb-2">
                                <label class="form-label">Yapılan İşler</label>
                                <textarea class="form-control" name="experience_duties_${experienceCount}" rows="2"></textarea>
                            </div>
                        </div>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', html);
            });
        }

        // Remove experience entry
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-experience')) {
                e.target.closest('.experience-entry').remove();
            }
        });

        // Add Education Entry
        let educationCount = 1;
        const addEducationBtn = document.getElementById('addEducationBtn');
        if (addEducationBtn) {
            addEducationBtn.addEventListener('click', function() {
                educationCount++;
                const container = document.getElementById('educationContainer');
                const html = `
                    <div class="education-entry mb-3 p-3 border rounded">
                        <button type="button" class="btn btn-sm btn-danger float-end remove-education">Sil</button>
                        <div class="row">
                            <div class="col-md-6 mb-2">
                                <label class="form-label">Okul Adı</label>
                                <input type="text" class="form-control" name="education_school_${educationCount}"/>
                            </div>
                            <div class="col-md-6 mb-2">
                                <label class="form-label">Şehir</label>
                                <input type="text" class="form-control" name="education_city_${educationCount}"/>
                            </div>
                            <div class="col-md-6 mb-2">
                                <label class="form-label">Başlangıç</label>
                                <input type="date" class="form-control" name="education_date_start_${educationCount}"/>
                            </div>
                            <div class="col-md-6 mb-2">
                                <label class="form-label">Bitiş</label>
                                <input type="date" class="form-control" name="education_date_end_${educationCount}"/>
                            </div>
                        </div>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', html);
            });
        }

        // Remove education entry
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-education')) {
                e.target.closest('.education-entry').remove();
            }
        });

        // Auto-fill consent name from full name
        const fullNameInput = document.getElementById('full_name');
        const consentNameInput = document.getElementById('consent_name');
        if (fullNameInput && consentNameInput) {
            fullNameInput.addEventListener('blur', function() {
                if (!consentNameInput.value) {
                    consentNameInput.value = this.value;
                }
            });
        }

        // Auto-fill consent date to today
        const consentDateInput = document.getElementById('consent_date');
        if (consentDateInput && !consentDateInput.value) {
            const today = new Date().toISOString().split('T')[0];
            consentDateInput.value = today;
        }

        // Form submission
        const form = document.getElementById('careerApplicationForm');
        if (form) {
            const liveValidate = function(e) {
                const stepElement = e.target && e.target.closest && e.target.closest('.form-step');
                if (stepElement && stepElement.dataset && stepElement.dataset.step) {
                    const stepNumber = parseInt(stepElement.dataset.step, 10);
                    if (Number.isInteger(stepNumber)) {
                        validateStep(stepNumber, { scroll: false });
                    }
                }
            };
            form.addEventListener('change', liveValidate);
            form.addEventListener('input', liveValidate);
        }

        // Submit button click handler
        if (submitBtn) {
            submitBtn.addEventListener('click', function(e) {
                console.log('Submit button clicked');
                e.preventDefault();

                const result = validateAllSteps();
                if (result.valid) {
                    console.log('Validation passed, submitting form');
                    if (form) {
                        form.submit();
                    }
                } else {
                    console.log('Validation failed');
                    if (result.firstInvalidStep) {
                        currentStep = result.firstInvalidStep;
                        showStep(currentStep);
                        validateStep(currentStep);
                    }
                }
            });
        }

        if (form) {
            form.addEventListener('submit', function(e) {
                console.log('Form submit event triggered');
                const result = validateAllSteps();
                if (!result.valid) {
                    console.log('Form validation failed, preventing submit');
                    e.preventDefault();
                    if (result.firstInvalidStep) {
                        currentStep = result.firstInvalidStep;
                        showStep(currentStep);
                        validateStep(currentStep);
                    }
                    return false;
                }
                console.log('Form validation passed, allowing submit');
                // Form will submit normally if validation passes
            });
        }

        // Initialize form after all event listeners are set up
        showStep(1);

        // Trigger all toggle functions to set initial state
        setTimeout(function() {
            togglePassportFields();
            toggleDisabilityFields();
            toggleMilitarySection();
            toggleMilitaryPostponeFields();
            toggleFamilyFields();
            toggleSpouseFields();
            toggleSpousePassportFields();
            toggleCertificateFields();
            toggleRecognitionFields();
        }, 100);

    }

    // Check if DOM is already loaded
    if (document.readyState === 'loading') {
        // DOM is still loading, wait for DOMContentLoaded
        console.log('=== Waiting for DOMContentLoaded ===');
        document.addEventListener('DOMContentLoaded', initializeForm);
    } else {
        // DOM is already loaded, run immediately
        console.log('=== DOM already loaded, initializing immediately ===');
        initializeForm();
    }

})();
