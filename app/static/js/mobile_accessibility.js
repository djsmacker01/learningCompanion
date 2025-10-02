// Mobile and Accessibility JavaScript

class MobileAccessibility {
    constructor() {
        this.init();
    }

    init() {
        this.setupAccessibilityFeatures();
        this.setupMobileFeatures();
        this.setupOfflineDetection();
        this.setupKeyboardNavigation();
        this.setupScreenReaderSupport();
        this.setupHighContrastMode();
        this.setupTextScaling();
        this.setupReducedMotion();
        this.setupColorBlindFriendly();
        this.setupFocusManagement();
        this.setupTouchTargets();
        this.setupSkipLinks();
        this.setupARIALabels();
        this.setupLiveRegions();
        this.setupErrorHandling();
    }

    setupAccessibilityFeatures() {
        // Add skip link
        this.addSkipLink();
        
        // Add ARIA landmarks
        this.addARIALandmarks();
        
        // Add live regions
        this.addLiveRegions();
        
        // Setup focus management
        this.setupFocusManagement();
    }

    setupMobileFeatures() {
        // Detect mobile device
        this.detectMobileDevice();
        
        // Setup touch events
        this.setupTouchEvents();
        
        // Setup viewport handling
        this.setupViewportHandling();
        
        // Setup device orientation
        this.setupDeviceOrientation();
    }

    setupOfflineDetection() {
        // Listen for online/offline events
        window.addEventListener('online', () => {
            this.handleOnlineStatus(true);
        });

        window.addEventListener('offline', () => {
            this.handleOnlineStatus(false);
        });

        // Check initial status
        this.handleOnlineStatus(navigator.onLine);
    }

