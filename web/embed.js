// Floating "Study Assistant" chat bubble for Moodle pages.
// Add to Moodle: Site administration > Appearance > Additional HTML > "Before BODY is closed":
//   <script src="http://localhost:8000/embed.js"></script>
(function () {
  if (window.__studyAssistant) return;
  window.__studyAssistant = true;

  // Don't show on the login page or to signed-out visitors.
  var body = document.body;
  if (!body || body.id === 'page-login-index' || body.classList.contains('notloggedin')) return;

  var origin = new URL(document.currentScript.src).origin;

  var css = document.createElement('style');
  css.textContent =
    '#sa-btn{position:fixed;right:22px;bottom:22px;z-index:2147483000;width:58px;height:58px;border-radius:50%;' +
    'border:none;background:#0f6cbf;color:#fff;box-shadow:0 4px 14px rgba(0,0,0,.25);cursor:pointer;' +
    'display:flex;align-items:center;justify-content:center;transition:transform .15s}' +
    '#sa-btn:hover{transform:scale(1.06)}#sa-btn svg{width:28px;height:28px}' +
    '#sa-panel{position:fixed;right:22px;bottom:92px;z-index:2147483000;width:380px;height:560px;' +
    'max-width:calc(100vw - 32px);max-height:calc(100vh - 120px);border:none;border-radius:14px;' +
    'box-shadow:0 10px 36px rgba(0,0,0,.28);background:#fff;display:none}' +
    '#sa-panel.open{display:block}' +
    '@media (max-width:480px){#sa-panel{right:16px;left:16px;width:auto;bottom:86px}#sa-btn{right:16px;bottom:16px}}';
  document.head.appendChild(css);

  var btn = document.createElement('button');
  btn.id = 'sa-btn';
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Open Study Assistant');
  btn.title = 'Study Assistant';
  btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
    '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>';

  var panel = document.createElement('iframe');
  panel.id = 'sa-panel';
  panel.title = 'Study Assistant';
  var loaded = false;

  function toggle(open) {
    if (open && !loaded) { panel.src = origin + '/?embed=1'; loaded = true; }
    panel.classList.toggle('open', open);
    btn.setAttribute('aria-label', open ? 'Close Study Assistant' : 'Open Study Assistant');
  }
  btn.addEventListener('click', function () { toggle(!panel.classList.contains('open')); });
  window.addEventListener('message', function (e) {
    if (e.origin === origin && e.data === 'study-assistant:close') toggle(false);
  });

  body.appendChild(panel);
  body.appendChild(btn);
})();
