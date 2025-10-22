let allPosts = [];

// Função para parsear CSV (lida com aspas e vírgulas no texto)
function parseCSV(csvText) {
  const lines = csvText.split('\n').filter(line => line.trim() !== '');
  
  // Primeira linha são os headers
  const headers = lines[0].split(',').map(h => h.trim());
  const posts = [];

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    const values = [];
    let current = '';
    let inQuotes = false;

    // Parser CSV que respeita aspas
    for (let j = 0; j < line.length; j++) {
      const char = line[j];
      const nextChar = line[j + 1] || '';

      if (char === '"' && !inQuotes) {
        inQuotes = true;
      } else if (char === '"' && inQuotes && nextChar !== '"') {
        inQuotes = false;
      } else if (char === '"' && inQuotes && nextChar === '"') {
        current += '"';
        j++;
      } else if (char === ',' && !inQuotes) {
        values.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }
    values.push(current.trim());

    // Criar objeto do post
    if (values.length === headers.length) {
      const post = {};
      headers.forEach((header, idx) => {
        post[header] = values[idx] || '';
      });

      // Garantir que likes e reposts sejam números
      post.likes = parseInt(post.likes) || 0;
      post.reposts = parseInt(post.reposts) || 0;

      // Extrair username de person_id (remover @)
      const username = post.person_id.replace(/^@/, '');
      post.username = username;

      // Definir account_type com base no username
      const isVerified = /oficial|news|real|rp|tech|crypto|br|456|123/i.test(username);
      post.account_type = isVerified ? 'verified' : 'regular';

      posts.push(post);
    }
  }
  
  return posts;
}

// Renderizar posts
function renderPosts(postsToRender) {
  const container = document.getElementById('posts-container');
  
  if (postsToRender.length === 0) {
    container.innerHTML = '<p style="text-align: center; color: #FF6B6B;">Nenhum tweet encontrado para esta data.</p>';
    return;
  }

  container.innerHTML = '';
  postsToRender.forEach(post => {
    const postEl = document.createElement('div');
    postEl.className = 'xis-post';
    postEl.dataset.postId = post.post_id;

    postEl.innerHTML = `
      <div class="post-header">
        <span class="username">@${post.username}</span>
        <span class="account-type">${post.account_type}</span>
      </div>
      <div class="text">${post.text}</div>
      <div class="post-meta">
        <span class="timestamp">${post.timestamp}</span>
        <span class="likes">👍 ${post.likes}</span>
        <span class="reposts">🔄 ${post.reposts}</span>
      </div>
    `;

    container.appendChild(postEl);
  });
}

// Filtro por data
function filterByDate() {
  const selectedDate = document.getElementById('date-filter').value;
  
  if (!selectedDate) {
    renderPosts(allPosts);
    return;
  }

  const filtered = allPosts.filter(post => {
    const postDate = post.timestamp.split('T')[0];
    return postDate === selectedDate;
  });

  renderPosts(filtered);
}

// Carregar data.csv automaticamente
window.addEventListener('DOMContentLoaded', async () => {
  try {
    console.log('🔍 Iniciando carregamento do CSV...');
    console.log('📍 URL atual:', window.location.href);
    console.log('📂 Tentando carregar: data.csv');
    
    // Tenta múltiplos caminhos
    const possiveisCaminhos = [
      'data.csv',
      './data.csv',
      '/data.csv',
      window.location.pathname + 'data.csv'
    ];
    
    let csvText = null;
    let caminhoSucesso = null;
    
    for (const caminho of possiveisCaminhos) {
      try {
        console.log(`🔄 Tentando: ${caminho}`);
        const response = await fetch(caminho);
        
        if (response.ok) {
          csvText = await response.text();
          caminhoSucesso = caminho;
          console.log(`✅ Sucesso com: ${caminho}`);
          break;
        } else {
          console.log(`❌ Falhou: ${caminho} (Status: ${response.status})`);
        }
      } catch (e) {
        console.log(`❌ Erro em: ${caminho}`, e.message);
      }
    }
    
    if (!csvText) {
      throw new Error('Arquivo não encontrado em nenhum dos caminhos testados');
    }
    
    console.log('📄 CSV carregado! Tamanho:', csvText.length, 'caracteres');
    console.log('📝 Primeiras linhas:', csvText.substring(0, 300));
    
    allPosts = parseCSV(csvText);
    console.log(`✅ ${allPosts.length} posts carregados com sucesso!`);
    
    if (allPosts.length > 0) {
      console.log('📊 Exemplo do primeiro post:', allPosts[0]);
    }
    
    renderPosts(allPosts);
    
    // Adicionar event listener para o filtro de data
    document.getElementById('date-filter').addEventListener('change', filterByDate);
    
  } catch (err) {
    console.error('❌ Erro detalhado:', err);
    console.error('Stack:', err.stack);
    
    document.getElementById('posts-container').innerHTML = `
      <p style="color: #FF6B6B; text-align: center; padding: 20px;">
        ❌ Falha ao carregar <code>data.csv</code><br>
        <strong>Erro:</strong> ${err.message}<br><br>
        
        <strong>🔍 Checklist de Debug:</strong>
        <ol style="text-align: left; max-width: 500px; margin: 20px auto; line-height: 1.8;">
          <li>Abra o <strong>Console</strong> (F12) e veja os logs detalhados</li>
          <li>Verifique se <code>data.csv</code> está na raiz do repositório</li>
          <li>Tente acessar diretamente: <a href="data.csv" target="_blank" style="color: #667eea;">SEU-SITE/data.csv</a></li>
          <li>Confirme que fez commit + push do arquivo</li>
          <li>Aguarde 2-3 minutos após o push (cache do GitHub Pages)</li>
        </ol>
        
        <button onclick="location.reload()" style="margin-top: 20px; padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer;">
          🔄 Tentar Novamente
        </button>
      </p>
    `;
  }
});