    setupKeyboardNavigation() {
        // Add keyboard event listeners
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardNavigation(e);
        });

        // Setup tab navigation
        this.setupTabNavigation();
        
        // Setup arrow key navigation
        this.setupArrowKeyNavigation();
        
        // Setup escape key handling
        this.setupEscapeKeyHandling();
    }

    setupScreenReaderSupport() {
        // Add screen reader announcements
        this.addScreenReaderAnnouncements();
        
        // Setup ARIA live regions
        this.setupARIALiveRegions();
        
        // Add semantic HTML
        this.addSemanticHTML();
    }

    setupHighContrastMode() {
        // Check for high contrast preference
        if (window.matchMedia('(prefers-contrast: high)').matches) {
            this.enableHighContrast();
        }

        // Listen for contrast changes
        window.matchMedia('(prefers-contrast: high)').addEventListener('change', (e) => {
            if (e.matches) {
                this.enableHighContrast();
            } else {
                this.disableHighContrast();
            }
        });
    }

    setupTextScaling() {
        // Check for text scaling preference
        const textSize = this.getTextSizePreference();
        this.applyTextScaling(textSize);

        // Listen for text size changes
        this.setupTextSizeListener();
    }

    setupReducedMotion() {
        // Check for reduced motion preference
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.enableReducedMotion();
        }

        // Listen for motion changes
        window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
            if (e.matches) {
                this.enableReducedMotion();
            } else {
                this.disableReducedMotion();
            }
        });
    }

    setupColorBlindFriendly() {
        // Check for color blind friendly preference
        const isColorBlindFriendly = this.getColorBlindFriendlyPreference();
        if (isColorBlindFriendly) {
            this.enableColorBlindFriendly();
        }
    }

    setupFocusManagement() {
        // Add focus indicators
        this.addFocusIndicators();
        
        // Setup focus trapping
        this.setupFocusTrapping();
        
        // Setup focus restoration
        this.setupFocusRestoration();
    }

    setupTouchTargets() {
        // Ensure minimum touch target size
        this.ensureMinimumTouchTargets();
        
        // Add touch feedback
        this.addTouchFeedback();
    }

    setupSkipLinks() {
        // Add skip to main content link
        this.addSkipToMainLink();
        
        // Add skip to navigation link
        this.addSkipToNavigationLink();
    }

    setupARIALabels() {
        // Add ARIA labels to interactive elements
        this.addARIALabels();
        
        // Add ARIA descriptions
        this.addARIADescriptions();
        
        // Add ARIA live regions
        this.addARIALiveRegions();
    }

    setupLiveRegions() {
        // Add status live region
        this.addStatusLiveRegion();
        
        // Add alert live region
        this.addAlertLiveRegion();
        
        // Add log live region
        this.addLogLiveRegion();
    }

    setupErrorHandling() {
        // Setup error handling for accessibility features
        this.setupAccessibilityErrorHandling();
        
        // Setup error recovery
        this.setupErrorRecovery();
    }

    // Accessibility Methods
    addSkipLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'skip-link';
        skipLink.setAttribute('aria-label', 'Skip to main content');
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    addARIALandmarks() {
        // Add main landmark
        const main = document.querySelector('main');
        if (main) {
            main.setAttribute('role', 'main');
            main.id = 'main-content';
        }

        // Add navigation landmarks
        const navs = document.querySelectorAll('nav');
        navs.forEach((nav, index) => {
            nav.setAttribute('role', 'navigation');
            nav.setAttribute('aria-label', `Navigation ${index + 1}`);
        });

        // Add header landmark
        const header = document.querySelector('header');
        if (header) {
            header.setAttribute('role', 'banner');
        }

        // Add footer landmark
        const footer = document.querySelector('footer');
        if (footer) {
            footer.setAttribute('role', 'contentinfo');
        }
    }

    addLiveRegions() {
        // Add status live region
        const statusRegion = document.createElement('div');
        statusRegion.id = 'status-live-region';
        statusRegion.setAttribute('aria-live', 'polite');
        statusRegion.setAttribute('aria-atomic', 'true');
        statusRegion.className = 'sr-only';
        document.body.appendChild(statusRegion);

        // Add alert live region
        const alertRegion = document.createElement('div');
        alertRegion.id = 'alert-live-region';
        alertRegion.setAttribute('aria-live', 'assertive');
        alertRegion.setAttribute('aria-atomic', 'true');
        alertRegion.className = 'sr-only';
        document.body.appendChild(alertRegion);
    }

    setupFocusManagement() {
        // Add focus indicators
        document.addEventListener('focusin', (e) => {
            e.target.classList.add('focus-visible');
        });

        document.addEventListener('focusout', (e) => {
            e.target.classList.remove('focus-visible');
        });
    }

    // Mobile Methods
    detectMobileDevice() {
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        if (isMobile) {
            document.body.classList.add('mobile-device');
        }
    }

    setupTouchEvents() {
        // Add touch event listeners
        document.addEventListener('touchstart', (e) => {
            e.target.classList.add('touch-active');
        });

        document.addEventListener('touchend', (e) => {
            setTimeout(() => {
                e.target.classList.remove('touch-active');
            }, 150);
        });
    }

    setupViewportHandling() {
        // Handle viewport changes
        window.addEventListener('resize', () => {
            this.handleViewportChange();
        });

        // Handle orientation changes
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.handleViewportChange();
            }, 100);
        });
    }

    setupDeviceOrientation() {
        // Handle device orientation
        if (window.DeviceOrientationEvent) {
            window.addEventListener('deviceorientation', (e) => {
                this.handleDeviceOrientation(e);
            });
        }
    }

    // Offline Methods
    handleOnlineStatus(isOnline) {
        const indicator = document.getElementById('offline-indicator');
        if (indicator) {
            if (isOnline) {
                indicator.classList.add('hidden');
                this.announceToScreenReader('Connection restored');
            } else {
                indicator.classList.remove('hidden');
                this.announceToScreenReader('You are now offline');
            }
        }
    }

    // Keyboard Navigation Methods
    handleKeyboardNavigation(e) {
        // Handle specific keyboard shortcuts
        if (e.altKey && e.key === 'm') {
            e.preventDefault();
            this.focusMainContent();
        }

        if (e.altKey && e.key === 'n') {
            e.preventDefault();
            this.focusNavigation();
        }

        if (e.key === 'Escape') {
            this.handleEscapeKey();
        }
    }

    setupTabNavigation() {
        // Ensure proper tab order
        const focusableElements = document.querySelectorAll(
            'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );

        focusableElements.forEach((element, index) => {
            element.setAttribute('tabindex', index + 1);
        });
    }

    setupArrowKeyNavigation() {
        // Setup arrow key navigation for custom components
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                this.handleArrowKeyNavigation(e);
            }
        });
    }

    setupEscapeKeyHandling() {
        // Handle escape key for modals, dropdowns, etc.
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.handleEscapeKey();
            }
        });
    }

    // Screen Reader Methods
    addScreenReaderAnnouncements() {
        // Add announcements for dynamic content
        this.setupDynamicAnnouncements();
    }

    setupARIALiveRegions() {
        // Setup live regions for dynamic content
        const liveRegions = document.querySelectorAll('[aria-live]');
        liveRegions.forEach(region => {
            this.setupLiveRegion(region);
        });
    }

    addSemanticHTML() {
        // Add semantic HTML elements
        this.addSemanticElements();
    }

    // High Contrast Methods
    enableHighContrast() {
        document.body.classList.add('high-contrast');
    }

    disableHighContrast() {
        document.body.classList.remove('high-contrast');
    }

    // Text Scaling Methods
    getTextSizePreference() {
        return localStorage.getItem('text-size') || 'medium';
    }

    applyTextScaling(size) {
        document.body.className = document.body.className.replace(/text-\w+-size/g, '');
        document.body.classList.add(`text-${size}-size`);
    }

    setupTextSizeListener() {
        // Listen for text size changes
        window.addEventListener('storage', (e) => {
            if (e.key === 'text-size') {
                this.applyTextScaling(e.newValue);
            }
        });
    }

    // Reduced Motion Methods
    enableReducedMotion() {
        document.body.classList.add('reduced-motion');
    }

    disableReducedMotion() {
        document.body.classList.remove('reduced-motion');
    }

    // Color Blind Friendly Methods
    getColorBlindFriendlyPreference() {
        return localStorage.getItem('color-blind-friendly') === 'true';
    }

    enableColorBlindFriendly() {
        document.body.classList.add('color-blind-friendly');
    }

    disableColorBlindFriendly() {
        document.body.classList.remove('color-blind-friendly');
    }

    // Focus Management Methods
    addFocusIndicators() {
        // Add focus indicators to interactive elements
        const focusableElements = document.querySelectorAll(
            'a, button, input, select, textarea, [tabindex]'
        );

        focusableElements.forEach(element => {
            element.addEventListener('focus', () => {
                element.classList.add('focus-visible');
            });

            element.addEventListener('blur', () => {
                element.classList.remove('focus-visible');
            });
        });
    }

    setupFocusTrapping() {
        // Setup focus trapping for modals
        this.setupModalFocusTrapping();
    }

    setupFocusRestoration() {
        // Store and restore focus
        let lastFocusedElement = null;

        document.addEventListener('focusin', (e) => {
            lastFocusedElement = e.target;
        });

        // Restore focus when needed
        this.restoreFocus = () => {
            if (lastFocusedElement) {
                lastFocusedElement.focus();
            }
        };
    }

    // Touch Target Methods
    ensureMinimumTouchTargets() {
        // Ensure minimum 44px touch targets
        const touchTargets = document.querySelectorAll('a, button, input, select, textarea');
        touchTargets.forEach(target => {
            const rect = target.getBoundingClientRect();
            if (rect.width < 44 || rect.height < 44) {
                target.style.minWidth = '44px';
                target.style.minHeight = '44px';
            }
        });
    }

    addTouchFeedback() {
        // Add touch feedback
        document.addEventListener('touchstart', (e) => {
            e.target.classList.add('touch-active');
        });

        document.addEventListener('touchend', (e) => {
            setTimeout(() => {
                e.target.classList.remove('touch-active');
            }, 150);
        });
    }

    // Skip Link Methods
    addSkipToMainLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'skip-link';
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    addSkipToNavigationLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#navigation';
        skipLink.textContent = 'Skip to navigation';
        skipLink.className = 'skip-link';
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    // ARIA Methods
    addARIALabels() {
        // Add ARIA labels to interactive elements
        const buttons = document.querySelectorAll('button:not([aria-label])');
        buttons.forEach(button => {
            if (!button.textContent.trim()) {
                button.setAttribute('aria-label', 'Button');
            }
        });
    }

    addARIADescriptions() {
        // Add ARIA descriptions
        const formControls = document.querySelectorAll('input, select, textarea');
        formControls.forEach(control => {
            if (control.hasAttribute('aria-describedby')) {
                const descriptionId = control.getAttribute('aria-describedby');
                let description = document.getElementById(descriptionId);
                if (!description) {
                    description = document.createElement('div');
                    description.id = descriptionId;
                    description.className = 'sr-only';
                    control.parentNode.appendChild(description);
                }
            }
        });
    }

    addARIALiveRegions() {
        // Add live regions for dynamic content
        const liveRegion = document.createElement('div');
        liveRegion.id = 'live-region';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        document.body.appendChild(liveRegion);
    }

    // Live Region Methods
    addStatusLiveRegion() {
        const statusRegion = document.createElement('div');
        statusRegion.id = 'status-live-region';
        statusRegion.setAttribute('aria-live', 'polite');
        statusRegion.setAttribute('aria-atomic', 'true');
        statusRegion.className = 'sr-only';
        document.body.appendChild(statusRegion);
    }

    addAlertLiveRegion() {
        const alertRegion = document.createElement('div');
        alertRegion.id = 'alert-live-region';
        alertRegion.setAttribute('aria-live', 'assertive');
        alertRegion.setAttribute('aria-atomic', 'true');
        alertRegion.className = 'sr-only';
        document.body.appendChild(alertRegion);
    }

    addLogLiveRegion() {
        const logRegion = document.createElement('div');
        logRegion.id = 'log-live-region';
        logRegion.setAttribute('aria-live', 'polite');
        logRegion.setAttribute('aria-atomic', 'false');
        logRegion.className = 'sr-only';
        document.body.appendChild(logRegion);
    }

    // Error Handling Methods
    setupAccessibilityErrorHandling() {
        // Setup error handling for accessibility features
        window.addEventListener('error', (e) => {
            this.handleAccessibilityError(e);
        });
    }

    setupErrorRecovery() {
        // Setup error recovery mechanisms
        this.setupErrorRecoveryMechanisms();
    }

    // Utility Methods
    announceToScreenReader(message) {
        const liveRegion = document.getElementById('status-live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }

    focusMainContent() {
        const main = document.getElementById('main-content');
        if (main) {
            main.focus();
        }
    }

    focusNavigation() {
        const nav = document.querySelector('nav');
        if (nav) {
            const firstLink = nav.querySelector('a');
            if (firstLink) {
                firstLink.focus();
            }
        }
    }

    handleEscapeKey() {
        // Close modals, dropdowns, etc.
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const closeButton = modal.querySelector('[data-bs-dismiss="modal"]');
            if (closeButton) {
                closeButton.click();
            }
        });
    }

    handleViewportChange() {
        // Handle viewport changes
        const viewport = {
            width: window.innerWidth,
            height: window.innerHeight
        };

        // Update mobile class
        if (viewport.width < 768) {
            document.body.classList.add('mobile-viewport');
        } else {
            document.body.classList.remove('mobile-viewport');
        }
    }

    handleDeviceOrientation(e) {
        // Handle device orientation changes
        const orientation = e.alpha; // 0-360 degrees
        // Handle orientation changes
    }

    handleArrowKeyNavigation(e) {
        // Handle arrow key navigation
        const currentElement = document.activeElement;
        const parent = currentElement.closest('[role="menu"], [role="listbox"], [role="grid"]');
        
        if (parent) {
            const items = parent.querySelectorAll('[role="menuitem"], [role="option"], [role="gridcell"]');
            const currentIndex = Array.from(items).indexOf(currentElement);
            
            let nextIndex;
            if (e.key === 'ArrowDown') {
                nextIndex = (currentIndex + 1) % items.length;
            } else if (e.key === 'ArrowUp') {
                nextIndex = (currentIndex - 1 + items.length) % items.length;
            }
            
            if (nextIndex !== undefined) {
                items[nextIndex].focus();
                e.preventDefault();
            }
        }
    }

    setupDynamicAnnouncements() {
        // Setup announcements for dynamic content
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            this.announceNewContent(node);
                        }
                    });
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    setupLiveRegion(region) {
        // Setup live region behavior
        region.addEventListener('DOMSubtreeModified', () => {
            // Handle live region updates
        });
    }

    addSemanticElements() {
        // Add semantic HTML elements
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        headings.forEach((heading, index) => {
            if (!heading.id) {
                heading.id = `heading-${index}`;
            }
        });
    }

    setupModalFocusTrapping() {
        // Setup focus trapping for modals
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.addEventListener('shown.bs.modal', () => {
                this.trapFocus(modal);
            });
        });
    }

    trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        element.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        lastElement.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        firstElement.focus();
                        e.preventDefault();
                    }
                }
            }
        });

        firstElement.focus();
    }

    setupErrorRecoveryMechanisms() {
        // Setup error recovery mechanisms
        window.addEventListener('unhandledrejection', (e) => {
            this.handleUnhandledRejection(e);
        });
    }

    handleAccessibilityError(e) {
        // Handle accessibility errors
        console.error('Accessibility error:', e);
        this.announceToScreenReader('An error occurred. Please try again.');
    }

    handleUnhandledRejection(e) {
        // Handle unhandled promise rejections
        console.error('Unhandled rejection:', e);
        this.announceToScreenReader('An error occurred. Please refresh the page.');
    }

    announceNewContent(node) {
        // Announce new content to screen readers
        if (node.matches('.alert, .notification, .message')) {
            const text = node.textContent.trim();
            if (text) {
                this.announceToScreenReader(text);
            }
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MobileAccessibility();
});

// Export for use in other modules
window.MobileAccessibility = MobileAccessibility;
