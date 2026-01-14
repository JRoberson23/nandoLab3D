// static/js/admin/configuracoes.js - VERSÃO COMPLETA
document.addEventListener('DOMContentLoaded', function() {
    console.log('Página de configurações carregada');
    
    // Carregar configurações ao abrir a página
    carregarConfiguracoes();
    
    // Botão salvar tudo
    document.getElementById('btnSalvarTudo')?.addEventListener('click', salvarTudo);
    
    // Botões de backup (APENAS SE EXISTIREM!)
    document.getElementById('btnExportProjetos')?.addEventListener('click', () => exportarBackup('projetos'));
    document.getElementById('btnExportClientes')?.addEventListener('click', () => exportarBackup('clientes'));
    document.getElementById('btnExportTudo')?.addEventListener('click', () => exportarBackup('tudo'));
    document.getElementById('btnAgendarBackup')?.addEventListener('click', agendarBackup);
    
    // Botão testar email
    document.getElementById('btnTestarEmail')?.addEventListener('click', testarEmail);
    
    // Contadores de caracteres para SEO
    const seoTitle = document.getElementById('seoTitle');
    const seoDesc = document.getElementById('seoDescription');
    
    if (seoTitle) {
        seoTitle.addEventListener('input', function() {
            atualizarContador(this, 60, 'titleCounter');
        });
        atualizarContador(seoTitle, 60, 'titleCounter');
    }
    
    if (seoDesc) {
        seoDesc.addEventListener('input', function() {
            atualizarContador(this, 160, 'descCounter');
        });
        atualizarContador(seoDesc, 160, 'descCounter');
    }
});

async function carregarConfiguracoes() {
    try {
        const response = await fetch('/admin/configuracoes/dados');
        const data = await response.json();
        
        if (data.success) {
            preencherFormularios(data.configuracoes);
        } else {
            mostrarErro('Erro ao carregar configurações');
        }
    } catch (error) {
        console.error('Erro:', error);
        mostrarErro('Não foi possível carregar as configurações');
    }
}

function preencherFormularios(config) {
    // Geral
    setValue('siteNome', config.geral?.site_nome);
    setValue('siteSlogan', config.geral?.site_slogan);
    setValue('siteDescricao', config.geral?.site_descricao);
    setValue('siteTimezone', config.geral?.timezone);
    setValue('siteIdioma', config.geral?.idioma);
    setCheckbox('manutencao', config.geral?.manutencao);
    
    // Site
    setValue('siteLogo', config.site?.logo);
    setValue('siteFavicon', config.site?.favicon);
    setValue('siteCorPrimaria', config.site?.cor_primaria);
    setValue('siteCorSecundaria', config.site?.cor_secundaria);
    setValue('siteKeywords', config.site?.keywords);
    
    // SEO (NOVOS CAMPOS - IMPORTANTE!)
    setValue('seoTitle', config.seo?.title);
    setValue('seoDescription', config.seo?.description);
    setValue('seoKeywords', config.seo?.keywords);
    setValue('seoGoogleAnalytics', config.seo?.google_analytics);
    setValue('seoOgImage', config.seo?.og_image);
    
    // Social (NOVOS CAMPOS)
    setValue('socialInstagram', config.social?.instagram);
    setValue('socialInstagramUrl', config.social?.instagram_url);
    setValue('socialFacebook', config.social?.facebook);
    setValue('socialWhatsapp', config.social?.whatsapp);
    setValue('socialWhatsappLink', config.social?.whatsapp_link);
    setValue('socialShowFeed', config.social?.show_feed);
    setValue('socialEmbedCode', config.social?.embed_code);
}

