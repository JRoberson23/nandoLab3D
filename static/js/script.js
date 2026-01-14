// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 NandoLab 3D - Site carregado');
    
    // 1. Efeito na navbar ao rolar
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // 2. Validação de formulários
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Criar mensagem de erro se não existir
                    if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'invalid-feedback';
                        errorDiv.textContent = 'Este campo é obrigatório';
                        field.parentNode.appendChild(errorDiv);
                    }
                } else {
                    field.classList.remove('is-invalid');
                    
                    // Remover mensagem de erro se existir
                    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
                    if (errorDiv) {
                        errorDiv.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                
                // Scroll para o primeiro erro
                const firstError = form.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                    firstError.focus();
                }
            }
        });
    });
    
    // 3. Máscara para telefone
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 11) {
                value = value.substring(0, 11);
            }
            
            if (value.length > 10) {
                // Formato: (11) 99999-9999
                value = value.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
            } else if (value.length > 6) {
                // Formato: (11) 9999-9999
                value = value.replace(/^(\d{2})(\d{4})(\d{0,4})$/, '($1) $2-$3');
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{0,5})$/, '($1) $2');
            } else if (value.length > 0) {
                value = value.replace(/^(\d{0,2})$/, '($1');
            }
            
            e.target.value = value;
        });
    });
    
    // 4. Máscara para dinheiro (R$)
    const moneyInputs = document.querySelectorAll('input[data-money]');
    moneyInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = (value / 100).toFixed(2);
            value = value.replace('.', ',');
            value = value.replace(/(\d)(\d{3})(\d{3}),/g, "$1.$2.$3,");
            value = value.replace(/(\d)(\d{3}),/g, "$1.$2,");
            e.target.value = 'R$ ' + value;
        });
    });
    
    // 5. Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    window.scrollTo({
                        top: target.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // 6. Carregar dinamicamente o portfólio (exemplo)
    async function carregarPortfolio() {
        try {
            const response = await fetch('/api/portfolio');
            const projetos = await response.json();
            
            const container = document.getElementById('portfolio-container');
            if (container && projetos.length > 0) {
                let html = '';
                
                projetos.forEach(projeto => {
                    html += `
                    <div class="col-md-4 mb-4">
                        <div class="card portfolio-card">
                            <img src="${projeto.imagem || '/static/images/default-project.jpg'}" 
                                 class="card-img-top" 
                                 alt="${projeto.titulo}">
                            <div class="card-body">
                                <h5 class="card-title">${projeto.titulo}</h5>
                                <p class="card-text">${projeto.descricao.substring(0, 100)}...</p>
                                <span class="badge bg-primary">${projeto.categoria}</span>
                            </div>
                        </div>
                    </div>
                    `;
                });
                
                container.innerHTML = html;
            }
        } catch (error) {
            console.error('Erro ao carregar portfólio:', error);
        }
    }
    
    // 7. Newsletter signup
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (!email) {
                alert('Por favor, digite seu e-mail');
                return;
            }
            
            try {
                const response = await fetch('/api/newsletter', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email: email })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('Obrigado por se inscrever!');
                    emailInput.value = '';
                } else {
                    alert('Erro ao se inscrever. Tente novamente.');
                }
            } catch (error) {
                console.error('Erro:', error);
                alert('Erro de conexão. Tente novamente.');
            }
        });
    }
    
    // 8. Contador de visitas (simples)
    function atualizarContadorVisitas() {
        let visitas = localStorage.getItem('nandolab_visitas');
        
        if (!visitas) {
            visitas = 1;
        } else {
            visitas = parseInt(visitas) + 1;
        }
        
        localStorage.setItem('nandolab_visitas', visitas);
        
        const contadorElement = document.getElementById('contador-visitas');
        if (contadorElement) {
            contadorElement.textContent = visitas;
        }
    }
    
    atualizarContadorVisitas();
    
    // 9. Modal para imagens do portfólio
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('portfolio-img')) {
            const modalHTML = `
            <div class="modal fade" id="portfolioModal" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${e.target.alt}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body text-center">
                            <img src="${e.target.src}" class="img-fluid" alt="${e.target.alt}">
                        </div>
                    </div>
                </div>
            </div>
            `;
            
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            
            const modal = new bootstrap.Modal(document.getElementById('portfolioModal'));
            modal.show();
            
            // Remover modal após fechar
            document.getElementById('portfolioModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
        }
    });
    
    // 10. Efeito de digitação (para slogans)
    function typeWriter(element, text, speed = 50) {
        let i = 0;
        element.textContent = '';
        
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }
    
    const typingElement = document.getElementById('typing-effect');
    if (typingElement) {
        const text = typingElement.getAttribute('data-text') || 'Transformando ideias em arte 3D';
        typeWriter(typingElement, text);
    }
});

// Funções utilitárias globais
function formatarData(data) {
    return new Date(data).toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

// Exportar funções para uso em outros arquivos
// export { formatarData, formatarMoeda };