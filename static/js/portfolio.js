// static/js/portfolio.js - VERSÃO CORRIGIDA

// Configurações
let currentCategory = 'all';

// Inicializar quando o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    console.log('Portfólio.js carregado - Versão com renderização no template');
    
    // Configurar filtros de categoria
    setupCategoryFilters();
    
    // Configurar modal de detalhes
    setupProjectModals();
    
    // Adicionar funcionalidade de busca
    setupSearch();
});

// Configurar filtros de categoria
function setupCategoryFilters() {
    const filterButtons = document.querySelectorAll('.btn-filter');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remover classe active de todos
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Adicionar ao botão clicado
            this.classList.add('active');
            
            // Atualizar categoria
            currentCategory = this.getAttribute('data-category');
            
            // Filtrar projetos
            filterProjects();
        });
    });
}

// Filtrar projetos por categoria
function filterProjects() {
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    const emptyState = document.getElementById('empty-state');
    
    let visibleItems = 0;
    
    portfolioItems.forEach(item => {
        const itemCategory = item.getAttribute('data-category') || '';
        
        if (currentCategory === 'all' || 
            itemCategory === currentCategory || 
            itemCategory.includes(currentCategory)) {
            item.style.display = 'block';
            visibleItems++;
            
            // Adicionar animação
            item.classList.add('fade-in');
        } else {
            item.style.display = 'none';
        }
    });
    
    // Mostrar mensagem se não houver itens
    showEmptyState(visibleItems === 0);
}

// Mostrar/ocultar mensagem de vazio
function showEmptyState(show) {
    let emptyState = document.getElementById('empty-state');
    
    if (show && !emptyState) {
        emptyState = document.createElement('div');
        emptyState.id = 'empty-state';
        emptyState.className = 'col-12 text-center py-5';
        emptyState.innerHTML = `
            <i class="fas fa-search fa-4x text-muted mb-3"></i>
            <h4 class="text-muted">Nenhum projeto encontrado</h4>
            <p class="text-muted">Tente selecionar outra categoria</p>
            <button class="btn btn-primary mt-3" onclick="resetFilters()">
                <i class="fas fa-redo me-2"></i>Mostrar Todos
            </button>
        `;
        
        const gallery = document.getElementById('portfolio-gallery');
        if (gallery) {
            gallery.appendChild(emptyState);
        }
    } else if (!show && emptyState) {
        emptyState.remove();
    }
}

// Resetar filtros
function resetFilters() {
    currentCategory = 'all';
    
    // Resetar botões
    const filterButtons = document.querySelectorAll('.btn-filter');
    filterButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-category') === 'all') {
            btn.classList.add('active');
        }
    });
    
    // Mostrar todos os itens
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    portfolioItems.forEach(item => {
        item.style.display = 'block';
    });
    
    // Remover mensagem de vazio
    showEmptyState(false);
}

// Configurar modal de detalhes dos projetos
function setupProjectModals() {
    // Usar event delegation para links do modal
    document.addEventListener('click', function(e) {
        if (e.target.closest('.btn-view-project')) {
            e.preventDefault();
            const link = e.target.closest('.btn-view-project');
            openProjectModal(link);
        }
    });
}

// Abrir modal com detalhes do projeto
function openProjectModal(linkElement) {
    // Coletar dados do data-attributes
    const projectId = linkElement.getAttribute('data-project-id');
    const projectTitle = linkElement.getAttribute('data-project-title');
    const projectCategory = linkElement.getAttribute('data-project-category');
    const projectDescription = linkElement.getAttribute('data-project-description');
    const projectDate = linkElement.getAttribute('data-project-date');
    const projectMaterial = linkElement.getAttribute('data-project-material');
    const projectImages = JSON.parse(linkElement.getAttribute('data-project-images') || '[]');
    
    // Atualizar título
    document.getElementById('modalProjectTitle').textContent = projectTitle;
    document.getElementById('modalProjectTitle2').textContent = projectTitle;
    
    // Atualizar categoria
    document.getElementById('modalProjectCategory').textContent = 
        projectCategory || 'Sem categoria';
    
    // Atualizar descrição
    document.getElementById('modalProjectDescription').textContent = 
        projectDescription || 'Descrição não disponível.';
    
    // Atualizar data
    document.getElementById('modalProjectDate').textContent = projectDate || 'Não informada';
    
    // Atualizar carrossel de imagens
    updateCarousel(projectImages, projectTitle);
    
    // Atualizar especificações
    updateSpecifications(projectMaterial, projectCategory, projectDate);
    
    // Atualizar link do botão "Solicitar Similar"
    const requestBtn = document.querySelector('#projectModal .btn-primary');
    if (requestBtn) {
        requestBtn.href = `/orcamento?ref=${projectId}&tipo=${encodeURIComponent(projectCategory)}`;
    }
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('projectModal'));
    modal.show();
}