async function salvarTudo() {
    const btn = document.getElementById('btnSalvarTudo');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Salvando...';
    btn.disabled = true;
    
    try {
        // Coletar dados de cada aba
        const configuracoes = {
            geral: coletarDadosGeral(),
            site: coletarDadosSite(),
            seo: coletarDadosSeo(),
            social: coletarDadosSocial()
        };
        
        // Salvar cada tipo separadamente
        for (const [tipo, dados] of Object.entries(configuracoes)) {
            const formData = new FormData();
            formData.append('tipo', tipo);
            formData.append('dados', JSON.stringify(dados));
            
            const response = await fetch('/admin/configuracoes/salvar', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            if (!result.success) {
                throw new Error(`Erro ao salvar ${tipo}: ${result.error}`);
            }
        }
        
        mostrarSucesso('Todas as configurações foram salvas com sucesso!');
        
    } catch (error) {
        console.error('Erro ao salvar:', error);
        mostrarErro('Erro ao salvar configurações: ' + error.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function coletarDadosGeral() {
    return {
        site_nome: getValue('siteNome'),
        site_slogan: getValue('siteSlogan'),
        site_descricao: getValue('siteDescricao'),
        timezone: getValue('siteTimezone'),
        idioma: getValue('siteIdioma'),
        manutencao: getCheckbox('manutencao')
    };
}

function coletarDadosSite() {
    return {
        logo: getValue('siteLogo'),
        favicon: getValue('siteFavicon'),
        cor_primaria: getValue('siteCorPrimaria'),
        cor_secundaria: getValue('siteCorSecundaria'),
        keywords: getValue('siteKeywords')
    };
}

function coletarDadosSeo() {
    return {
        title: getValue('seoTitle'),
        description: getValue('seoDescription'),
        keywords: getValue('seoKeywords'),
        google_analytics: getValue('seoGoogleAnalytics'),
        og_image: getValue('seoOgImage')
    };
}

function coletarDadosSocial() {
    return {
        instagram: getValue('socialInstagram'),
        instagram_url: getValue('socialInstagramUrl'),
        facebook: getValue('socialFacebook'),
        whatsapp: getValue('socialWhatsapp'),
        whatsapp_link: getValue('socialWhatsappLink'),
        show_feed: getValue('socialShowFeed'),
        embed_code: getValue('socialEmbedCode')
    };
}

async function exportarBackup(tipo) {
    try {
        const btnId = `btnExport${tipo.charAt(0).toUpperCase() + tipo.slice(1)}`;
        const btn = document.getElementById(btnId);
        
        if (btn) {
            btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Preparando...';
            btn.disabled = true;
        }
        
        // Abrir em nova aba para download
        window.open(`/admin/backup/exportar/${tipo}`, '_blank');
        
        mostrarSucesso(`Backup ${tipo} iniciado. O download começará em breve.`);
        
        // Restaurar botão após 2 segundos
        setTimeout(() => {
            if (btn) {
                btn.innerHTML = tipo === 'projetos' ? 
                    '<i class="fas fa-cube me-2"></i> Exportar Projetos (JSON)' :
                    tipo === 'clientes' ? 
                    '<i class="fas fa-users me-2"></i> Exportar Clientes (CSV)' :
                    '<i class="fas fa-file-archive me-2"></i> Backup Completo (ZIP)';
                btn.disabled = false;
            }
        }, 2000);
        
    } catch (error) {
        mostrarErro('Erro ao exportar backup: ' + error.message);
    }
}

async function agendarBackup() {
    const frequencia = getValue('backupFrequencia');
    const manterDias = parseInt(getValue('backupManter'));
    
    try {
        const formData = new FormData();
        formData.append('frequencia', frequencia);
        formData.append('manter_dias', manterDias);
        
        const response = await fetch('/admin/backup/agendar', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (result.success) {
            mostrarSucesso(result.message);
        } else {
            mostrarErro(result.error);
        }
    } catch (error) {
        mostrarErro('Erro ao agendar backup: ' + error.message);
    }
}

// Funções auxiliares
function getValue(id) {
    const element = document.getElementById(id);
    return element ? element.value : '';
}

function setValue(id, value) {
    const element = document.getElementById(id);
    if (element && value !== undefined) {
        element.value = value;
    }
}

function getCheckbox(id) {
    const element = document.getElementById(id);
    return element ? element.checked : false;
}

function setCheckbox(id, checked) {
    const element = document.getElementById(id);
    if (element) {
        element.checked = !!checked;
    }
}

function atualizarContador(element, max, counterId) {
    const length = element.value.length;
    let counter = document.getElementById(counterId);
    
    if (!counter) {
        counter = document.createElement('small');
        counter.id = counterId;
        counter.className = 'form-text';
        element.parentNode.appendChild(counter);
    }
    
    counter.textContent = `${length}/${max} caracteres`;
    counter.className = `form-text ${length > max ? 'text-danger' : length > max * 0.9 ? 'text-warning' : 'text-success'}`;
}

function mostrarSucesso(mensagem) {
    alerta('success', mensagem);
}

function mostrarErro(mensagem) {
    alerta('danger', mensagem);
}

function alerta(tipo, mensagem) {
    const container = document.getElementById('admin-alert-container');
    const alert = document.getElementById('admin-alert-message');
    
    if (container && alert) {
        alert.className = `alert alert-${tipo} alert-dismissible fade show`;
        alert.innerHTML = `
            <i class="fas fa-${tipo === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        container.style.display = 'block';
        
        setTimeout(() => {
            container.style.display = 'none';
        }, 5000);
    } else {
        // Fallback
        alert(mensagem);
    }
}

// Teste de email (simulado)
async function testarEmail() {
    const btn = document.getElementById('btnTestarEmail');
    if (!btn) return;
    
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Testando...';
    
    // Simulação - em produção, faria uma requisição real
    setTimeout(() => {
        btn.innerHTML = originalText;
        mostrarSucesso('Conexão de email testada com sucesso! (simulado)');
    }, 1500);
}