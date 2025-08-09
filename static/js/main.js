// Clean Luxury Real Estate Landing Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize components
    initializeHeroSlider();
    initializeForms();
    initializeScrollEffects();
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Clean navbar scroll effect
    window.addEventListener('scroll', function() {
        const nav = document.querySelector('.luxury-nav');
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });
});

// Initialize clean scroll effects
function initializeScrollEffects() {
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    // Observe fade-up elements
    document.querySelectorAll('.fade-up').forEach(el => {
        observer.observe(el);
    });
    
    // Animate sections on scroll
    document.querySelectorAll('.value-prop, .feature-card, .unit-card, .testimonial-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
}

// Hero Auto-Sliding Gallery
function initializeHeroSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    let currentSlide = 0;
    
    console.log('Hero slider initialized with', slides.length, 'slides');
    
    if (slides.length === 0) {
        console.warn('No hero slides found!');
        return;
    }
    
    function nextSlide() {
        console.log('Changing from slide', currentSlide, 'to', (currentSlide + 1) % slides.length);
        
        // Remove active class from current slide
        slides[currentSlide].classList.remove('active');
        
        // Move to next slide
        currentSlide = (currentSlide + 1) % slides.length;
        
        // Add active class to new slide
        slides[currentSlide].classList.add('active');
    }
    
    // Start auto-sliding
    setInterval(nextSlide, 3000); // Change slide every 3 seconds
}

// Form handling
function initializeForms() {
    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.startsWith('90')) {
                value = '+' + value;
            } else if (value.startsWith('0')) {
                value = '+90' + value.substring(1);
            } else if (!value.startsWith('+90')) {
                value = '+90' + value;
            }
            e.target.value = value;
        });
    });

    // Email validation function
    function isValidEmail(email) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email) && email.length <= 320 && !email.includes('..');
    }

    // Phone validation function
    function isValidPhone(phone) {
        const cleanPhone = phone.replace(/[\s\-\(\)\+\.]/g, '');
        const patterns = [
            /^90[0-9]{10}$/,    // +905551234567
            /^0[0-9]{10}$/,     // 05551234567
            /^5[0-9]{9}$/,      // 5551234567
            /^[0-9]{10}$/       // 10 digits
        ];
        return patterns.some(pattern => pattern.test(cleanPhone)) || 
               (cleanPhone.length >= 10 && cleanPhone.length <= 15 && /^[0-9]+$/.test(cleanPhone));
    }

    // Add validation styling
    function addValidationStyling() {
        const style = document.createElement('style');
        style.textContent = `
            .is-invalid {
                border-color: #dc3545 !important;
                box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25) !important;
            }
            .invalid-feedback {
                display: block;
                color: #dc3545;
                font-size: 0.875em;
                margin-top: 0.25rem;
            }
        `;
        document.head.appendChild(style);
    }
    addValidationStyling();

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;

            // Clear previous validation
            form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
            form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());

            // Validate name
            const nameInput = form.querySelector('input[name="name"]');
            if (nameInput) {
                const name = nameInput.value.trim();
                if (!name) {
                    showFieldError(nameInput, 'İsim gereklidir / Name is required');
                    isValid = false;
                }
            }

            // Validate phone
            const phoneInput = form.querySelector('input[name="phone"]');
            if (phoneInput) {
                const phone = phoneInput.value.trim();
                if (!phone) {
                    showFieldError(phoneInput, 'Telefon numarası gereklidir / Phone number is required');
                    isValid = false;
                } else if (!isValidPhone(phone)) {
                    showFieldError(phoneInput, 'Geçersiz telefon numarası formatı / Invalid phone number format');
                    isValid = false;
                }
            }

            // Validate email (if present and not empty)
            const emailInput = form.querySelector('input[name="email"]');
            if (emailInput && emailInput.value.trim()) {
                const email = emailInput.value.trim();
                if (!isValidEmail(email)) {
                    showFieldError(emailInput, 'Geçersiz e-posta adresi formatı / Invalid email address format');
                    isValid = false;
                }
            }

            // If validation fails, prevent submission
            if (!isValid) {
                e.preventDefault();
                return false;
            }

            // Proceed with loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Gönderiliyor...';
            }
            
            // Re-enable button after 5 seconds in case of error
            setTimeout(() => {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'Gönder';
                }
            }, 5000);
        });
    });

    // Helper function to show field error
    function showFieldError(input, message) {
        input.classList.add('is-invalid');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        input.parentNode.appendChild(errorDiv);
        input.focus();
    }

    // Store original button text
    document.querySelectorAll('button[type="submit"]').forEach(btn => {
        btn.setAttribute('data-original-text', btn.innerHTML);
    });
}

