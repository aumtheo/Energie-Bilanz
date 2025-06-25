/**
 * Main JavaScript file for the Energy Balance application
 * Initializes all components and handles global events
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the energy calculator if we're on a calculation page
    if (document.querySelector('input[name]')) {
        initializeCalculator();
    }

    // Initialize form validation
    initializeFormValidation();

    // Initialize navigation highlighting
    highlightCurrentNavItem();
});

/**
 * Initialize the energy calculator
 */
function initializeCalculator() {
    const inputs = document.querySelectorAll('input[name], select[name]');
    inputs.forEach(input => {
        input.addEventListener('input', debounce(updateCalculations, 500));
        input.addEventListener('change', debounce(updateCalculations, 500));
    });

    // Initial calculation
    updateCalculations();
}

/**
 * Update calculations via API call
 */
function updateCalculations() {
    showLoading();
    
    const formData = collectFormData();
    const params = new URLSearchParams(formData);
    
    fetch(`/api/berechnung/?${params}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateResults(data);
            } else {
                console.error('Calculation error:', data.error);
            }
        })
        .catch(error => {
            console.error('API call error:', error);
        })
        .finally(() => {
            hideLoading();
        });
}

/**
 * Collect form data from all inputs
 */
function collectFormData() {
    const formData = {};
    const inputs = document.querySelectorAll('input[name], select[name]');
    
    inputs.forEach(input => {
        const value = input.value.trim();
        if (value !== '') {
            formData[input.name] = value;
        }
    });

    return formData;
}

/**
 * Update result displays with calculation data
 */
function updateResults(data) {
    // Update building data
    if (data.gebaeudedaten) {
        updateElement('hoehe', data.gebaeudedaten.hoehe, 'm');
        updateElement('volumen', data.gebaeudedaten.volumen, 'm³');
        updateElement('bgf', data.gebaeudedaten.bgf, 'm²');
        updateElement('nf', data.gebaeudedaten.nf, 'm²');
    }

    // Update energy data
    if (data.nutzenergie) {
        updateElement('ne_absolut', data.nutzenergie.ne_absolut, 'kWh/a');
        updateElement('ne_spezifisch', data.nutzenergie.ne_spezifisch, 'kWh/m²a');
    }

    if (data.strombedarf) {
        updateElement('sb_absolut', data.strombedarf.sb_absolut, 'kWh/a');
        updateElement('sb_spezifisch', data.strombedarf.sb_spezifisch, 'kWh/m²a');
    }

    if (data.waermebedarf) {
        updateElement('wb_absolut', data.waermebedarf.wb_absolut, 'kWh/a');
    }

    if (data.endenergie) {
        updateElement('ee_absolut', data.endenergie.ee_absolut, 'kWh/a');
        updateElement('ee_spezifisch', data.endenergie.ee_spezifisch, 'kWh/m²a');
    }

    // Update sidebar cards
    updateSidebarCards(data);
}

/**
 * Update an element with a value and optional unit
 */
function updateElement(id, value, unit = '') {
    const elements = document.querySelectorAll(`[id^="${id}"]`);
    elements.forEach(element => {
        if (element) {
            const formattedValue = formatNumber(value);
            element.textContent = unit ? `${formattedValue} ${unit}` : formattedValue;
            
            // Add animation class
            element.classList.add('updated');
            setTimeout(() => element.classList.remove('updated'), 300);
        }
    });
}

/**
 * Update sidebar cards with calculation results
 */
function updateSidebarCards(data) {
    // Nutzenergiebedarf
    if (data.nutzenergie) {
        updateElement('if4xkh-2-2-2', data.nutzenergie.ne_absolut, 'kWh/a');
        updateElement('ilepeh-2-2-2', data.nutzenergie.ne_spezifisch, 'kWh/m²a');
    }

    // Energiebedarf
    if (data.endenergie) {
        updateElement('ihm1d4-2-2-2', data.endenergie.ee_absolut, 'kWh/a');
        updateElement('iz085c-2-2-2', data.endenergie.ee_spezifisch, 'kWh/m²a');
    }

    // Primärenergiebedarf (example - would need actual calculation)
    if (data.endenergie) {
        const primFaktor = 1.8; // Example primary energy factor
        const primAbs = data.endenergie.ee_absolut * primFaktor;
        const primSpez = data.endenergie.ee_spezifisch * primFaktor;
        
        updateElement('ivn3qd-2-2-2', primAbs.toFixed(2), 'kWh/a');
        updateElement('iwlzd1-2-2-2', primSpez.toFixed(2), 'kWh/m²a');
    }

    // Strom (Überschuss) - if PV data is available
    if (data.strombedarf) {
        updateElement('i0dy85-2-2-2-2-2', data.strombedarf.sb_absolut, 'kWh/a');
        updateElement('iw5g8h-2-2-2-2-2', data.strombedarf.sb_spezifisch, 'kWh/m²a');
    }
}

/**
 * Format a number for display
 */
function formatNumber(value) {
    if (value === undefined || value === null) return '-';
    if (typeof value !== 'number') return value;
    
    return new Intl.NumberFormat('de-DE', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(value);
}

/**
 * Show loading indicators
 */
function showLoading() {
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add('loading');
    });
}

/**
 * Hide loading indicators
 */
function hideLoading() {
    document.querySelectorAll('.card').forEach(card => {
        card.classList.remove('loading');
    });
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateForm(form)) {
                event.preventDefault();
            }
        });
    });
}

/**
 * Validate a form
 */
function validateForm(form) {
    let isValid = true;
    
    // Check required fields
    form.querySelectorAll('[required]').forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });
    
    return isValid;
}

/**
 * Highlight the current navigation item
 */
function highlightCurrentNavItem() {
    const currentPath = window.location.pathname;
    
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.parentElement.classList.add('active');
        }
    });
}

/**
 * Debounce function to limit the rate at which a function can fire
 */
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}