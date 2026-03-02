// Company Insight - Animations with GSAP

// Wait for DOM and GSAP to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Check if GSAP is loaded
    if (typeof gsap === 'undefined') {
        console.warn('GSAP not loaded');
        return;
    }

    // Register ScrollTrigger plugin
    if (typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
    }

    // Initialize animations
    initHeroAnimations();
    initScrollAnimations();
    initParticles();
    initServiceCardAnimations();
    initCounterAnimations();
});

// ===== Hero Section Animations =====
function initHeroAnimations() {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

    // Animate hero content
    tl.from('.hero-title', {
        y: 100,
        opacity: 0,
        duration: 1,
        delay: 0.2
    })
    .from('.hero-subtitle', {
        y: 50,
        opacity: 0,
        duration: 0.8
    }, '-=0.5')
    .from('.hero-cta', {
        y: 30,
        opacity: 0,
        duration: 0.6
    }, '-=0.4')
    .from('.scroll-indicator', {
        y: 20,
        opacity: 0,
        duration: 0.5
    }, '-=0.3');
}

// ===== Scroll-triggered Animations =====
function initScrollAnimations() {
    if (typeof ScrollTrigger === 'undefined') return;

    // Animate service cards on scroll
    gsap.utils.toArray('.service-card').forEach((card, index) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 80%',
                toggleActions: 'play none none none'
            },
            y: 60,
            opacity: 0,
            duration: 0.8,
            delay: index * 0.1,
            ease: 'power2.out'
        });
    });

    // Animate portfolio cards
    gsap.utils.toArray('.portfolio-card').forEach((card, index) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 80%',
                toggleActions: 'play none none none'
            },
            scale: 0.9,
            opacity: 0,
            duration: 0.6,
            delay: index * 0.15,
            ease: 'back.out(1.7)'
        });
    });

    // Animate blog cards
    gsap.utils.toArray('.blog-card').forEach((card, index) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 80%',
                toggleActions: 'play none none none'
            },
            x: index % 2 === 0 ? -50 : 50,
            opacity: 0,
            duration: 0.8,
            ease: 'power2.out'
        });
    });

    // Parallax effect for hero background
    const heroSection = document.querySelector('#hero');
    if (heroSection) {
        gsap.to('#hero #particles', {
            scrollTrigger: {
                trigger: heroSection,
                start: 'top top',
                end: 'bottom top',
                scrub: true
            },
            y: 200,
            opacity: 0.5
        });
    }
}

// ===== Animated Particles Background =====
function initParticles() {
    const particlesContainer = document.getElementById('particles');

    if (!particlesContainer) return;

    // Create particles
    const particleCount = 50;
    const particles = [];

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 20}s`;
        particle.style.animationDuration = `${15 + Math.random() * 10}s`;

        // Random size
        const size = 1 + Math.random() * 3;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;

        particlesContainer.appendChild(particle);
        particles.push(particle);
    }

    // Mouse move effect
    document.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;

        particles.forEach((particle, index) => {
            const speed = (index % 5 + 1) * 0.5;
            gsap.to(particle, {
                x: (x - 0.5) * speed * 100,
                y: (y - 0.5) * speed * 100,
                duration: 1,
                ease: 'power2.out'
            });
        });
    });
}

// ===== Service Card Hover Animations =====
function initServiceCardAnimations() {
    const serviceCards = document.querySelectorAll('.service-card');

    serviceCards.forEach(card => {
        const icon = card.querySelector('i');

        card.addEventListener('mouseenter', () => {
            if (icon) {
                gsap.to(icon, {
                    rotation: 360,
                    scale: 1.2,
                    duration: 0.5,
                    ease: 'back.out(1.7)'
                });
            }
        });

        card.addEventListener('mouseleave', () => {
            if (icon) {
                gsap.to(icon, {
                    rotation: 0,
                    scale: 1,
                    duration: 0.3,
                    ease: 'power2.out'
                });
            }
        });
    });
}

// ===== Counter Animations =====
function initCounterAnimations() {
    const counters = document.querySelectorAll('.counter');

    if (counters.length === 0 || typeof ScrollTrigger === 'undefined') return;

    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));

        ScrollTrigger.create({
            trigger: counter,
            start: 'top 80%',
            onEnter: () => {
                gsap.to(counter, {
                    innerText: target,
                    duration: 2,
                    ease: 'power1.inOut',
                    snap: { innerText: 1 },
                    onUpdate: function() {
                        counter.innerText = Math.ceil(counter.innerText);
                    }
                });
            },
            once: true
        });
    });
}

// ===== Stagger Animation Utility =====
function staggerAnimation(selector, options = {}) {
    const defaults = {
        y: 50,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: 'power2.out'
    };

    const settings = { ...defaults, ...options };

    gsap.from(selector, settings);
}

// ===== Reveal on Scroll =====
function revealOnScroll(selector, animation = {}) {
    if (typeof ScrollTrigger === 'undefined') return;

    const defaults = {
        y: 60,
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out'
    };

    const settings = { ...defaults, ...animation };

    gsap.utils.toArray(selector).forEach(element => {
        gsap.from(element, {
            scrollTrigger: {
                trigger: element,
                start: 'top 80%',
                toggleActions: 'play none none none'
            },
            ...settings
        });
    });
}

// ===== Text Split Animation =====
function splitTextAnimation(element, options = {}) {
    const text = element.textContent;
    const chars = text.split('');

    element.textContent = '';

    chars.forEach(char => {
        const span = document.createElement('span');
        span.textContent = char === ' ' ? '\u00A0' : char;
        span.style.display = 'inline-block';
        element.appendChild(span);
    });

    const defaults = {
        y: 50,
        opacity: 0,
        duration: 0.05,
        stagger: 0.03,
        ease: 'back.out(1.7)'
    };

    const settings = { ...defaults, ...options };

    gsap.from(element.children, settings);
}

// ===== Magnetic Button Effect =====
function magneticEffect(button) {
    button.addEventListener('mousemove', (e) => {
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        gsap.to(button, {
            x: x * 0.3,
            y: y * 0.3,
            duration: 0.3,
            ease: 'power2.out'
        });
    });

    button.addEventListener('mouseleave', () => {
        gsap.to(button, {
            x: 0,
            y: 0,
            duration: 0.5,
            ease: 'elastic.out(1, 0.3)'
        });
    });
}

// Apply magnetic effect to CTA buttons
document.querySelectorAll('.btn-primary, .btn-secondary').forEach(button => {
    magneticEffect(button);
});

// ===== Page Transition =====
function pageTransition() {
    const tl = gsap.timeline();

    tl.to('body', {
        opacity: 0,
        duration: 0.3,
        ease: 'power2.inOut'
    })
    .to('body', {
        opacity: 1,
        duration: 0.3,
        ease: 'power2.inOut'
    });

    return tl;
}

// ===== Smooth Page Load =====
window.addEventListener('load', () => {
    gsap.to('body', {
        opacity: 1,
        duration: 0.5,
        ease: 'power2.out'
    });
});

// ===== Export animation functions =====
window.CompanyInsightAnimations = {
    staggerAnimation,
    revealOnScroll,
    splitTextAnimation,
    magneticEffect,
    pageTransition
};

console.log('Company Insight - Animations initialized');
