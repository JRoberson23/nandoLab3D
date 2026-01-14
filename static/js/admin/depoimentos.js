// static/js/admin/depoimentos.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('Depoimentos Admin carregado');
    
    // Inicializar componentes
    initDepoimentos();
    initEventListeners();
    loadDepoimentos();
});

function initDepoimentos() {
    // Sistema de estrelas para avaliação
    const stars = document.querySelectorAll('.star');
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const value = parseInt(this.getAttribute('data-value'));
            document.getElementById('avaliacaoInput').value = value;
            
            stars.forEach(s => {
                if (parseInt(s.getAttribute('data-value')) <= value) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
        });
    });
}

function initEventListeners() {
    // Botão novo depoimento
    document.getElementById('btnNovoDepoimento').addEventListener('click', function() {
        document.getElementById('modalTitle').textContent = 'Novo Depoimento';
        document.getElementById('formDepoimento').reset();
        document.getElementById('avaliacaoInput').value = '5';
        
        // Resetar estrelas
        document.querySelectorAll('.star').forEach((star, index) => {
            if (index < 5) star.classList.add('active');
        });
        
        const modal = new bootstrap.Modal(document.getElementById('depoimentoModal'));
        modal.show();
    });
    
    // Busca
    document.getElementById('buscaDepoimento').addEventListener('input', function(e) {
        filterDepoimentos();
    });
    
    // Filtros
    document.getElementById('filtroStatus').addEventListener('change', filterDepoimentos);
    document.getElementById('filtroAvaliacao').addEventListener('change', filterDepoimentos);
}

async function loadDepoimentos() {
    try {
        // Simular carregamento de API
        const depoimentos = [
            {
                id: 1,
                nome: "João Silva",
                cargo: "Arquiteto",
                empresa: "Studio Arquitetura",
                texto: "Excelente qualidade nas maquetes 3D!",
                avaliacao: 5,
                aprovado: true,
                foto: null,
                created_at: "2024-01-10"
            }
        ];
        
        renderDepoimentos(depoimentos);
        updateStats(depoimentos);
        
    } catch (error) {
        console.error('Erro ao carregar depoimentos:', error);
        document.getElementById('containerDepoimentos').innerHTML = `
            <div class="alert alert-danger">
                Erro ao carregar depoimentos. Tente novamente.
            </div>
        `;
    }
}

function renderDepoimentos(depoimentos) {
    const container = document.getElementById('containerDepoimentos');
    
    if (!depoimentos || depoimentos.length === 0) {
        container.innerHTML = `
            <div class="empty-depoimentos">
                <i class="fas fa-comment-slash"></i>
                <h4>Nenhum depoimento encontrado</h4>
                <p class="mb-4">Comece adicionando seu primeiro depoimento</p>
                <button class="btn btn-primary" id="btnNovoDepoimento">
                    <i class="fas fa-plus me-2"></i> Adicionar Depoimento
                </button>
            </div>
        `;
        return;
    }
    
    let html = '<div class="row">';
    
    depoimentos.forEach(dep => {
        const stars = '★'.repeat(dep.avaliacao) + '☆'.repeat(5 - dep.avaliacao);
        
        html += `
        <div class="col-md-6 mb-3 depoimento-item" 
             data-status="${dep.aprovado ? 'aprovado' : 'pendente'}" 
             data-avaliacao="${dep.avaliacao}">
            <div class="card depoimento-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div class="d-flex align-items-center">
                            ${dep.foto ? 
                                `<img src="${dep.foto}" alt="${dep.nome}" class="depoimento-avatar me-3">` : 
                                `<div class="depoimento-avatar bg-primary text-white d-flex align-items-center justify-content-center me-3">
                                    <i class="fas fa-user fa-lg"></i>
                                </div>`
                            }
                            <div>
                                <h5 class="mb-1">${dep.nome}</h5>
                                <p class="text-muted mb-0 small">
                                    ${dep.cargo}${dep.empresa ? ' na ' + dep.empresa : ''}
                                </p>
                            </div>
                        </div>
                        <div class="text-end">
                            <span class="status-badge ${dep.aprovado ? 'status-aprovado' : 'status-pendente'}">
                                ${dep.aprovado ? 'Aprovado' : 'Pendente'}
                            </span>
                            <div class="avaliacao-stars mt-2">
                                ${stars}
                            </div>
                        </div>
                    </div>
                    <p class="depoimento-texto">"${dep.texto}"</p>
                    <div class="d-flex justify-content-between align-items-center mt-3">
                        <small class="text-muted">${new Date(dep.created_at).toLocaleDateString('pt-BR')}</small>
                        <div>
                            <button class="btn btn-sm btn-outline-primary me-1" onclick="editarDepoimento(${dep.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" onclick="excluirDepoimento(${dep.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

function updateStats(depoimentos) {
    const total = depoimentos.length;
    const aprovados = depoimentos.filter(d => d.aprovado).length;
    const pendentes = total - aprovados;
    const media = depoimentos.reduce((sum, d) => sum + d.avaliacao, 0) / total || 0;
    
    document.getElementById('totalDepoimentos').textContent = total;
    document.getElementById('aprovadosCount').textContent = aprovados;
    document.getElementById('pendentesCount').textContent = pendentes;
    document.getElementById('mediaAvaliacao').textContent = media.toFixed(1);
    document.getElementById('contadorDepoimentos').textContent = total;
}

function filterDepoimentos() {
    const search = document.getElementById('buscaDepoimento').value.toLowerCase();
    const status = document.getElementById('filtroStatus').value;
    const avaliacao = document.getElementById('filtroAvaliacao').value;
    
    const items = document.querySelectorAll('.depoimento-item');
    let visibleCount = 0;
    
    items.forEach(item => {
        const itemStatus = item.getAttribute('data-status');
        const itemAvaliacao = item.getAttribute('data-avaliacao');
        const text = item.textContent.toLowerCase();
        
        const matchSearch = !search || text.includes(search);
        const matchStatus = !status || itemStatus === status;
        const matchAvaliacao = !avaliacao || itemAvaliacao === avaliacao;
        
        if (matchSearch && matchStatus && matchAvaliacao) {
            item.style.display = 'block';
            visibleCount++;
        } else {
            item.style.display = 'none';
        }
    });
    
    document.getElementById('contadorDepoimentos').textContent = visibleCount;
}

// Funções globais
window.editarDepoimento = function(id) {
    console.log('Editar depoimento:', id);
    // Implementar edição
};

window.excluirDepoimento = function(id) {
    if (confirm('Tem certeza que deseja excluir este depoimento?')) {
        console.log('Excluir depoimento:', id);
        // Implementar exclusão
    }
};