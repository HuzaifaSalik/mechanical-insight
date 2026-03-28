/**
 * Newsletter subscription form handler
 */
document.addEventListener('DOMContentLoaded', function() {
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    
    newsletterForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const emailInput = form.querySelector('input[name="email"]');
            const submitBtn = form.querySelector('button[type="submit"]');
            const messageEl = form.querySelector('.newsletter-message');
            
            const email = emailInput.value.trim();
            
            // Client-side validation
            if (!email || !isValidEmail(email)) {
                showMessage(messageEl, 'Please enter a valid email address.', 'error');
                return;
            }
            
            // Disable button during submission
            submitBtn.disabled = true;
            submitBtn.textContent = 'Subscribing...';
            
            try {
                const formData = new FormData();
                formData.append('email', email);
                
                const response = await fetch('/newsletter/subscribe', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                showMessage(messageEl, data.message, data.success ? 'success' : 'error');
                
                if (data.success) {
                    emailInput.value = '';
                }
            } catch (error) {
                showMessage(messageEl, 'An error occurred. Please try again.', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Subscribe';
            }
        });
    });
    
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
    
    function showMessage(el, message, type) {
        if (el) {
            el.textContent = message;
            el.className = 'newsletter-message mt-2 text-sm ' + 
                (type === 'success' ? 'text-green-400' : 'text-red-400');
            el.style.display = 'block';
            
            setTimeout(() => { el.style.display = 'none'; }, 5000);
        }
    }
});
