/**
 * Real-time calculation system for building energy balance
 */

class EnergyCalculator {
    constructor() {
        this.apiUrl = '/api/berechnung/';
        this.debounceTimer = null;
        this.debounceDelay = 500; // ms
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateCalculations(); // Initial calculation
    }

    bindEvents() {
        // Bind to all input fields with name attributes
        const inputs = document.querySelectorAll('input[name], select[name]');
        inputs.forEach(input => {
            input.addEventListener('input', () => this.debouncedUpdate());
            input.addEventListener('change', () => this.debouncedUpdate());
        });
    }

    debouncedUpdate() {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.updateCalculations();
        }, this.debounceDelay);
    }

    async updateCalculations() {
        try {
            this.showLoading();
            
            const formData = this.collectFormData();
            const response = await this.makeApiCall(formData);
            
            if (response.success) {
                this.updateResults(response);
            } else {
                this.showError(response.error);
            }
        } catch (error) {
            console.error('Calculation error:', error);
            this.showError('Fehler bei der Berechnung');
        } finally {
            this.hideLoading();
        }
    }

    collectFormData() {
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

    async makeApiCall(data) {
        const params = new URLSearchParams(data);
        const response = await fetch(`${this.apiUrl}?${params}`);
        return await response.json();
    }

    updateResults(data) {
        // Update building data
        if (data.gebaeudedaten) {
            this.updateElement('ausgabe_hoehe', data.gebaeudedaten.hoehe, 'm');
            this.updateElement('ausgabe_volumen', data.gebaeudedaten.volumen, 'm³');
            this.updateElement('ausgabe_bgf', data.gebaeudedaten.bgf, 'm²');
            this.updateElement('ausgabe_nf', data.gebaeudedaten.nf, 'm²');
        }

        // Update energy data
        if (data.nutzenergie) {
            this.updateElement('ausgabe_ne_abs', data.nutzenergie.ne_absolut, 'kWh/a');
            this.updateElement('ausgabe_ne_spec', data.nutzenergie.ne_spezifisch, 'kWh/m²a');
        }

        if (data.strombedarf) {
            this.updateElement('ausgabe_sb_abs', data.strombedarf.sb_absolut, 'kWh/a');
            this.updateElement('ausgabe_sb_spec', data.strombedarf.sb_spezifisch, 'kWh/m²a');
        }

        if (data.endenergie) {
            this.updateElement('ausgabe_ee_abs', data.endenergie.ee_absolut, 'kWh/a');
            this.updateElement('ausgabe_ee_spec', data.endenergie.ee_spezifisch, 'kWh/m²a');
        }

        // Trigger custom event for other components
        document.dispatchEvent(new CustomEvent('calculationUpdate', {
            detail: data
        }));
    }

    updateElement(id, value, unit = '') {
        const element = document.getElementById(id);
        if (element) {
            const formattedValue = this.formatNumber(value);
            element.textContent = unit ? `${formattedValue} ${unit}` : formattedValue;
            
            // Add animation class
            element.classList.add('updated');
            setTimeout(() => element.classList.remove('updated'), 300);
        }
    }

    formatNumber(value) {
        if (typeof value !== 'number') return '-';
        return new Intl.NumberFormat('de-DE', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 2
        }).format(value);
    }

    showLoading() {
        const indicators = document.querySelectorAll('.calculation-result');
        indicators.forEach(el => el.classList.add('loading'));
    }

    hideLoading() {
        const indicators = document.querySelectorAll('.calculation-result');
        indicators.forEach(el => el.classList.remove('loading'));
    }

    showError(message) {
        console.error('Calculation error:', message);
        // You could show a toast notification here
    }
}

// Building type defaults for quick setup
const buildingDefaults = {
    buero: {
        tw_pro_m2: 15,
        lwt_pro_m2: 8,
        bel_pro_m2: 10,
        nutzer_pro_m2: 5
    },
    schule: {
        tw_pro_m2: 5,
        lwt_pro_m2: 6,
        bel_pro_m2: 12,
        nutzer_pro_m2: 2
    },
    heim: {
        tw_pro_m2: 25,
        lwt_pro_m2: 5,
        bel_pro_m2: 8,
        nutzer_pro_m2: 3
    }
};

// Building type selector functionality
function setupBuildingTypeSelector() {
    const selector = document.getElementById('geb_klasse');
    if (!selector) return;

    selector.addEventListener('change', function() {
        const buildingType = this.value;
        const defaults = buildingDefaults[buildingType];
        
        if (defaults) {
            Object.entries(defaults).forEach(([key, value]) => {
                const input = document.querySelector(`input[name="${key}"]`);
                if (input) {
                    input.value = value;
                    input.dispatchEvent(new Event('input'));
                }
            });
        }
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize on pages with calculation forms
    if (document.querySelector('input[name]')) {
        new EnergyCalculator();
        setupBuildingTypeSelector();
    }
});

// Export for use in other modules
window.EnergyCalculator = EnergyCalculator;
window.buildingDefaults = buildingDefaults;