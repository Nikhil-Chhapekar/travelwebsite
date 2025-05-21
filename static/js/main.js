// Main JavaScript file for Discovering Paradise

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize toasts
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000
        });
    });

    // Auto-hide toasts after 5 seconds
    setTimeout(function() {
        toastList.forEach(function(toast) {
            toast.hide();
        });
    }, 5000);

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Back to top button
    const backToTopButton = document.getElementById('backToTop');
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });

        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Animate elements on scroll
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');

        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            if (elementPosition < windowHeight - 50) {
                element.classList.add('animated');
            }
        });
    };

    if (document.querySelectorAll('.animate-on-scroll').length > 0) {
        window.addEventListener('scroll', animateOnScroll);
        // Trigger once on load
        animateOnScroll();
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Destination filtering
    const filterButtons = document.querySelectorAll('[data-filter]');
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));

                // Add active class to clicked button
                this.classList.add('active');

                const filterValue = this.getAttribute('data-filter');

                // Get all destination cards
                const destinationCards = document.querySelectorAll('.destination-card');

                destinationCards.forEach(card => {
                    const cardParent = card.parentElement;

                    // Show all cards if filter is 'all'
                    if (filterValue === 'all') {
                        cardParent.style.display = 'block';

                        // Add animation
                        cardParent.classList.remove('animated-card');
                        void cardParent.offsetWidth; // Trigger reflow
                        cardParent.classList.add('animated-card');
                    } else {
                        // Check if card has the filter value in its data attributes
                        const cardType = card.getAttribute('data-type') || '';

                        if (cardType.includes(filterValue)) {
                            cardParent.style.display = 'block';

                            // Add animation
                            cardParent.classList.remove('animated-card');
                            void cardParent.offsetWidth; // Trigger reflow
                            cardParent.classList.add('animated-card');
                        } else {
                            cardParent.style.display = 'none';
                        }
                    }
                });
            });
        });
    }

    // Typing animation for hero section
    const typingElement = document.querySelector('.typing-animation');
    if (typingElement) {
        const text = typingElement.textContent;
        typingElement.textContent = '';
        typingElement.style.width = '0';

        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                typingElement.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };

        // Start typing animation after a delay
        setTimeout(typeWriter, 1000);
    }

    // Date picker initialization for booking forms
    const dateInputs = document.querySelectorAll('.date-picker');
    if (dateInputs.length > 0) {
        dateInputs.forEach(input => {
            // This is a placeholder for actual date picker initialization
            // You would typically use a library like flatpickr or bootstrap-datepicker
            input.setAttribute('type', 'date');
        });
    }

    // Destination filter functionality
    const filterForm = document.getElementById('destination-filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Get form data
            const formData = new FormData(filterForm);
            const params = new URLSearchParams();

            for (const [key, value] of formData.entries()) {
                if (value) {
                    params.append(key, value);
                }
            }

            // Redirect to filtered results
            window.location.href = `${window.location.pathname}?${params.toString()}`;
        });
    }

    // Booking form validation
    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            let isValid = true;

            // Check required fields
            const requiredFields = bookingForm.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            // Check date validity
            const startDate = bookingForm.querySelector('#start_date');
            const endDate = bookingForm.querySelector('#end_date');

            if (startDate && endDate && startDate.value && endDate.value) {
                if (new Date(startDate.value) >= new Date(endDate.value)) {
                    isValid = false;
                    endDate.classList.add('is-invalid');
                    const feedbackElement = document.createElement('div');
                    feedbackElement.className = 'invalid-feedback';
                    feedbackElement.textContent = 'End date must be after start date';
                    endDate.parentNode.appendChild(feedbackElement);
                }
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    }
});
