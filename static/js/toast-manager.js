/**
 * Sistema de gerenciamento de toasts para a aplicação Case Bem
 * Utiliza Bootstrap 5.3 Toast component
 */

class ToastManager {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // Criar container de toasts se não existir
        if (!document.getElementById('toast-container')) {
            this.createContainer();
        }
        this.container = document.getElementById('toast-container');
    }

    createContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        container.style.marginTop = '80px'; // Abaixo do cabeçalho
        document.body.appendChild(container);
    }

    /**
     * Exibe um toast
     * @param {string} message - Mensagem a ser exibida
     * @param {string} type - Tipo do toast (success, danger, warning, info, alert)
     * @param {number} duration - Duração em ms (0 = não remove automaticamente)
     */
    show(message, type = 'info', duration = 5000) {
        const toast = this.createToast(message, type);
        this.container.appendChild(toast);

        // Inicializar o toast do Bootstrap
        const bsToast = new bootstrap.Toast(toast, {
            autohide: duration > 0,
            delay: duration
        });

        // Remover o elemento do DOM após ser escondido
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });

        bsToast.show();
        return bsToast;
    }

    createToast(message, type) {
        const toastId = 'toast-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);

        // Mapear tipos para classes do Bootstrap
        const typeClasses = {
            'success': 'text-bg-success',
            'danger': 'text-bg-danger',
            'warning': 'text-bg-warning',
            'info': 'text-bg-info',
            'alert': 'text-bg-primary'
        };

        const bgClass = typeClasses[type] || 'text-bg-info';

        // Mapear tipos para ícones
        const typeIcons = {
            'success': '✓',
            'danger': '✕',
            'warning': '⚠',
            'info': 'ℹ',
            'alert': '!'
        };

        const icon = typeIcons[type] || 'ℹ';

        const toastHtml = `
            <div class="toast ${bgClass}" role="alert" aria-live="assertive" aria-atomic="true" id="${toastId}">
                <div class="toast-header">
                    <span class="me-2">${icon}</span>
                    <strong class="me-auto">${this.getTypeTitle(type)}</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Fechar"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;

        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = toastHtml;
        return tempDiv.firstElementChild;
    }

    getTypeTitle(type) {
        const titles = {
            'success': 'Sucesso',
            'danger': 'Erro',
            'warning': 'Aviso',
            'info': 'Informação',
            'alert': 'Alerta'
        };
        return titles[type] || 'Notificação';
    }

    // Métodos de conveniência
    success(message, duration = 5000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 7000) {
        return this.show(message, 'danger', duration);
    }

    warning(message, duration = 6000) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration = 5000) {
        return this.show(message, 'info', duration);
    }

    alert(message, duration = 6000) {
        return this.show(message, 'alert', duration);
    }

    // Limpar todos os toasts
    clear() {
        const toasts = this.container.querySelectorAll('.toast');
        toasts.forEach(toast => {
            const bsToast = bootstrap.Toast.getInstance(toast);
            if (bsToast) {
                bsToast.hide();
            }
        });
    }
}

// Instância global
window.toastManager = new ToastManager();

// Função global para facilitar o uso
window.showToast = function(message, type = 'info', duration = 5000) {
    return window.toastManager.show(message, type, duration);
};

// Funções de conveniência globais
window.showSuccess = function(message, duration = 5000) {
    return window.toastManager.success(message, duration);
};

window.showError = function(message, duration = 7000) {
    return window.toastManager.error(message, duration);
};

window.showWarning = function(message, duration = 6000) {
    return window.toastManager.warning(message, duration);
};

window.showInfo = function(message, duration = 5000) {
    return window.toastManager.info(message, duration);
};

window.showAlert = function(message, duration = 6000) {
    return window.toastManager.alert(message, duration);
};