// Toast notifications
function initializeToasts() {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toastElement = document.createElement('div');
    toastElement.className = `toast ${type === 'success' ? 'bg-success' : 'bg-danger'} text-white`;
    toastElement.setAttribute('role', 'alert');
    
    toastElement.innerHTML = `
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toastElement);
    
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1050';
    document.body.appendChild(container);
    return container;
}

// Initialize analytics tracking
function initializeAnalytics() {
    // Track scroll depth
    let maxScroll = 0;
    const milestones = [25, 50, 75, 100];
    
    window.addEventListener('scroll', function() {
        const scrollPercent = Math.round((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100);
        
        if (scrollPercent > maxScroll) {
            maxScroll = scrollPercent;
            
            milestones.forEach(milestone => {
                if (scrollPercent >= milestone && !window[`scrolled_${milestone}`]) {
                    window[`scrolled_${milestone}`] = true;
                    
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'scroll_depth', {
                            event_category: 'engagement',
                            event_label: `${milestone}%`,
                            value: milestone
                        });
                    }
                }
            });
        }
    });
    
    // Track button clicks
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const text = this.textContent.trim();
            const section = this.closest('section')?.className || 'unknown';
            
            if (typeof gtag !== 'undefined') {
                gtag('event', 'button_click', {
                    event_category: 'engagement',
                    event_label: text,
                    custom_parameter_1: section
                });
            }
        });
    });
    
    // Track form submissions
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const formType = this.className.includes('quick-form') ? 'quick_form' : 'main_form';
            
            if (typeof gtag !== 'undefined') {
                gtag('event', 'form_submit', {
                    event_category: 'conversion',
                    event_label: formType
                });
            }
            
            if (typeof fbq !== 'undefined') {
                fbq('track', 'Lead');
            }
        });
    });
    
    // Track time on page
    let timeOnPage = 0;
    setInterval(() => {
        timeOnPage += 10;
        
        // Track engagement milestones
        if (timeOnPage === 30 && typeof gtag !== 'undefined') {
            gtag('event', 'time_on_page', {
                event_category: 'engagement',
                event_label: '30_seconds',
                value: 30
            });
        }
        
        if (timeOnPage === 120 && typeof gtag !== 'undefined') {
            gtag('event', 'time_on_page', {
                event_category: 'engagement',
                event_label: '2_minutes',
                value: 120
            });
        }
    }, 10000);
}

// Utility function for mobile detection
function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Enhanced WhatsApp link for mobile
document.addEventListener('click', function(e) {
    if (e.target.closest('a[href*="wa.me"]')) {
        const link = e.target.closest('a[href*="wa.me"]');
        
        if (typeof gtag !== 'undefined') {
            gtag('event', 'whatsapp_click', {
                event_category: 'engagement',
                event_label: 'contact'
            });
        }
        
        if (typeof fbq !== 'undefined') {
            fbq('track', 'Contact');
        }
    }
});

// Performance optimization
if ('loading' in HTMLImageElement.prototype) {
    // Lazy loading supported natively
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.loading = 'lazy';
    });
} else {
    // Fallback for browsers that don't support lazy loading
    const images = document.querySelectorAll('img');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src || img.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        imageObserver.observe(img);
    });
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Script error:', e.error);
    
    if (typeof gtag !== 'undefined') {
        gtag('event', 'exception', {
            description: e.error.message,
            fatal: false
        });
    }
});

// Service worker registration for better performance (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
            console.log('SW registered: ', registration);
        }).catch(function(registrationError) {
            console.log('SW registration failed: ', registrationError);
        });
    });
}

// ===== ULTRA-MODERN 2025 EFFECTS =====

// Enhanced Lead Form Handling
function selectUnit(unitType) {
    const leadForm = document.getElementById('lead-form');
    if (leadForm) {
        const interestedUnitField = leadForm.querySelector('#interested_unit');
        if (interestedUnitField) {
            interestedUnitField.value = unitType;
        }
        
        // Smooth scroll to the form
        leadForm.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
        
        // Premium highlight effect
        leadForm.style.boxShadow = '0 0 50px rgba(201, 168, 118, 0.6)';
        leadForm.style.transform = 'scale(1.02)';
        setTimeout(() => {
            leadForm.style.boxShadow = '';
            leadForm.style.transform = '';
        }, 2000);
    }
}

// Initialize Modern Effects
document.addEventListener('DOMContentLoaded', function() {
    // Create particle system
    createParticleSystem();
    
    // Initialize magnetic buttons
    initializeMagneticButtons();
    
    // Initialize tilt effects
    initializeTiltCards();
    
    // Initialize custom cursor
    initializeCustomCursor();
    
    // Initialize enhanced navbar
    initializeEnhancedNavbar();
    
    // Initialize text reveal
    initializeTextReveal();
    
    // Initialize stagger animations
    initializeStaggerAnimations();
});

// Advanced Particle System
function createParticleSystem() {
    const particlesContainer = document.querySelector('.particles-container');
    if (!particlesContainer) return;

    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 8 + 's';
        particle.style.animationDuration = (8 + Math.random() * 8) + 's';
        particlesContainer.appendChild(particle);
    }
}

// Magnetic Button Effects
function initializeMagneticButtons() {
    document.querySelectorAll('.magnetic-btn').forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px) scale(1.05)`;
        });
        
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });
}

