// Contador animado para estatísticas
function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-count'));
    console.log(`Animado contador: elemento=${element},target=${target}`);

    if (isNaN(target) || target === 0) {
        console.error('Target inválido para contador:', element);
        return;
    }

    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            element.textContent = target + '+';
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Observador para ativar contadores quando visíveis
function setupStatsCounter() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counters = entry.target.querySelectorAll('.stat-number');
                counters.forEach(counter => {
                    // VALORES DE TESTE - substitua pelos valores reais que quiser
                    const testValues = [500, 150, 5, 12]; // Projetos, Destaques, Anos, Materiais
                    const index = Array.from(counters).indexOf(counter);
                    
                    // Se o data-count for 0, usa valor de teste
                    if (counter.getAttribute('data-count') === '0' && testValues[index]) {
                        counter.setAttribute('data-count', testValues[index]);
                    }
                    
                    animateCounter(counter);
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    const statsSection = document.querySelector('section.py-5');
    if (statsSection) {
        observer.observe(statsSection);
    } else {
        console.error('Seção de estatísticas NÃO encontrada!');
    }
}

// Carregar projetos em destaque da API
async function loadFeaturedProjects() {
    try {
        const response = await fetch('/api/portfolio?limit=3');
        const data = await response.json();
        
        const container = document.getElementById('featured-projects');
        if (container && data.projetos && data.projetos.length > 0) {
            container.innerHTML = '';
            
            data.projetos.forEach(projeto => {
                const projectHTML = `
                <div class="col-md-4">
                    <div class="project-card">
                        <img src="${projeto.imagens && projeto.imagens.length > 0 ? projeto.imagens[0] : 'https://images.unsplash.com/photo-1581094794329-c8112a89af12?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'}" 
                             class="project-img" 
                             alt="${projeto.titulo}">
                        <div class="project-overlay">
                            <div>
                                <h5 class="text-white mb-2">${projeto.categoria || 'Projeto 3D'}</h5>
                                <p class="text-light small mb-0">${projeto.material || 'Material variado'}</p>
                            </div>
                        </div>
                        <div class="p-3">
                            <h5>${projeto.titulo}</h5>
                            <p class="text-muted small">${projeto.material || ''} • ${projeto.data_conclusao ? new Date(projeto.data_conclusao).toLocaleDateString('pt-BR') : ''}</p>
                            <button class="btn btn-sm btn-outline-primary" onclick="viewProject(${projeto.id})">
                                Ver Detalhes
                            </button>
                        </div>
                    </div>
                </div>
                `;
                container.innerHTML += projectHTML;
            });
        }
    } catch (error) {
        console.error('Erro ao carregar projetos:', error);
        // Mantém os placeholders se a API falhar
    }
}

// Função para visualizar projeto
function viewProject(projectId) {
    window.location.href = `/portfolio#project-${projectId}`;
}

// Inicializar quando o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    console.log(`DOM carregado - inicializando home.js`);
    setupStatsCounter();

     // DEBUG: Verificar se os elementos existem
    const counters = document.querySelectorAll('.stat-number');
    console.log(`Total de elementos .stat-number: ${counters.length}`);
    counters.forEach((counter, i) => {
        const count = counter.getAttribute('data-count');
        console.log(`Contador ${i}: data-count="${count}"`);
    });
});