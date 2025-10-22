let allPosts = [];

function renderPosts(postsToRender) {
  const container = document.getElementById('posts-container');
  if (postsToRender.length === 0) {
    container.innerHTML = '<p style="text-align: center; color: #FF6B6B;">Nenhum tweet encontrado.</p>';
    return;
  }

  container.innerHTML = '';
  postsToRender.forEach(post => {
    // Extrair username sem @
    const username = post.person_id.replace(/^@/, '');
    // Definir account_type com base no username
    const isVerified = /oficial|news|real|rp|tech|crypto|br|456|123/i.test(username);
    const accountType = isVerified ? 'verified' : 'regular';

    const postEl = document.createElement('div');
    postEl.className = 'xis-post';
    postEl.dataset.postId = post.post_id;

    postEl.innerHTML = `
      <div class="post-header">
        <span class="username">@${username}</span>
        <span class="account-type">${accountType}</span>
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

// Carregar data.json
window.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('data.json');
    if (!response.ok) throw new Error('Arquivo data.json não encontrado');
    allPosts = await response.json();
    renderPosts(allPosts);
    document.getElementById('date-filter').addEventListener('change', filterByDate);
  } catch (err) {
    console.error('Erro ao carregar data.json:', err);
    document.getElementById('posts-container').innerHTML = `
      <p style="color: #FF6B6B; text-align: center;">
        ❌ Falha ao carregar <code>data.json</code>.<br>
        Verifique se o arquivo está na mesma pasta e é um JSON válido.
      </p>
    `;
  }
});