// Funções comuns para área administrativa
class AdminCommon {
    constructor() {
        this.init();
    }
    
    init() {
        this.initSidebar();        // Atualizada
        this.initTableScroll();    // Nova
        this.initTouchFeedback();  // Nova
        this.initNotifications();
        this.initSearch();
        this.initKeyboardShortcuts();
        this.initLogout();
    }
    
    // Sidebar responsiva com overlay (ATUALIZADA)
    initSidebar() {
        const sidebarToggle = document.getElementById('sidebarToggle');
        const adminSidebar = document.querySelector('.admin-sidebar');
        
        if (!sidebarToggle || !adminSidebar) return;
        
        // Criar overlay se não existir
        let sidebarOverlay = document.querySelector('.sidebar-overlay');
        if (!sidebarOverlay) {
            sidebarOverlay = document.createElement('div');
            sidebarOverlay.className = 'sidebar-overlay';
            document.body.appendChild(sidebarOverlay);
        }
        
        // Abrir/fechar menu
        sidebarToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            adminSidebar.classList.toggle('active');
            sidebarOverlay.classList.toggle('active');
            document.body.style.overflow = adminSidebar.classList.contains('active') ? 'hidden' : '';
        });
        
        // Fechar menu ao clicar no overlay
        sidebarOverlay.addEventListener('click', () => {
            adminSidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
            document.body.style.overflow = '';
        });
        
        // Fechar menu ao clicar em link (mobile)
        const menuLinks = document.querySelectorAll('.sidebar-menu a');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 1200) {
                    adminSidebar.classList.remove('active');
                    sidebarOverlay.classList.remove('active');
                    document.body.style.overflow = '';
                }
            });
        });
        
        // Fechar menu ao redimensionar para desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 1200) {
                adminSidebar.classList.remove('active');
                sidebarOverlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
    
    // Detectar scroll em tabelas (NOVA)
    initTableScroll() {
        const tables = document.querySelectorAll('.table-responsive');
        
        tables.forEach(table => {
            let isScrolling;
            
            table.addEventListener('scroll', () => {
                // Adicionar classe durante scroll
                table.classList.add('scrolling');
                
                // Remover classe após parar
                clearTimeout(isScrolling);
                isScrolling = setTimeout(() => {
                    table.classList.remove('scrolling');
                }, 500);
            });
        });
    }
    
    // Feedback tátil em mobile (NOVA)
    initTouchFeedback() {
        // Apenas para dispositivos touch
        if (!('ontouchstart' in window)) return;
        
        const touchElements = document.querySelectorAll('.btn, .menu-item a, .card.clickable');
        
        touchElements.forEach(el => {
            el.addEventListener('touchstart', () => {
                el.classList.add('touch-active');
            }, { passive: true });
            
            el.addEventListener('touchend', () => {
                el.classList.remove('touch-active');
            }, { passive: true });
        });
    }
    
    // Sistema de notificações (MANTIDO)
    initNotifications() {
        const notificationBtn = document.querySelector('.notification-btn');
        if (!notificationBtn) return;
        
        notificationBtn.addEventListener('click', async () => {
            await this.loadNotifications();
        });
        
        // Carregar notificações a cada 30 segundos
        setInterval(() => {
            this.loadNotificationCount();
        }, 30000);
    }
    
    async loadNotifications() {
        try {
            const response = await fetch('/api/admin/notifications');
            const data = await response.json();
            
            const container = document.querySelector('.notifications-dropdown');
            if (container) {
                container.innerHTML = this.renderNotifications(data);
            }
        } catch (error) {
            console.error('Erro ao carregar notificações:', error);
        }
    }
    
    async loadNotificationCount() {
        try {
            const response = await fetch('/api/admin/notifications/count');
            const data = await response.json();
            
            const badge = document.querySelector('.notification-badge');
            if (badge && data.count > 0) {
                badge.textContent = data.count;
                badge.style.display = 'flex';
            }
        } catch (error) {
            console.error('Erro ao carregar contagem:', error);
        }
    }
    
    renderNotifications(notifications) {
        if (!notifications.length) {
            return `
                <div class="notification-empty">
                    <i class="fas fa-bell-slash"></i>
                    <p>Nenhuma notificação</p>
                </div>
            `;
        }
        
        return notifications.map(notif => `
            <div class="notification-item ${notif.read ? '' : 'unread'}">
                <div class="notification-icon ${notif.type}">
                    <i class="fas fa-${this.getNotificationIcon(notif.type)}"></i>
                </div>
                <div class="notification-content">
                    <p class="notification-text">${notif.message}</p>
                    <small class="notification-time">${this.formatTime(notif.created_at)}</small>
                </div>
            </div>
        `).join('');
    }
    
    getNotificationIcon(type) {
        const icons = {
            'info': 'info-circle',
            'warning': 'exclamation-triangle',
            'success': 'check-circle',
            'error': 'times-circle',
            'order': 'shopping-cart',
            'project': 'cube',
            'client': 'user'
        };
        return icons[type] || 'bell';
    }
    
    // Busca global (MANTIDO)
    initSearch() {
        const searchInput = document.querySelector('.global-search');
        if (!searchInput) return;
        
        // Busca em tempo real
        searchInput.addEventListener('input', this.debounce(async (e) => {
            const query = e.target.value.trim();
            if (query.length > 2) {
                await this.performSearch(query);
            }
        }, 300));
        
        // Atalho Ctrl+K
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }
    
    async performSearch(query) {
        try {
            const response = await fetch(`/api/admin/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();
            
            // Mostrar resultados em dropdown
            this.showSearchResults(results);
        } catch (error) {
            console.error('Erro na busca:', error);
        }
    }
    
    showSearchResults(results) {
        // Implementar dropdown de resultados
        console.log('Resultados:', results);
    }
    
    // Atalhos de teclado (MANTIDO)
    initKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Shift+P - Novo projeto
            if (e.ctrlKey && e.shiftKey && e.key === 'P') {
                e.preventDefault();
                window.location.href = '/admin/projetos/novo';
            }
            
            // Ctrl+Shift+O - Pedidos
            if (e.ctrlKey && e.shiftKey && e.key === 'O') {
                e.preventDefault();
                window.location.href = '/admin/pedidos';
            }
            
            // Esc - Fechar modais/sidebar
            if (e.key === 'Escape') {
                document.querySelector('.admin-sidebar').classList.remove('active');
                document.querySelector('.sidebar-overlay').classList.remove('active');
            }
        });
    }
    
    // Logout com confirmação (MANTIDO)
    initLogout() {
        const logoutBtn = document.querySelector('.logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (confirm('Tem certeza que deseja sair?')) {
                    window.location.href = logoutBtn.getAttribute('href');
                }
            });
        }
    }
    
    // Utilitários (MANTIDOS)
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Agora';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} min atrás`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h atrás`;
        return date.toLocaleDateString('pt-BR');
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Mostrar mensagens (MANTIDO)
    showMessage(message, type = 'info', duration = 5000) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `admin-message admin-message-${type}`;
        messageDiv.innerHTML = `
            <div class="message-content">
                <i class="fas fa-${this.getMessageIcon(type)}"></i>
                <span>${message}</span>
            </div>
            <button class="message-close">&times;</button>
        `;
        
        document.body.appendChild(messageDiv);
        
        // Animar entrada
        setTimeout(() => {
            messageDiv.classList.add('show');
        }, 10);
        
        // Fechar ao clicar
        messageDiv.querySelector('.message-close').addEventListener('click', () => {
            messageDiv.classList.remove('show');
            setTimeout(() => messageDiv.remove(), 300);
        });
        
        // Auto-remover
        if (duration > 0) {
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.classList.remove('show');
                    setTimeout(() => messageDiv.remove(), 300);
                }
            }, duration);
        }
        
        return messageDiv;
    }
    
    getMessageIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'times-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    // Loading state (MANTIDO)
    showLoading(element) {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'admin-loading';
        loadingDiv.innerHTML = `
            <div class="loading-spinner"></div>
            <span>Carregando...</span>
        `;
        
        if (element) {
            element.style.position = 'relative';
            element.appendChild(loadingDiv);
        } else {
            document.body.appendChild(loadingDiv);
        }
        
        return loadingDiv;
    }
    
    hideLoading(loadingDiv) {
        if (loadingDiv && loadingDiv.parentNode) {
            loadingDiv.classList.add('hide');
            setTimeout(() => loadingDiv.remove(), 300);
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.adminCommon = new AdminCommon();
});

// Exportar funções úteis
window.showAdminMessage = (message, type, duration) => {
    return adminCommon.showMessage(message, type, duration);
};

window.showAdminLoading = (element) => {
    return adminCommon.showLoading(element);
};

window.hideAdminLoading = (loadingDiv) => {
    adminCommon.hideLoading(loadingDiv);
};