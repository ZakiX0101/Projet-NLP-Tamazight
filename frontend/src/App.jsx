import { useState } from 'react'
import './App.css'
// Inter font via Google Fonts (loaded once)
if (!document.querySelector('#inter-font')) {
  const link = Object.assign(document.createElement('link'), {
    id: 'inter-font',
    rel: 'stylesheet',
    href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap',
  });
  document.head.appendChild(link);
}

function App() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleTranslate = async () => {
    if (!inputText.trim()) return;

    setIsLoading(true);
    setOutputText('');

    try {
      const response = await fetch('http://localhost:8000/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) throw new Error('Erreur réseau');

      const data = await response.json();
      setOutputText(data.target_zgh);
    } catch (error) {
      setOutputText("Erreur lors de la traduction. Vérifiez que l'API est lancée.");
    } finally {
      setIsLoading(false);
    }
  };

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setInputText(text);
    } catch {
      /* clipboard access denied */
    }
  };

  return (
    <div className="app">
      {/* ── Navbar ─────────────────────────────────────────── */}
      <nav className="navbar">
        <span className="nav-brand">NLP<span className="nav-brand-accent">TMZ</span></span>
        <div className="nav-center">
          <h1 className="nav-title">Traducteur Arabe ➔ Tamazight</h1>
          <p className="nav-subtitle">Basé sur l'architecture Transformer (NLLB)</p>
        </div>
      </nav>

      {/* ── Language selector bar ───────────────────────────── */}
      <div className="lang-bar">
        <div className="lang-bar-inner">
          <button className="lang-pill active-lang" disabled>Arabe</button>
          <span className="swap-icon" title="Direction fixe">⇄</span>
          <button className="lang-pill active-lang" disabled>Tamazight (Tifinagh)</button>
        </div>
      </div>

      {/* ── Split panels ────────────────────────────────────── */}
      <main className="panels">
        {/* Left — Input */}
        <div className="panel panel-left">
          <textarea
            className="panel-textarea"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Saisir le texte…"
            dir="rtl"
            aria-label="Texte source en arabe"
          />
          <div className="panel-actions">
            <button className="paste-btn" onClick={handlePaste}>
              ⎘ Coller le texte
            </button>
            {inputText && (
              <button className="clear-btn" onClick={() => { setInputText(''); setOutputText(''); }}>
                ✕ Effacer
              </button>
            )}
          </div>
        </div>

        {/* Divider */}
        <div className="divider" />

        {/* Right — Output */}
        <div className="panel panel-right">
          {outputText ? (
            <textarea
              className="panel-textarea output-text"
              value={outputText}
              readOnly
              aria-label="Traduction en Tamazight"
            />
          ) : (
            <p className="output-placeholder">
              {isLoading ? 'Traduction en cours…' : 'La traduction apparaîtra ici…'}
            </p>
          )}
        </div>
      </main>

      {/* ── Bottom action bar ───────────────────────────────── */}
      <div className="bottom-bar">
        <button
          className="translate-btn"
          onClick={handleTranslate}
          disabled={isLoading || !inputText.trim()}
        >
          {isLoading ? 'Traduction…' : '→ Traduire'}
        </button>
      </div>

      {/* ── Footer ──────────────────────────────────────────── */}
      <footer className="footer">
        <p>Projet NLP réalisé par Aymane El Akkioui et Zakaria Bellil</p>
      </footer>
    </div>
  );
}

export default App