// Atualizar carrossel de imagens
function updateCarousel(images, projectTitle) {
    const carouselInner = document.getElementById('modalCarouselInner');
    if (!carouselInner) return;
    
    let carouselHTML = '';
    
    if (images && images.length > 0) {
        images.forEach((img, index) => {
            carouselHTML += `
            <div class="carousel-item ${index === 0 ? 'active' : ''}">
                <img src="${img}" 
                     class="d-block w-100" 
                     alt="${projectTitle} - Imagem ${index + 1}"
                     onerror="this.src='/static/imagens/projeto-default.jpg'">
            </div>
            `;
        });
    } else {
        // Imagem padrão se não houver imagens
        carouselHTML = `
        <div class="carousel-item active">
            <div class="d-flex justify-content-center align-items-center bg-light" style="height: 300px;">
                <i class="fas fa-cube fa-4x text-muted"></i>
            </div>
        </div>
        `;
    }
    
    carouselInner.innerHTML = carouselHTML;
}

// Atualizar especificações no modal
function updateSpecifications(material, category, date) {
    const specsList = document.getElementById('modalProjectSpecs');
    if (!specsList) return;
    
    let specsHTML = '';
    
    if (material) {
        specsHTML += `<li><i class="fas fa-cube me-2 text-primary"></i><strong>Material:</strong> ${material}</li>`;
    }
    
    if (category) {
        specsHTML += `<li><i class="fas fa-tag me-2 text-primary"></i><strong>Categoria:</strong> ${category}</li>`;
    }
    
    if (date && date !== '--/--/----') {
        specsHTML += `<li><i class="far fa-calendar-check me-2 text-primary"></i><strong>Concluído:</strong> ${date}</li>`;
    }
    
    specsList.innerHTML = specsHTML || '<li class="text-muted">Especificações não disponíveis</li>';
}

// Configurar funcionalidade de busca
function setupSearch() {
    // Criar campo de busca se não existir
    const filterSection = document.querySelector('.py-4.bg-light .container .row');
    if (!filterSection) return;
    
    let searchContainer = document.getElementById('portfolio-search');
    
    if (!searchContainer) {
        searchContainer = document.createElement('div');
        searchContainer.id = 'portfolio-search';
        searchContainer.className = 'col-12 mb-4';
        searchContainer.innerHTML = `
            <div class="input-group input-group-lg" style="max-width: 500px; margin: 0 auto;">
                <span class="input-group-text">
                    <i class="fas fa-search"></i>
                </span>
                <input type="text" 
                       class="form-control" 
                       id="search-input"
                       placeholder="Buscar projetos por título, descrição ou material...">
                <button class="btn btn-outline-secondary" type="button" id="clear-search">
                    Limpar
                </button>
            </div>
        `;
        
        filterSection.prepend(searchContainer);
        
        // Adicionar eventos
        const searchInput = document.getElementById('search-input');
        const clearButton = document.getElementById('clear-search');
        
        if (searchInput) {
            searchInput.addEventListener('input', performSearch);
        }
        
        if (clearButton) {
            clearButton.addEventListener('click', clearSearch);
        }
    }
}

// Realizar busca
function performSearch(e) {
    const searchTerm = e.target.value.toLowerCase().trim();
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    if (!searchTerm) {
        // Se busca vazia, aplicar filtro de categoria atual
        filterProjects();
        return;
    }
    
    let visibleItems = 0;
    
    portfolioItems.forEach(item => {
        const card = item.querySelector('.project-card');
        if (!card) return;
        
        const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
        const description = card.querySelector('.card-text')?.textContent.toLowerCase() || '';
        const category = card.querySelector('.badge.bg-light')?.textContent.toLowerCase() || '';
        const material = card.querySelectorAll('.badge.bg-light')[1]?.textContent.toLowerCase() || '';
        
        const matches = title.includes(searchTerm) || 
                       description.includes(searchTerm) || 
                       category.includes(searchTerm) || 
                       material.includes(searchTerm);
        
        if (matches) {
            item.style.display = 'block';
            visibleItems++;
        } else {
            item.style.display = 'none';
        }
    });
    
    showEmptyState(visibleItems === 0);
}

// Limpar busca
function clearSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.value = '';
        filterProjects();
    }
}

// Adicionar animação aos cards
function animateCards() {
    const cards = document.querySelectorAll('.project-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-card');
    });
}

// Inicializar animações
setTimeout(animateCards, 100);