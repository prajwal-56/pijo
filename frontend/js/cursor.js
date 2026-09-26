// cursor.js — Custom Neobrutal Cursor, Antigravity Physics Particles & Background Pencil Canvas

(function () {
  // Check if touch device
  const isTouch = window.matchMedia('(pointer: coarse)').matches;

  // =========================================================================
  // 1. AMBIENT BACKGROUND PARTICLES (ANTIGRAVITY STYLE REPULSION)
  // =========================================================================
  const bgCanvas = document.createElement('canvas');
  bgCanvas.id = 'ambient-particles-canvas';
  bgCanvas.style.position = 'fixed';
  bgCanvas.style.top = '0';
  bgCanvas.style.left = '0';
  bgCanvas.style.width = '100vw';
  bgCanvas.style.height = '100vh';
  bgCanvas.style.pointerEvents = 'none';
  bgCanvas.style.zIndex = '0';
  bgCanvas.style.opacity = '0.75';
  document.body.prepend(bgCanvas);

  const bgCtx = bgCanvas.getContext('2d');
  let bgWidth = (bgCanvas.width = window.innerWidth);
  let bgHeight = (bgCanvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    bgWidth = bgCanvas.width = window.innerWidth;
    bgHeight = bgCanvas.height = window.innerHeight;
    doodleWidth = doodleCanvas.width = window.innerWidth;
    doodleHeight = doodleCanvas.height = window.innerHeight;
  });

  const particlePalette = ['#121212', '#FFE600', '#FF6584', '#00F0FF', '#38EF7D', '#9D4EDD'];
  const ambientParticles = [];
  const particleCount = 45;

  let mousePos = { x: -500, y: -500 };

  class AmbientParticle {
    constructor() {
      this.x = Math.random() * bgWidth;
      this.y = Math.random() * bgHeight;
      this.originX = this.x;
      this.originY = this.y;
      this.vx = (Math.random() - 0.5) * 0.6;
      this.vy = (Math.random() - 0.5) * 0.6;
      this.size = Math.random() * 6 + 4;
      this.shape = ['square', 'circle', 'plus'][Math.floor(Math.random() * 3)];
      this.color = particlePalette[Math.floor(Math.random() * particlePalette.length)];
      this.rotation = Math.random() * Math.PI;
      this.rotSpeed = (Math.random() - 0.5) * 0.02;
    }

    update() {
      // Normal drift
      this.x += this.vx;
      this.y += this.vy;
      this.rotation += this.rotSpeed;

      // Wrap around bounds
      if (this.x < -20) this.x = bgWidth + 20;
      if (this.x > bgWidth + 20) this.x = -20;
      if (this.y < -20) this.y = bgHeight + 20;
      if (this.y > bgHeight + 20) this.y = -20;

      // Cursor interaction (Antigravity physics repulsion)
      const dx = this.x - mousePos.x;
      const dy = this.y - mousePos.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const repelDist = 120;

      if (dist < repelDist && dist > 0) {
        const force = (repelDist - dist) / repelDist;
        const angle = Math.atan2(dy, dx);
        this.x += Math.cos(angle) * force * 5.5;
        this.y += Math.sin(angle) * force * 5.5;
      }
    }

    draw(ctx) {
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);
      ctx.fillStyle = this.color;
      ctx.strokeStyle = '#121212';
      ctx.lineWidth = 1.5;

      const s = this.size;
      if (this.shape === 'square') {
        ctx.fillRect(-s / 2, -s / 2, s, s);
        ctx.strokeRect(-s / 2, -s / 2, s, s);
      } else if (this.shape === 'circle') {
        ctx.beginPath();
        ctx.arc(0, 0, s / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
      } else if (this.shape === 'plus') {
        ctx.beginPath();
        ctx.moveTo(-s / 2, 0);
        ctx.lineTo(s / 2, 0);
        ctx.moveTo(0, -s / 2);
        ctx.lineTo(0, s / 2);
        ctx.stroke();
      }
      ctx.restore();
    }
  }

  for (let i = 0; i < particleCount; i++) {
    ambientParticles.push(new AmbientParticle());
  }

  function loopAmbientParticles() {
    bgCtx.clearRect(0, 0, bgWidth, bgHeight);
    for (let p of ambientParticles) {
      p.update();
      p.draw(bgCtx);
    }
    requestAnimationFrame(loopAmbientParticles);
  }
  requestAnimationFrame(loopAmbientParticles);

  // =========================================================================
  // 2. BACKGROUND PENCIL / DOODLE CANVAS & FLOATING TOOLBAR
  // =========================================================================
  const doodleCanvas = document.createElement('canvas');
  doodleCanvas.id = 'doodle-canvas';
  doodleCanvas.style.position = 'fixed';
  doodleCanvas.style.top = '0';
  doodleCanvas.style.left = '0';
  doodleCanvas.style.width = '100vw';
  doodleCanvas.style.height = '100vh';
  doodleCanvas.style.pointerEvents = 'none'; // active when pencil mode is on
  doodleCanvas.style.zIndex = '5';
  document.body.appendChild(doodleCanvas);

  const dCtx = doodleCanvas.getContext('2d');
  let doodleWidth = (doodleCanvas.width = window.innerWidth);
  let doodleHeight = (doodleCanvas.height = window.innerHeight);

  let isPencilActive = false;
  let isDrawing = false;
  let pencilColor = '#121212';
  let pencilSize = 3.5;
  let lastDoodlePos = { x: 0, y: 0 };

  // Floating Pencil Toolbar
  const toolbar = document.createElement('div');
  toolbar.id = 'doodle-toolbar';
  toolbar.className = 'doodle-toolbar';
  toolbar.innerHTML = `
    <button id="btn-toggle-pencil" class="btn btn-sm" title="Toggle Pencil Draw Mode">
      <span class="pencil-icon">Pencil</span>
    </button>
    <div id="doodle-colors" class="doodle-colors" style="display:none;">
      <button class="color-dot dot-black active" data-color="#121212"></button>
      <button class="color-dot dot-yellow" data-color="#FFE600"></button>
      <button class="color-dot dot-pink" data-color="#FF6584"></button>
      <button class="color-dot dot-cyan" data-color="#00F0FF"></button>
      <button id="btn-clear-doodle" class="btn btn-sm btn-danger" style="padding:0.2rem 0.5rem; font-size:0.7rem;" title="Clear Canvas">Clear</button>
    </div>
  `;
  document.body.appendChild(toolbar);

  const togglePencilBtn = document.getElementById('btn-toggle-pencil');
  const doodleColors = document.getElementById('doodle-colors');
  const clearDoodleBtn = document.getElementById('btn-clear-doodle');

  togglePencilBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    isPencilActive = !isPencilActive;
    if (isPencilActive) {
      doodleCanvas.style.pointerEvents = 'auto';
      doodleCanvas.style.zIndex = '99990';
      togglePencilBtn.classList.add('btn-primary');
      togglePencilBtn.innerHTML = 'Draw: ON';
      doodleColors.style.display = 'flex';
      if (cursorOuter) cursorOuter.classList.add('cursor-pencil');
      if (window.showToast) window.showToast('Pencil mode active: click & drag to doodle on page!', 'info');
    } else {
      doodleCanvas.style.pointerEvents = 'none';
      doodleCanvas.style.zIndex = '5';
      togglePencilBtn.classList.remove('btn-primary');
      togglePencilBtn.innerHTML = 'Pencil';
      doodleColors.style.display = 'none';
      if (cursorOuter) cursorOuter.classList.remove('cursor-pencil');
    }
  });

  toolbar.querySelectorAll('.color-dot').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      toolbar.querySelectorAll('.color-dot').forEach((d) => d.classList.remove('active'));
      btn.classList.add('active');
      pencilColor = btn.dataset.color;
    });
  });

  clearDoodleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    dCtx.clearRect(0, 0, doodleWidth, doodleHeight);
    if (window.showToast) window.showToast('Doodles cleared', 'info');
  });

  doodleCanvas.addEventListener('mousedown', (e) => {
    if (!isPencilActive) return;
    isDrawing = true;
    lastDoodlePos = { x: e.clientX, y: e.clientY };
  });

  window.addEventListener('mouseup', () => {
    isDrawing = false;
  });

  doodleCanvas.addEventListener('mousemove', (e) => {
    if (!isPencilActive || !isDrawing) return;
    dCtx.beginPath();
    dCtx.moveTo(lastDoodlePos.x, lastDoodlePos.y);
    dCtx.lineTo(e.clientX, e.clientY);
    dCtx.strokeStyle = pencilColor;
    dCtx.lineWidth = pencilSize;
    dCtx.lineCap = 'round';
    dCtx.lineJoin = 'round';
    dCtx.stroke();
    lastDoodlePos = { x: e.clientX, y: e.clientY };
  });

  // =========================================================================
  // 3. NEOBRUTAL CUSTOM CURSOR
  // =========================================================================
  if (isTouch) return;

  const cursorDot = document.createElement('div');
  cursorDot.id = 'neo-cursor-dot';
  cursorDot.className = 'neo-cursor-dot';
  document.body.appendChild(cursorDot);

  const cursorOuter = document.createElement('div');
  cursorOuter.id = 'neo-cursor-outer';
  cursorOuter.className = 'neo-cursor-outer';
  document.body.appendChild(cursorOuter);

  let currentX = -100;
  let currentY = -100;
  let targetX = -100;
  let targetY = -100;

  window.addEventListener('mousemove', (e) => {
    mousePos.x = e.clientX;
    mousePos.y = e.clientY;
    targetX = e.clientX;
    targetY = e.clientY;

    cursorDot.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
  });

  function renderCursor() {
    currentX += (targetX - currentX) * 0.22;
    currentY += (targetY - currentY) * 0.22;
    cursorOuter.style.transform = `translate3d(${currentX}px, ${currentY}px, 0)`;
    requestAnimationFrame(renderCursor);
  }
  requestAnimationFrame(renderCursor);

  // Hover states for links & buttons
  const interactiveSelector = 'a, button, input, select, textarea, .task-card, .nav-link, .stat-card, [draggable="true"]';
  document.addEventListener('mouseover', (e) => {
    if (e.target.closest(interactiveSelector)) {
      cursorOuter.classList.add('cursor-hover');
    }
  });

  document.addEventListener('mouseout', (e) => {
    if (e.target.closest(interactiveSelector)) {
      cursorOuter.classList.remove('cursor-hover');
    }
  });

  document.addEventListener('mousedown', () => {
    cursorOuter.classList.add('cursor-active');
  });

  document.addEventListener('mouseup', () => {
    cursorOuter.classList.remove('cursor-active');
  });
})();
