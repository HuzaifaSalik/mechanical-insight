// Company Insight - Contact Form Handler

document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', handleContactFormSubmit);
    }
});

async function handleContactFormSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
    const formMessage = document.getElementById('formMessage');
    const originalButtonText = submitButton.value || submitButton.textContent;

    // Disable submit button
    submitButton.disabled = true;
    submitButton.value = 'Sending...';
    if (submitButton.textContent) submitButton.textContent = 'Sending...';

    // Get form data
    const formData = new FormData(form);

    try {
        // Send AJAX request
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();

        if (data.success) {
            // Success
            showFormMessage('success', data.message || 'Thank you for contacting us! We will get back to you soon.');
            form.reset();

            // Show success toast
            if (window.CompanyInsight && window.CompanyInsight.showToast) {
                window.CompanyInsight.showToast(data.message, 'success');
            }
        } else {
            // Error
            showFormMessage('error', data.message || 'An error occurred. Please try again.');

            if (window.CompanyInsight && window.CompanyInsight.showToast) {
                window.CompanyInsight.showToast(data.message || 'An error occurred', 'error');
            }
        }
    } catch (error) {
        console.error('Form submission error:', error);
        showFormMessage('error', 'An error occurred. Please try again later.');

        if (window.CompanyInsight && window.CompanyInsight.showToast) {
            window.CompanyInsight.showToast('An error occurred', 'error');
        }
    } finally {
        // Re-enable submit button
        submitButton.disabled = false;
        submitButton.value = originalButtonText;
        if (submitButton.textContent) submitButton.textContent = originalButtonText;
    }
}

function showFormMessage(type, message) {
    const formMessage = document.getElementById('formMessage');

    if (!formMessage) return;

    const colors = {
        success: 'bg-neon-green text-deep-navy',
        error: 'bg-red-500 text-white',
        warning: 'bg-yellow-500 text-deep-navy'
    };

    formMessage.className = `p-4 rounded-lg ${colors[type] || colors.success}`;
    formMessage.textContent = message;
    formMessage.classList.remove('hidden');

    // Auto-hide after 5 seconds
    setTimeout(() => {
        formMessage.classList.add('hidden');
    }, 5000);

    // Scroll to message
    formMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Client-side validation
function validateContactForm(form) {
    const name = form.querySelector('[name="name"]');
    const email = form.querySelector('[name="email"]');
    const message = form.querySelector('[name="message"]');

    let isValid = true;
    let errors = [];

    // Validate name
    if (!name.value.trim() || name.value.trim().length < 2) {
        errors.push('Please enter a valid name');
        name.classList.add('border-red-500');
        isValid = false;
    } else {
        name.classList.remove('border-red-500');
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.value.trim())) {
        errors.push('Please enter a valid email address');
        email.classList.add('border-red-500');
        isValid = false;
    } else {
        email.classList.remove('border-red-500');
    }

    // Validate message
    if (!message.value.trim() || message.value.trim().length < 10) {
        errors.push('Please enter a message (at least 10 characters)');
        message.classList.add('border-red-500');
        isValid = false;
    } else {
        message.classList.remove('border-red-500');
    }

    if (!isValid) {
        showFormMessage('error', errors.join('. '));
    }

    return isValid;
}

// Real-time validation
const emailInput = document.querySelector('[name="email"]');
if (emailInput) {
    emailInput.addEventListener('blur', function() {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (this.value && !emailRegex.test(this.value)) {
            this.classList.add('border-red-500');
        } else {
            this.classList.remove('border-red-500');
        }
    });
}

const phoneInput = document.querySelector('[name="phone"]');
if (phoneInput) {
    phoneInput.addEventListener('input', function() {
        // Format phone number as user types
        let value = this.value.replace(/\D/g, '');
        if (value.length > 10) value = value.substring(0, 10);

        if (value.length >= 6) {
            this.value = `(${value.substring(0, 3)}) ${value.substring(3, 6)}-${value.substring(6)}`;
        } else if (value.length >= 3) {
            this.value = `(${value.substring(0, 3)}) ${value.substring(3)}`;
        } else {
            this.value = value;
        }
    });
}
