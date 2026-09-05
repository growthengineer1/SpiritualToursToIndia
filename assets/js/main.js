// Spiritual Tours to India - Main JavaScript

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

    // Toggle mobile menu
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });

        // Close menu when nav link clicked
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.add('hidden');
            });
        });
    }

    // Smooth scrolling offset for sticky header
    const headerHeight = document.getElementById('header').offsetHeight;
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const targetPosition = target.offsetTop - headerHeight;
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // FAQ Accordion Functionality
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        const icon = item.querySelector('.faq-icon');

        question.addEventListener('click', function() {
            const isOpen = !answer.classList.contains('hidden');

            // Close all other FAQs (optional - comment out if you want multiple open)
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.querySelector('.faq-answer').classList.add('hidden');
                    otherItem.querySelector('.faq-icon').classList.remove('rotate-180');
                }
            });

            // Toggle current FAQ
            if (isOpen) {
                answer.classList.add('hidden');
                icon.classList.remove('rotate-180');
            } else {
                answer.classList.remove('hidden');
                icon.classList.add('rotate-180');
            }
        });
    });

    // Form Submission with AJAX (stays on page)
    const contactForm = document.getElementById('contact-form');
    const formSuccess = document.getElementById('form-success');
    const formError = document.getElementById('form-error');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const website = document.getElementById('website')?.value.trim();
            const submitButton = contactForm.querySelector('button[type="submit"]');

            formSuccess.classList.add('hidden');
            formError.classList.add('hidden');

            if (!contactForm.checkValidity()) {
                contactForm.reportValidity();
                return false;
            }

            // Silently treat automated submissions as successful without sending
            // unsupported honeypot data to the lead API.
            if (website) {
                contactForm.reset();
                formSuccess.classList.remove('hidden');
                formSuccess.focus();
                return false;
            }

            const nameParts = name.split(/\s+/);
            const jsonData = {
                tour_title: document.getElementById('tour-interest')?.value || 'Custom Tour / General Enquiry',
                first_name: nameParts[0],
                last_name: nameParts.slice(1).join(' ') || 'Not provided',
                email: email,
                mobile: document.getElementById('phone')?.value.trim() || null,
                tour_dates_preferred: document.getElementById('travel-dates')?.value.trim() || null,
                quantity: 1,
                currency: 'USD',
                type: 'SpiritualToursToIndia',
                source_url: window.location.href,
                message: document.getElementById('message')?.value.trim() || null,
                website: website || null
            };
            
            // Disable button and show loading state
            submitButton.disabled = true;
            submitButton.textContent = 'Sending...';

            fetch(contactForm.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            })
            .then(async response => {
                const data = await response.json().catch(() => ({}));
                if (!response.ok) {
                    throw new Error(data.detail || data.message || 'We could not submit your enquiry. Please try again.');
                }
                return data;
            })
            .then(data => {
                if (data.success) {
                    // Show success message
                    formSuccess.classList.remove('hidden');
                    
                    // Reset form
                    contactForm.reset();
                    
                    // Scroll to success message
                    formSuccess.focus();
                    formSuccess.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    
                    // Hide success message after 10 seconds
                    setTimeout(() => {
                        formSuccess.classList.add('hidden');
                    }, 10000);
                } else {
                    throw new Error(data.error || data.message || 'We could not submit your enquiry. Please try again or contact us directly.');
                }
            })
            .catch(error => {
                console.error('Form submission error:', error);
                formError.textContent = error.message || 'We could not submit your enquiry. Please try again or contact us directly.';
                formError.classList.remove('hidden');
                formError.focus();
            })
            .finally(() => {
                // Re-enable button
                submitButton.disabled = false;
                submitButton.textContent = 'Send Message';
            });
        });
    }

    // Back to Top Button (Optional)
    const createBackToTop = () => {
        const backToTopBtn = document.createElement('button');
        backToTopBtn.innerHTML = `
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path>
            </svg>
        `;
        backToTopBtn.className = 'fixed bottom-8 right-8 bg-orange-600 text-white p-4 rounded-full shadow-lg hover:bg-orange-700 transition-all duration-200 opacity-0 pointer-events-none z-50';
        backToTopBtn.setAttribute('aria-label', 'Back to top');
        backToTopBtn.id = 'back-to-top';
        document.body.appendChild(backToTopBtn);

        // Show/hide button based on scroll position
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.remove('opacity-0', 'pointer-events-none');
            } else {
                backToTopBtn.classList.add('opacity-0', 'pointer-events-none');
            }
        });

        // Scroll to top on click
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    };

    createBackToTop();

    // Scroll Animations (Optional - Fade in elements on scroll)
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for fade-in animation (optional)
    document.querySelectorAll('.faq-item, .bg-white.rounded-xl, .bg-white.rounded-lg').forEach(el => {
        el.classList.add('fade-target');
        observer.observe(el);
    });
});
