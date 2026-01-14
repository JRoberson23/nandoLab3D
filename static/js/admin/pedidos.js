// Funções para gerenciamento de pedidos

/**
 * Exibe detalhes de um pedido
 */
function verPedido(pedidoId) {
    // Carregar detalhes do pedido via AJAX
    fetch(`/admin/pedidos/${pedidoId}/detalhes`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar detalhes');
            }
            return response.text();
        })
        .then(html => {
            document.getElementById('pedidoDetalhes').innerHTML = html;
            const modal = new bootstrap.Modal(document.getElementById('pedidoModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao carregar detalhes do pedido');
        });
}

/**
 * Aprova um pedido
 */
function aprovarPedido(pedidoId) {
    if (confirm('Deseja aprovar este pedido?')) {
        fetch(`/admin/pedidos/${pedidoId}/aprovar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content || ''
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Pedido aprovado com sucesso!');
                location.reload();
            } else {
                alert('Erro: ' + (data.error || 'Erro desconhecido'));
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao aprovar pedido');
        });
    }
}

/**
 * Rejeita um pedido
 */
function rejeitarPedido(pedidoId) {
    const motivo = prompt('Digite o motivo da rejeição:');
    if (motivo) {
        fetch(`/admin/pedidos/${pedidoId}/rejeitar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content || ''
            },
            body: JSON.stringify({ motivo: motivo })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Pedido rejeitado!');
                location.reload();
            } else {
                alert('Erro: ' + (data.error || 'Erro desconhecido'));
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao rejeitar pedido');
        });
    }
}

/**
 * Marca um pedido como concluído
 */
function concluirPedido(pedidoId) {
    if (confirm('Marcar pedido como concluído?')) {
        fetch(`/admin/pedidos/${pedidoId}/concluir`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content || ''
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Pedido marcado como concluído!');
                location.reload();
            } else {
                alert('Erro: ' + (data.error || 'Erro desconhecido'));
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao concluir pedido');
        });
    }
}

/**
 * Redireciona para página de edição do pedido
 */
function editarPedido(pedidoId) {
    window.location.href = `/admin/pedidos/editar/${pedidoId}`;
}

// Event Listeners para os botões
document.addEventListener('DOMContentLoaded', function() {
    // Configurar botão de enviar orçamento
    const btnEnviarOrcamento = document.getElementById('btnEnviarOrcamento');
    if (btnEnviarOrcamento) {
        btnEnviarOrcamento.addEventListener('click', function() {
            alert('Funcionalidade de envio de orçamento em desenvolvimento!');
        });
    }
    
    // Ver detalhes do pedido
    document.querySelectorAll('.btn-ver-pedido').forEach(button => {
        button.addEventListener('click', function() {
            const pedidoId = this.getAttribute('data-pedido-id');
            verPedido(pedidoId);
        });
    });
    
    // Aprovar pedido
    document.querySelectorAll('.btn-aprovar-pedido').forEach(button => {
        button.addEventListener('click', function() {
            const pedidoId = this.getAttribute('data-pedido-id');
            aprovarPedido(pedidoId);
        });
    });
    
    // Rejeitar pedido
    document.querySelectorAll('.btn-rejeitar-pedido').forEach(button => {
        button.addEventListener('click', function() {
            const pedidoId = this.getAttribute('data-pedido-id');
            rejeitarPedido(pedidoId);
        });
    });
    
    // Concluir pedido
    document.querySelectorAll('.btn-concluir-pedido').forEach(button => {
        button.addEventListener('click', function() {
            const pedidoId = this.getAttribute('data-pedido-id');
            concluirPedido(pedidoId);
        });
    });
    
    // Editar pedido
    document.querySelectorAll('.btn-editar-pedido').forEach(button => {
        button.addEventListener('click', function() {
            const pedidoId = this.getAttribute('data-pedido-id');
            editarPedido(pedidoId);
        });
    });
});