// orcamento.js - Lógica específica da página de orçamento
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ orcamento.js carregado');
    
    const form = document.getElementById('orcamentoForm');
    const formStatus = document.getElementById('form-status');
    
    // DEBUG: Verifique se os elementos foram encontrados
    console.log('Form encontrado:', !!form);
    console.log('Form status encontrado:', !!formStatus);
    
    // Validação do formulário
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        console.log('📤 Enviando formulário...');
        
        // Validação básica
        const nome = document.getElementById('nome').value.trim();
        const email = document.getElementById('email').value.trim();
        const tipo = document.getElementById('tipo_projeto').value;
        const projeto = document.getElementById('projeto').value.trim();
        
        if (!nome || !email || !tipo || !projeto) {
            showAlert('Por favor, preencha todos os campos obrigatórios.', 'danger');
            return;
        }
        
        if (!validateEmail(email)) {
            showAlert('Por favor, insira um e-mail válido.', 'danger');
            return;
        }
        
        // Mostrar loading
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Enviando...';
        submitBtn.disabled = true;
        
        try {
            console.log('📦 Preparando envio com imagem...');
            
            // PRIMEIRO: Preparar FormData para enviar tudo (incluindo imagem)
            const formData = new FormData();
            formData.append('nome', nome);
            formData.append('email', email);
            formData.append('telefone', document.getElementById('telefone').value.trim());
            formData.append('tipo_projeto', tipo);
            formData.append('projeto', projeto);
            formData.append('prazo', document.getElementById('prazo').value);
            
            // Adicionar imagem se existir
            const imagemInput = document.getElementById('imagem');
            if (imagemInput.files[0]) {
                formData.append('imagem', imagemInput.files[0]);
                console.log('📷 Imagem anexada:', imagemInput.files[0].name);
            }
            
            // Enviar para nosso backend (agora com imagem)
            console.log('📦 Enviando para nosso backend...');
            const backendResponse = await fetch('/api/salvar-orcamento-com-imagem', {
                method: 'POST',
                body: formData  // Note: sem headers Content-Type, o browser define automaticamente
            });
            
            const backendData = await backendResponse.json();
            console.log('✅ Backend response:', backendData);
            
            if (!backendResponse.ok) {
                throw new Error('Erro no backend: ' + (backendData.detail || 'Unknown error'));
            }
            
            console.log('📧 Enviando para Formspree...');
            
            // DEPOIS: Enviar para Formspree usando o mesmo FormData
            const formspreeResponse = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            });
            
            const formspreeData = await formspreeResponse.json();
            console.log('✅ Formspree response:', formspreeData);
            
            if (formspreeResponse.ok) {
                // Mostrar modal de sucesso
                showSuccessModal(nome, backendData.pedido_id);
            } else {
                throw new Error('Erro ao enviar para Formspree: ' + formspreeData.error);
            }
            
        } catch (error) {
            console.error('❌ Erro no envio:', error);
            showAlert('❌ Ocorreu um erro: ' + error.message, 'danger');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    });
    
    // Funções auxiliares
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    function showAlert(message, type) {
        if (!formStatus) {
            console.error('❌ form-status não encontrado!');
            alert(message); // Fallback
            return;
        }
        
        formStatus.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Auto-remover alerta após 5 segundos
        setTimeout(() => {
            const alert = formStatus.querySelector('.alert');
            if (alert) {
                alert.remove();
            }
        }, 5000);
    }
    
    // Validação em tempo real do email
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            if (this.value && !validateEmail(this.value)) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    }
    
    // ========== NOVAS FUNÇÕES ADICIONADAS ==========
    
    // Função para mostrar modal de sucesso
    function showSuccessModal(nome, pedidoId) {
        // Criar modal dinamicamente
        const modalHtml = `
        <div class="modal fade" id="successModal" tabindex="-1" aria-labelledby="successModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title" id="successModalLabel">
                            <i class="fas fa-check-circle me-2"></i> Orçamento Enviado!
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <div class="mb-3">
                            <i class="fas fa-paper-plane fa-4x text-success"></i>
                        </div>
                        <h4 class="mb-3">Obrigado, ${nome}!</h4>
                        <p>Seu orçamento foi enviado com sucesso.</p>
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            <strong>Nº do Pedido:</strong> ${pedidoId}
                        </div>
                        <p class="text-muted">Você receberá uma confirmação por email em breve.</p>
                    </div>
                    <div class="modal-footer justify-content-center">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            <i class="fas fa-home me-2"></i> Ficar nesta página
                        </button>
                        <button type="button" class="btn btn-success" onclick="goToThankYouPage('${nome}', '${pedidoId}')">
                            <i class="fas fa-thumbs-up me-2"></i> Ir para página de confirmação
                        </button>
                    </div>
                </div>
            </div>
        </div>
        `;
        
        // Adicionar modal ao body
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Mostrar modal
        const successModal = new bootstrap.Modal(document.getElementById('successModal'));
        successModal.show();
        
        // Remover modal quando fechar
        document.getElementById('successModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }
    
    // Função para ir para página de obrigado
    window.goToThankYouPage = function(nome, pedidoId) {
        window.location.href = `/obrigado?nome=${encodeURIComponent(nome)}&pedido_id=${pedidoId}`;
    };
});