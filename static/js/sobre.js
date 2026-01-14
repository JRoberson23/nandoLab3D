// static/js/sobre.js
// JavaScript específico para a página Sobre

document.addEventListener('DOMContentLoaded', function() {
    console.log('Sobre.js carregado');
    
    // Animar elementos flutuantes
    initFloatingElements();
    
    // Animação para timeline quando visível
    initTimelineAnimation();
});

// Inicializar elementos flutuantes
function initFloatingElements() {
    const elements = document.querySelectorAll('.floating-cube, .floating-sphere, .floating-cylinder');
    
    // Adicionar delay aleatório para cada elemento
    elements.forEach((element, index) => {
        element.style.animationDelay = `${index * 0.5}s`;
    });
}

// Animar timeline quando visível
function initTimelineAnimation() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Delay escalonado para cada item
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateX(0)';
                }, index * 200);
                
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.3,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Configurar estado inicial
    timelineItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-20px)';
        item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(item);
    });
}

// Função para atualizar foto do fundador (quando tiver)
//function updateFounderPhoto(photoUrl) {
//    const founderImg = document.querySelector('.founder-image img');
//    if (founderImg && photoUrl) {
//        founderImg.src = photoUrl;
//        founderImg.alt = 'Fernando (Nando) - Fundador do NandoLab 3D';
//    }
//}