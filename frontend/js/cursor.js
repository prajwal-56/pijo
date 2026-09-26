// cursor.js — Interactive Neobrutalism Particle Trail & Micro-Burst

(function () {
  // Respect touch devices / small screens
  if (window.matchMedia('(pointer: coarse)').matches) return;

  const canvas = document.createElement('canvas');
  canvas.id = 'neo-cursor-canvas';
  canvas.style.position = 'fixed';
  canvas.style.top = '0';
  canvas.style.left = '0';
  canvas.style.width = '100vw';
  canvas.style.height = '100vh';
  canvas.style.pointerEvents = 'none';
  canvas.style.zIndex = '99999';
  document.body.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const colors = ['#FFE600', '#FF6584', '#00F0FF', '#38EF7D', '#9D4EDD', '#121212'];
  const particles = [];
  const maxParticles = 40;

  let mouseX = -100;
  let mouseY = -100;
  let lastSpawn = 0;

  class Particle {
    constructor(x, y, isClick = false) {
      this.x = x;
      this.y = y;
      this.color = colors[Math.floor(Math.random() * colors.length)];
      this.size = isClick ? Math.random() * 8 + 5 : Math.random() * 5 + 3;
      const angle = isClick ? Math.random() * Math.PI * 2 : Math.random() * Math.PI * 2;
      const speed = isClick ? Math.random() * 4 + 2 : Math.random() * 1.5 + 0.5;
      this.vx = Math.cos(angle) * speed;
      this.vy = Math.sin(angle) * speed - (isClick ? 1 : 0.5);
      this.life = 1;
      this.decay = isClick ? Math.random() * 0.03 + 0.02 : Math.random() * 0.04 + 0.03;
      this.shape = Math.random() > 0.4 ? 'square' : 'circle';
      this.rotation = Math.random() * Math.PI;
      this.rotSpeed = (Math.random() - 0.5) * 0.1;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.vy += 0.08; // mild gravity
      this.rotation += this.rotSpeed;
      this.life -= this.decay;
    }

    draw(ctx) {
      if (this.life <= 0) return;
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);
      ctx.globalAlpha = Math.max(0, this.life);
      ctx.fillStyle = this.color;
      ctx.strokeStyle = '#121212';
      ctx.lineWidth = 1.5;

      const half = this.size / 2;
      if (this.shape === 'square') {
        ctx.fillRect(-half, -half, this.size, this.size);
        ctx.strokeRect(-half, -half, this.size, this.size);
      } else {
        ctx.beginPath();
        ctx.arc(0, 0, half, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
      }
      ctx.restore();
    }
  }

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;

    const now = performance.now();
    if (now - lastSpawn > 24 && particles.length < maxParticles) {
      particles.push(new Particle(mouseX, mouseY, false));
      lastSpawn = now;
    }
  });

  window.addEventListener('click', (e) => {
    // Click confetti burst!
    for (let i = 0; i < 10; i++) {
      particles.push(new Particle(e.clientX, e.clientY, true));
    }
    // Also trigger tactile click sound
    if (window.playPopSound) {
      window.playPopSound();
    }
  });

  function render() {
    ctx.clearRect(0, 0, width, height);

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.update();
      p.draw(ctx);
      if (p.life <= 0) {
        particles.splice(i, 1);
      }
    }

    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);
})();
