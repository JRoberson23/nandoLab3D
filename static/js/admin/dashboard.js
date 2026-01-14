// static/js/admin/dashboard.js - VERSÃO CORRIGIDA
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard NandoLab 3D Admin carregado');
    
    // Inicializar sidebar toggle (usando o mesmo do commons.js ou base_admin.html)
    initDashboardFunctions();
    
    // Carregar dados do dashboard
    loadDashboardData();
});

function initDashboardFunctions() {
    // Botão de refresh
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            loadDashboardData().finally(() => {
                this.innerHTML = '<i class="fas fa-sync-alt"></i>';
            });
        });
    }
    
    // Cards clicáveis
    document.querySelectorAll('.stat-card').forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            if (target) window.location.href = target;
        });
    });
}

async function loadDashboardData() {
    try {
        // Aqui você faria uma requisição para sua API
        // Por enquanto, vamos usar dados mock
        updateStatistics({
            projetos: 0,
            pedidos_pendentes: 2,
            clientes: 0,
            depoimentos: 0
        });
        
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        showAlert('Erro ao carregar dados do dashboard', 'danger');
    }
}

function updateStatistics(data) {
    // Atualizar os contadores
    const counters = {
        'total-projetos': data.projetos,
        'pending-orders': data.pedidos_pendentes,
        'total-clientes': data.clientes,
        'total-depoimentos': data.depoimentos
    };
    
    for (const [id, value] of Object.entries(counters)) {
        const element = document.getElementById(id);
        if (element) {
            animateCounter(element, value);
        }
    }
}

function animateCounter(element, target) {
    let current = 0;
    const duration = 1000;
    const increment = target / (duration / 16);
    
    const update = () => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
        } else {
            element.textContent = Math.floor(current);
            requestAnimationFrame(update);
        }
    };
    
    update();
}

function showAlert(message, type = 'info') {
    const container = document.getElementById('admin-alert-container');
    const alert = document.getElementById('admin-alert-message');
    
    if (container && alert) {
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        container.style.display = 'block';
        
        // Auto-esconder após 5 segundos
        setTimeout(() => {
            container.style.display = 'none';
        }, 5000);
    }
}

// Funções públicas
window.refreshDashboard = function() {
    loadDashboardData();
};

window.viewDetails = function(section) {
    window.location.href = `/admin/${section}`;
};