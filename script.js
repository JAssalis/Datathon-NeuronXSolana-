let allPosts = [];

/**
 * Renderiza uma lista de posts no container principal.
 * @param {Array} postsToRender - O array de posts a ser exibido.
 */
function renderPosts(postsToRender) {
  const container = document.getElementById('posts-container');
  
  // Mensagem se o filtro não retornar nada
  if (postsToRender.length === 0) {
    container.innerHTML = '<p style="text-align: center; color: #A0B8D0;">Nenhum tweet encontrado para esta data.</p>';
    return;
  }

  container.innerHTML = ''; // Limpa o container
  
  postsToRender.forEach(post => {
    // Tenta extrair o username.
    const username = post.username || 'desconhecido';
    
    // Usa o account_type diretamente do JSON.
    const accountType = post.account_type || 'regular';

    const postEl = document.createElement('div');
    postEl.className = 'xis-post';
    postEl.dataset.postId = post.post_id; // Armazena o post_id no elemento

    // Formata a data para exibição (ex: 25/12/2023 14:30)
    const formattedDate = new Date(post.timestamp).toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });

    postEl.innerHTML = `
      <div class="post-header">
        <span class="username">@${username}</span>
        <span class="account-type">${accountType}</span>
      </div>
      <div class="text">${post.text}</div>
      <div class="post-meta">
        <span class="timestamp">${formattedDate}</span>
        <span class="likes">👍 ${post.likes}</span>
        <span class="reposts">🔁 ${post.reposts}</span>
      </div>
    `;

    container.appendChild(postEl);
  });
}

/**
 * Filtra os posts com base na data selecionada no calendário.
 */
function filterByDate() {
  const selectedDate = document.getElementById('date-filter').value;
  
  if (!selectedDate) {
    renderPosts(allPosts); // Se limpar a data, mostra tudo (ou poderia mostrar nada)
    return;
  }

  // Filtra os posts
  const filtered = allPosts.filter(post => {
    // Pega apenas a parte YYYY-MM-DD do timestamp
    const postDate = post.timestamp.split('T')[0];
    return postDate === selectedDate;
  });

  renderPosts(filtered);
}

// --- LÓGICA DE CARREGAMENTO INICIAL ---

window.addEventListener('DOMContentLoaded', async () => {
  const postsContainer = document.getElementById('posts-container');
  const dateFilter = document.getElementById('date-filter');

  try {
    // 1. Busca o "data.json" (que você renomeou)
    const response = await fetch('data.json'); 
    
    if (!response.ok) {
      throw new Error('Arquivo data.json não encontrado na pasta.');
    }
    
    allPosts = await response.json();

    if (allPosts.length === 0) {
      postsContainer.innerHTML = '<p style="text-align: center; color: #A0B8D0;">JSON carregado, mas está vazio.</p>';
      return;
    }

    // 2. CORREÇÃO DE LÓGICA: Configura o calendário
    // Pega todas as datas e ordena
    const dates = allPosts.map(p => p.timestamp.split('T')[0]);
    dates.sort(); 
    
    const minDate = dates[0]; // A primeira data (ex: 2022-10-01)
    const maxDate = dates[dates.length - 1]; // A última data (ex: 2024-12-25)

    // Define os atributos do calendário no HTML
    dateFilter.min = minDate;
    dateFilter.max = maxDate;
    dateFilter.value = minDate; // Define o valor padrão para o primeiro dia

    
    // 3. Renderiza APENAS os posts do primeiro dia (para não travar)
    filterByDate(); 
    
    // 4. Adiciona o 'listener' para monitorar mudanças futuras no filtro
    dateFilter.addEventListener('change', filterByDate);

  } catch (err) {
    console.error('Erro ao carregar data.json:', err);
    postsContainer.innerHTML = `
      <p style="color: #FF6B6B; text-align: center;">
        ❌ Falha ao carregar <code>data.json</code>.<br>
        Verifique se o arquivo está na mesma pasta e é um JSON válido.
      </p>
    `;
  }
});