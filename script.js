let allPosts = [];

// Função para parsear CSV (lida com aspas e vírgulas no texto)
function parseCSV(csvText) {
  const lines = csvText.split('\n').filter(line => line.trim() !== '');
  const headers = lines[0].split(',').map(h => h.trim());
  const posts = [];

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    const values = [];
    let current = '';
    let inQuotes = false;

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

// Renderizar posts (sem edição!)
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
        <span class="reposts">🔁 ${post.reposts}</span>
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
    const response = await fetch('data.json');  
    if (!response.ok) throw new Error('Arquivo data.csv não encontrado');
    const csvText = await response.text();
    allPosts = parseCSV(csvText);
    renderPosts(allPosts);
    document.getElementById('date-filter').addEventListener('change', filterByDate);
  } catch (err) {
    console.error('Erro ao carregar data.csv:', err);
    document.getElementById('posts-container').innerHTML = `
      <p style="color: #FF6B6B; text-align: center;">
        ❌ Falha ao carregar <code>data.csv</code>.<br>
        Verifique se o arquivo está na mesma pasta do site.
      </p>
    `;
  }
});