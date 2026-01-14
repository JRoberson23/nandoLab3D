// static/js/servicos.js

// Carregar serviços da API
async function loadServicos() {
    try {
        showLoading(true);
        
        const response = await fetch('/api/servicos');
        const data = await response.json();
        
        if (data.servicos && data.servicos.length > 0) {
            renderServicos(data.servicos);
        } else {
            renderDefaultServicos();
        }
    } catch (error) {
        console.error('Erro ao carregar serviços:', error);
        renderDefaultServicos();
    } finally {
        showLoading(false);
    }
}

// Mostrar/ocultar loading
function showLoading(show) {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.style.display = show ? 'block' : 'none';
    }
}

// Renderizar serviços da API
function renderServicos(servicos) {
    const container = document.getElementById('servicos-container');
    if (!container) return;
    
    let html = '';
    
    servicos.forEach(servico => {
        html += `
        <div class="col-lg-4 col-md-6">
            <div class="service-card">
                <div class="service-icon">
                    <i class="${getServiceIcon(servico.tipo)}"></i>
                </div>
                
                <h3 class="service-title">${servico.nome}</h3>
                <p class="service-description">${servico.descricao || 'Descrição do serviço'}</p>
                
                ${servico.preco_base ? `
                <div class="service-price">R$ ${servico.preco_base.toFixed(2)}</div>
                <div class="service-price-period">Preço base</div>
                ` : ''}
                
                <ul class="service-features">
                    <li><i class="fas fa-check"></i> Modelagem 3D profissional</li>
                    <li><i class="fas fa-check"></i> Revisões ilimitadas</li>
                    <li><i class="fas fa-check"></i> Suporte especializado</li>
                    <li><i class="fas fa-check"></i> Arquivos fonte incluídos</li>
                </ul>
                
                <a href="/orcamento?servico=${encodeURIComponent(servico.nome)}" 
                   class="btn btn-primary w-100">
                    <i class="fas fa-comments-dollar me-2"></i>Solicitar Orçamento
                </a>
            </div>
        </div>
        `;
    });
    
    container.innerHTML = html;
}

// Serviços padrão (se API não retornar)
function renderDefaultServicos() {
    const defaultServicos = [
        {
            nome: "Modelagem 3D Básica",
            descricao: "Criação de modelos 3D a partir de desenhos ou ideias.",
            tipo: "modelagem",
            preco_base: 150.00
        },
        {
            nome: "Impressão 3D Padrão",
            descricao: "Impressão de peças em PLA ou ABS com tamanho padrão.",
            tipo: "impressao",
            preco_base: 80.00
        },
        {
            nome: "Projeto Completo",
            descricao: "Modelagem + impressão + acabamento profissional.",
            tipo: "completo",
            preco_base: 300.00
        },
        {
            nome: "Escaneamento 3D",
            descricao: "Digitalização de objetos reais para modelo 3D.",
            tipo: "escaneamento",
            preco_base: 200.00
        },
        {
            nome: "Prototipagem Rápida",
            descricao: "Desenvolvimento rápido de protótipos funcionais.",
            tipo: "prototipagem",
            preco_base: 250.00
        },
        {
            nome: "Consultoria 3D",
            descricao: "Aconselhamento técnico para projetos em 3D.",
            tipo: "consultoria",
            preco_base: 100.00
        }
    ];
    
    renderServicos(defaultServicos);
}

// Obter ícone baseado no tipo de serviço
function getServiceIcon(tipo) {
    const icons = {
        'modelagem': 'fas fa-cube',
        'impressao': 'fas fa-print',
        'completo': 'fas fa-star',
        'escaneamento': 'fas fa-camera',
        'prototipagem': 'fas fa-cogs',
        'consultoria': 'fas fa-headset',
        'default': 'fas fa-cube'
    };
    
    return icons[tipo?.toLowerCase()] || icons.default;
}

// Formatar preço
function formatPrice(price) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(price);
}

// Inicializar quando o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    console.log('Serviços.js carregado');
    loadServicos();
});