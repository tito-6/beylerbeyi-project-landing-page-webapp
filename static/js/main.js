// Luxury Real Estate Landing Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize components
    initializeAnimations();
    initializeForms();
    initializeToasts();
    initializeCallbackModal();
    initializeAnalytics();
    
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
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        const nav = document.querySelector('.luxury-nav');
        if (window.scrollY > 100) {
            nav.style.background = 'rgba(0,0,0,0.95)';
        } else {
            nav.style.background = 'rgba(0,0,0,0.9)';
        }
    });
});

// Initialize scroll animations
function initializeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Animate sections on scroll
    document.querySelectorAll('.value-prop, .feature-card, .unit-card, .testimonial-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
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
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
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

// Callback modal
function initializeCallbackModal() {
    const callbackModal = document.getElementById('callbackModal');
    if (callbackModal) {
        callbackModal.addEventListener('shown.bs.modal', function() {
            document.getElementById('callback_name').focus();
        });
        
        // Reset form when modal is hidden
        callbackModal.addEventListener('hidden.bs.modal', function() {
            document.getElementById('callbackForm').reset();
        });
    }
}

// Submit callback form
function submitCallback() {
    const name = document.getElementById('callback_name').value.trim();
    const phone = document.getElementById('callback_phone').value.trim();
    const language = document.getElementById('callback_language').value;
    
    if (!name || !phone) {
        showToast('Lütfen tüm alanları doldurun', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('callback_name', name);
    formData.append('callback_phone', phone);
    formData.append('language', language);
    
    fetch('/callback-request', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Geri arama talebiniz alındı. En kısa sürede arayacağız!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('callbackModal')).hide();
            
            // Track conversion
            if (typeof gtag !== 'undefined') {
                gtag('event', 'callback_request', {
                    event_category: 'engagement',
                    event_label: 'header_callback'
                });
            }
            
            if (typeof fbq !== 'undefined') {
                fbq('track', 'Lead');
            }
        } else {
            showToast('Bir hata oluştu. Lütfen tekrar deneyin.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Bir hata oluştu. Lütfen tekrar deneyin.', 'error');
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
