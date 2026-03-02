// Company Insight - Main JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initBackToTop();
    initSmoothScroll();
    initMobileMenu();
    initTooltips();
    initLazyLoading();
});

// ===== Navbar Scroll Effect =====
function initNavbar() {
    const navbar = document.getElementById('navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        // Add scrolled class when scrolled down
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });
}

// ===== Back to Top Button =====
function initBackToTop() {
    const backToTopButton = document.getElementById('backToTop');

    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });

        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// ===== Smooth Scrolling for Anchor Links =====
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            // Skip if href is just "#"
            if (href === '#') {
                e.preventDefault();
                return;
            }

            const target = document.querySelector(href);

            if (target) {
                e.preventDefault();
                const offsetTop = target.offsetTop - 80; // Account for fixed navbar

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== Mobile Menu Toggle =====
function initMobileMenu() {
    const mobileMenuButton = document.querySelector('[data-mobile-menu-toggle]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            const isOpen = !mobileMenu.classList.contains('hidden');
            mobileMenuButton.setAttribute('aria-expanded', isOpen);
        });
    }
}

// ===== Tooltips =====
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');

    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip absolute bg-gray-900 text-white text-sm px-3 py-2 rounded shadow-lg z-50';
            tooltip.textContent = tooltipText;
            tooltip.style.top = `${this.offsetTop - 40}px`;
            tooltip.style.left = `${this.offsetLeft}px`;
            document.body.appendChild(tooltip);

            this.addEventListener('mouseleave', () => {
                tooltip.remove();
            });
        });
    });
}

// ===== Lazy Loading Images =====
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// ===== Form Validation Utilities =====
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

// ===== Show Toast Notification =====
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    const colors = {
        success: 'bg-neon-green text-deep-navy',
        error: 'bg-red-500 text-white',
        warning: 'bg-yellow-500 text-deep-navy',
        info: 'bg-electric-blue text-white'
    };

    toast.className = `fixed top-20 right-4 z-50 max-w-sm p-4 rounded-lg shadow-lg ${colors[type] || colors.info} animate-slide-in`;
    toast.innerHTML = `
        <div class="flex items-center justify-between">
            <p class="font-medium">${message}</p>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-current opacity-70 hover:opacity-100">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    document.body.appendChild(toast);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slide-out 0.3s ease-in';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// ===== Loading Spinner =====
function showLoadingSpinner(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner mx-auto';
    element.innerHTML = '';
    element.appendChild(spinner);
}

function hideLoadingSpinner(element, content) {
    element.innerHTML = content;
}

// ===== Debounce Function =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== Throttle Function =====
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ===== Local Storage Utilities =====
const storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Error saving to localStorage', e);
        }
    },
    get: (key) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error reading from localStorage', e);
            return null;
        }
    },
    remove: (key) => {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Error removing from localStorage', e);
        }
    }
};

// ===== Cookie Consent (Basic) =====
function initCookieConsent() {
    if (!storage.get('cookieConsent')) {
        const banner = document.createElement('div');
        banner.className = 'fixed bottom-0 left-0 right-0 bg-deep-navy text-white p-4 z-50';
        banner.innerHTML = `
            <div class="container mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
                <p class="text-sm">We use cookies to enhance your experience. By continuing to visit this site you agree to our use of cookies.</p>
                <button onclick="acceptCookies()" class="px-6 py-2 bg-electric-blue hover:bg-vibrant-cyan rounded-lg font-medium transition-colors">
                    Accept
                </button>
            </div>
        `;
        document.body.appendChild(banner);
    }
}

function acceptCookies() {
    storage.set('cookieConsent', true);
    document.querySelector('[onclick="acceptCookies()"]').closest('div').remove();
}

// ===== Utility: Format Date =====
function formatDate(date, format = 'long') {
    const d = new Date(date);
    const options = format === 'short'
        ? { month: 'short', day: 'numeric', year: 'numeric' }
        : { month: 'long', day: 'numeric', year: 'numeric' };

    return d.toLocaleDateString('en-US', options);
}

// ===== Utility: Truncate Text =====
function truncateText(text, length = 100) {
    if (text.length <= length) return text;
    return text.substring(0, length) + '...';
}

// ===== Export functions for use in other scripts =====
window.CompanyInsight = {
    showToast,
    validateEmail,
    validatePhone,
    showLoadingSpinner,
    hideLoadingSpinner,
    debounce,
    throttle,
    storage,
    formatDate,
    truncateText
};

// Initialize cookie consent
// Uncomment when ready to use
// initCookieConsent();

console.log('Company Insight - Website loaded successfully');
