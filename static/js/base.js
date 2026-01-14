console.log('✅ base.js carregado');
console.log('Bootstrap:', typeof bootstrap !== 'undefined' ? '✅ Carregado' : '❌ Não carregado');

// Destacar menu ativo
function highlightActiveMenu() {
    const currentPath = window.location.pathname;
    const navItems = {
        '/': 'nav-home',
        '/portfolio': 'nav-portfolio',
        '/servicos': 'nav-servicos',
        '/sobre': 'nav-sobre',
        '/orcamento': 'nav-orcamento',
        '/admin/dashboard': 'nav-admin'
    };
    
    for (const [path, navId] of Object.entries(navItems)) {
        if (currentPath === path || currentPath.startsWith(path + '/')) {
            const navElement = document.getElementById(navId);
            if (navElement) {
                navElement.classList.add('active');
            }
            break;
        }
    }
}

// Mostrar alertas
function showAlert(type, message) {
    const container = document.getElementById('alert-container');
    const alertDiv = document.getElementById('alert-message');
    
    if (container && alertDiv) {
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        container.style.display = 'block';
        
        // Auto-esconder após 5 segundos
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

// Verificar alertas na URL
function checkUrlAlerts() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('success')) {
        showAlert('success', 'Sucesso! Sua mensagem foi enviada. Entraremos em contato em breve.');
    }
    if (urlParams.has('error')) {
        showAlert('danger', 'Erro! Ocorreu um problema. Tente novamente.');
    }
}

// Inicializar quando o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    highlightActiveMenu();
    checkUrlAlerts();
});