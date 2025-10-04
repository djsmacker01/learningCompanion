

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

        this.addSkipLink();
        

        this.addARIALandmarks();
        

        this.addLiveRegions();
        

        this.setupFocusManagement();
    }

    setupMobileFeatures() {

        this.detectMobileDevice();
        

        this.setupTouchEvents();
        

        this.setupViewportHandling();
        

        this.setupDeviceOrientation();
    }

    setupOfflineDetection() {

        window.addEventListener('online', () => {
            this.handleOnlineStatus(true);
        });

        window.addEventListener('offline', () => {
            this.handleOnlineStatus(false);
        });


        this.handleOnlineStatus(navigator.onLine);
    }

    setupKeyboardNavigation() {

        document.addEventListener('keydown', (e) => {
            this.handleKeyboardNavigation(e);
        });


        this.setupTabNavigation();
        

        this.setupArrowKeyNavigation();
        

        this.setupEscapeKeyHandling();
    }

    setupScreenReaderSupport() {

        this.addScreenReaderAnnouncements();
        

        this.setupARIALiveRegions();
        

        this.addSemanticHTML();
    }

    setupHighContrastMode() {

        if (window.matchMedia('(prefers-contrast: high)').matches) {
            this.enableHighContrast();
        }


        window.matchMedia('(prefers-contrast: high)').addEventListener('change', (e) => {
            if (e.matches) {
                this.enableHighContrast();
            } else {
                this.disableHighContrast();
            }
        });
    }

    setupTextScaling() {

        const textSize = this.getTextSizePreference();
        this.applyTextScaling(textSize);


        this.setupTextSizeListener();
    }

    setupReducedMotion() {

        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.enableReducedMotion();
        }


        window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
            if (e.matches) {
                this.enableReducedMotion();
            } else {
                this.disableReducedMotion();
            }
        });
    }

    setupColorBlindFriendly() {

        const isColorBlindFriendly = this.getColorBlindFriendlyPreference();
        if (isColorBlindFriendly) {
            this.enableColorBlindFriendly();
        }
    }

    setupFocusManagement() {

        this.addFocusIndicators();
        

        this.setupFocusTrapping();
        

        this.setupFocusRestoration();
    }

    setupTouchTargets() {

        this.ensureMinimumTouchTargets();
        

        this.addTouchFeedback();
    }

    setupSkipLinks() {

        this.addSkipToMainLink();
        

        this.addSkipToNavigationLink();
    }

    setupARIALabels() {

        this.addARIALabels();
        

        this.addARIADescriptions();
        

        this.addARIALiveRegions();
    }

    setupLiveRegions() {

        this.addStatusLiveRegion();
        

        this.addAlertLiveRegion();
        

        this.addLogLiveRegion();
    }

    setupErrorHandling() {

        this.setupAccessibilityErrorHandling();
        

        this.setupErrorRecovery();
    }


    addSkipLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'skip-link';
        skipLink.setAttribute('aria-label', 'Skip to main content');
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    addARIALandmarks() {

        const main = document.querySelector('main');
        if (main) {
            main.setAttribute('role', 'main');
            main.id = 'main-content';
        }


        const navs = document.querySelectorAll('nav');
        navs.forEach((nav, index) => {
            nav.setAttribute('role', 'navigation');
            nav.setAttribute('aria-label', `Navigation ${index + 1}`);
        });


        const header = document.querySelector('header');
        if (header) {
            header.setAttribute('role', 'banner');
        }


        const footer = document.querySelector('footer');
        if (footer) {
            footer.setAttribute('role', 'contentinfo');
        }
    }

    addLiveRegions() {

        const statusRegion = document.createElement('div');
        statusRegion.id = 'status-live-region';
        statusRegion.setAttribute('aria-live', 'polite');
        statusRegion.setAttribute('aria-atomic', 'true');
        statusRegion.className = 'sr-only';
        document.body.appendChild(statusRegion);


        const alertRegion = document.createElement('div');
        alertRegion.id = 'alert-live-region';
        alertRegion.setAttribute('aria-live', 'assertive');
        alertRegion.setAttribute('aria-atomic', 'true');
        alertRegion.className = 'sr-only';
        document.body.appendChild(alertRegion);
    }

    setupFocusManagement() {

        document.addEventListener('focusin', (e) => {
            e.target.classList.add('focus-visible');
        });

        document.addEventListener('focusout', (e) => {
            e.target.classList.remove('focus-visible');
        });
    }


    detectMobileDevice() {
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        if (isMobile) {
            document.body.classList.add('mobile-device');
        }
    }

    setupTouchEvents() {

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

        window.addEventListener('resize', () => {
            this.handleViewportChange();
        });


        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.handleViewportChange();
            }, 100);
        });
    }

    setupDeviceOrientation() {

        if (window.DeviceOrientationEvent) {
            window.addEventListener('deviceorientation', (e) => {
                this.handleDeviceOrientation(e);
            });
        }
    }


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


    handleKeyboardNavigation(e) {

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

        const focusableElements = document.querySelectorAll(
            'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );

        focusableElements.forEach((element, index) => {
            element.setAttribute('tabindex', index + 1);
        });
    }

    setupArrowKeyNavigation() {

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                this.handleArrowKeyNavigation(e);
            }
        });
    }

    setupEscapeKeyHandling() {

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.handleEscapeKey();
            }
        });
    }


    addScreenReaderAnnouncements() {

        this.setupDynamicAnnouncements();
    }

    setupARIALiveRegions() {

        const liveRegions = document.querySelectorAll('[aria-live]');
        liveRegions.forEach(region => {
            this.setupLiveRegion(region);
        });
    }

    addSemanticHTML() {

        this.addSemanticElements();
    }


    enableHighContrast() {
        document.body.classList.add('high-contrast');
    }

    disableHighContrast() {
        document.body.classList.remove('high-contrast');
    }


    getTextSizePreference() {
        return localStorage.getItem('text-size') || 'medium';
    }

    applyTextScaling(size) {
        document.body.className = document.body.className.replace(/text-\w+-size/g, '');
        document.body.classList.add(`text-${size}-size`);
    }

    setupTextSizeListener() {

        window.addEventListener('storage', (e) => {
            if (e.key === 'text-size') {
                this.applyTextScaling(e.newValue);
            }
        });
    }


    enableReducedMotion() {
        document.body.classList.add('reduced-motion');
    }

    disableReducedMotion() {
        document.body.classList.remove('reduced-motion');
    }


    getColorBlindFriendlyPreference() {
        return localStorage.getItem('color-blind-friendly') === 'true';
    }

    enableColorBlindFriendly() {
        document.body.classList.add('color-blind-friendly');
    }

    disableColorBlindFriendly() {
        document.body.classList.remove('color-blind-friendly');
    }


    addFocusIndicators() {

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

        this.setupModalFocusTrapping();
    }

    setupFocusRestoration() {

        let lastFocusedElement = null;

        document.addEventListener('focusin', (e) => {
            lastFocusedElement = e.target;
        });


        this.restoreFocus = () => {
            if (lastFocusedElement) {
                lastFocusedElement.focus();
            }
        };
    }


    ensureMinimumTouchTargets() {

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

        document.addEventListener('touchstart', (e) => {
            e.target.classList.add('touch-active');
        });

        document.addEventListener('touchend', (e) => {
            setTimeout(() => {
                e.target.classList.remove('touch-active');
            }, 150);
        });
    }


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


    addARIALabels() {

        const buttons = document.querySelectorAll('button:not([aria-label])');
        buttons.forEach(button => {
            if (!button.textContent.trim()) {
                button.setAttribute('aria-label', 'Button');
            }
        });
    }

    addARIADescriptions() {

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

        const liveRegion = document.createElement('div');
        liveRegion.id = 'live-region';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        document.body.appendChild(liveRegion);
    }


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


    setupAccessibilityErrorHandling() {

        window.addEventListener('error', (e) => {
            this.handleAccessibilityError(e);
        });
    }

    setupErrorRecovery() {

        this.setupErrorRecoveryMechanisms();
    }


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

        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const closeButton = modal.querySelector('[data-bs-dismiss="modal"]');
            if (closeButton) {
                closeButton.click();
            }
        });
    }

    handleViewportChange() {

        const viewport = {
            width: window.innerWidth,
            height: window.innerHeight
        };


        if (viewport.width < 768) {
            document.body.classList.add('mobile-viewport');
        } else {
            document.body.classList.remove('mobile-viewport');
        }
    }

    handleDeviceOrientation(e) {

        const orientation = e.alpha;

    }

    handleArrowKeyNavigation(e) {

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

        region.addEventListener('DOMSubtreeModified', () => {

        });
    }

    addSemanticElements() {

        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        headings.forEach((heading, index) => {
            if (!heading.id) {
                heading.id = `heading-${index}`;
            }
        });
    }

    setupModalFocusTrapping() {

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

        window.addEventListener('unhandledrejection', (e) => {
            this.handleUnhandledRejection(e);
        });
    }

    handleAccessibilityError(e) {

        console.error('Accessibility error:', e);
        this.announceToScreenReader('An error occurred. Please try again.');
    }

    handleUnhandledRejection(e) {

        console.error('Unhandled rejection:', e);
        this.announceToScreenReader('An error occurred. Please refresh the page.');
    }

    announceNewContent(node) {

        if (node.matches('.alert, .notification, .message')) {
            const text = node.textContent.trim();
            if (text) {
                this.announceToScreenReader(text);
            }
        }
    }
}


document.addEventListener('DOMContentLoaded', () => {
    new MobileAccessibility();
});


window.MobileAccessibility = MobileAccessibility;
