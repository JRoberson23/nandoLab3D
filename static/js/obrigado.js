// obrigado.js - Lógica da página de agradecimento

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Página de agradecimento carregada');
    
    // Personalizar mensagem com nome da URL
    const urlParams = new URLSearchParams(window.location.search);
    const nome = urlParams.get('nome');
    const pedidoId = urlParams.get('pedido_id');
    
    if (nome) {
        document.getElementById('personal-message').textContent = 
            `Obrigado, ${nome}, pelo seu interesse em nossos serviços!`;
    }
    
    // Mostrar número do pedido se disponível
    if (pedidoId) {
        document.getElementById('pedido-info').style.display = 'block';
        document.getElementById('pedido-numero').textContent = `#${pedidoId}`;
    }
    
    // Configurar WhatsApp com mensagem personalizada
    const whatsappBtn = document.querySelector('a[href*="whatsapp"]');
    if (whatsappBtn && pedidoId) {
        const currentText = whatsappBtn.getAttribute('href');
        const newText = `Olá! Gostaria de falar sobre meu orçamento #${pedidoId} enviado pelo site.`;
        whatsappBtn.setAttribute('href', currentText.replace('meu orçamento enviado', newText));
    }
    
    // Contador para redirecionamento automático
    let countdown = 10;
    let redirectTimer;
    let redirectEnabled = true;
    
    function startCountdown() {
        const countdownElement = document.getElementById('countdown');
        
        redirectTimer = setInterval(function() {
            if (!redirectEnabled) return;
            
            countdown--;
            countdownElement.textContent = countdown;
            
            if (countdown <= 0) {
                clearInterval(redirectTimer);
                window.location.href = '/';
            }
        }, 1000);
    }
    
    // Iniciar contador
    startCountdown();
    
    // Função para cancelar redirecionamento
    window.cancelRedirect = function() {
        redirectEnabled = false;
        clearInterval(redirectTimer);
        document.getElementById('redirect-counter').innerHTML = 
            '<i class="bi bi-check-circle text-success me-1"></i> Redirecionamento cancelado.';
    };
    
    // Animar elementos ao rolar
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observar elementos para animação
    document.querySelectorAll('.timeline-item, .tips-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
});