// 3D Tilt Cards
function initializeTiltCards() {
    document.querySelectorAll('.tilt-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 15;
            const rotateY = -(x - centerX) / 15;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(20px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
}

// Custom Cursor
function initializeCustomCursor() {
    if (isMobile()) return; // Skip on mobile
    
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);
    
    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX - 10 + 'px';
        cursor.style.top = e.clientY - 10 + 'px';
    });
    
    document.querySelectorAll('a, button, .magnetic-btn').forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
    });
}

// Enhanced Navbar
function initializeEnhancedNavbar() {
    const navbar = document.querySelector('.luxury-nav');
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > 100) {
            navbar.classList.add('scrolled');
            navbar.style.background = 'rgba(0,0,0,0.98)';
            navbar.style.backdropFilter = 'blur(20px)';
        } else {
            navbar.classList.remove('scrolled');
            navbar.style.background = 'rgba(0,0,0,0.9)';
            navbar.style.backdropFilter = 'none';
        }
        
        if (currentScrollY > lastScrollY && currentScrollY > 200) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollY = currentScrollY;
    });
}

// Text Reveal Animation
function initializeTextReveal() {
    const textElements = document.querySelectorAll('.text-reveal');
    
    textElements.forEach(element => {
        const text = element.textContent;
        const words = text.split(' ');
        element.innerHTML = '';
        
        words.forEach((word, index) => {
            const span = document.createElement('span');
            span.textContent = word + ' ';
            span.style.animationDelay = `${index * 0.1}s`;
            element.appendChild(span);
        });
    });
}

// Stagger Animation Observer
function initializeStaggerAnimations() {
    const staggerContainers = document.querySelectorAll('.stagger-container');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, { threshold: 0.2 });
    
    staggerContainers.forEach(container => {
        observer.observe(container);
    });
}
