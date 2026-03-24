const runtimeConfig = window.__APP_CONFIG__ || {};
const apiBaseUrl = (runtimeConfig.API_BASE_URL || '').replace(/\/$/, '');
const API_URL = apiBaseUrl ? `${apiBaseUrl}/buscar` : '/api/buscar';

function scoreClass(s) {
  if (s >= 0.6) return 'high';
  if (s >= 0.45) return 'mid';
  return 'low';
}

function descricao(s) {
  if (s >= 0.75) return 'você é praticamente Sabotage, mano';
  if (s >= 0.60) return 'flow parecido, respeito';
  if (s >= 0.45) return 'tem alguma vibe, continua treinando';
  return 'ainda longe da quebrada';
}

function truncate(txt, max) {
  return txt.length > max ? txt.slice(0, max) + '...' : txt;
}

async function buscar() {
  const query = document.getElementById('query').value.trim();
  const topk  = parseInt(document.getElementById('topk').value);
  const btn   = document.getElementById('btnAnalyze');
  const loading    = document.getElementById('loading');
  const errorMsg   = document.getElementById('errorMsg');
  const scoreGeral = document.getElementById('scoreGeral');
  const resultsDiv = document.getElementById('results');
  const resultsHeader = document.getElementById('resultsHeader');

  if (!query) {
    mostrarErro('// escreve alguma coisa primeiro');
    return;
  }

  // Reset
  errorMsg.classList.remove('visible');
  scoreGeral.classList.remove('visible');
  resultsHeader.classList.remove('visible');
  resultsDiv.innerHTML = '';
  btn.disabled = true;
  loading.classList.add('visible');

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
      body: JSON.stringify({ texto: query, top_k: topk }),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    const resultados = data.resultados || [];

    if (!resultados.length) {
      mostrarErro('// nenhum resultado encontrado');
      return;
    }

    // Score geral = média dos scores
    const media = resultados.reduce((sum, r) => sum + r.score, 0) / resultados.length;
    const pct = Math.round(media * 100);
    const cls = scoreClass(media);

    document.getElementById('scoreGeralValue').textContent = pct + '%';
    document.getElementById('scoreGeralDesc').textContent = descricao(media);
    scoreGeral.classList.add('visible');
    resultsHeader.classList.add('visible');

    // Renderiza cards
    resultados.forEach((r, i) => {
      const s = Math.round(r.score * 100);
      const c = scoreClass(r.score);
      const card = document.createElement('div');
      card.className = 'result-card';
      card.innerHTML = `
        <div class="result-top">
          <div>
            <div class="result-title">${r.titulo}</div>
            <a class="result-link" href="${r.url}" target="_blank" rel="noopener">// vagalume ↗</a>
          </div>
          <div class="score-pill score-${c}">${s}%</div>
        </div>
        <div class="result-text">${truncate(r.trecho, 200)}</div>
        <div class="bar-track">
          <div class="bar-fill bar-${c}" id="bar-${i}" style="width:0%"></div>
        </div>
      `;
      resultsDiv.appendChild(card);

      // Animação escalonada
      setTimeout(() => {
        card.classList.add('visible');
        setTimeout(() => {
          document.getElementById(`bar-${i}`).style.width = s + '%';
        }, 100);
      }, i * 120);
    });

  } catch (err) {
    mostrarErro(`// erro ao conectar com o backend: ${err.message}`);
  } finally {
    loading.classList.remove('visible');
    btn.disabled = false;
  }
}

function mostrarErro(msg) {
  const el = document.getElementById('errorMsg');
  el.textContent = msg;
  el.classList.add('visible');
}

// Enter para enviar (Shift+Enter = nova linha)
document.getElementById('query').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    buscar();
  }
});
