// utils.js — Neobrutalism UI Helpers & Markdown Parser (Emoji-Free Clean Design)

// Safe Markdown Parser helper
function renderMarkdown(content) {
  if (!content) return '';
  if (window.marked && typeof window.marked.parse === 'function') {
    try {
      const parsed = window.marked.parse(content, { breaks: true, gfm: true });
      if (window.DOMPurify && typeof window.DOMPurify.sanitize === 'function') {
        return window.DOMPurify.sanitize(parsed);
      }
      return parsed;
    } catch (e) {
      console.warn('Marked parse error, using fallback:', e);
    }
  }

  // Fallback simple markdown parser if library is offline
  let html = content
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*)\*/gim, '<em>$1</em>')
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    .replace(/^\s*-\s+(.*$)/gim, '<li>$1</li>')
    .replace(/\n\n/gim, '</p><p>');

  if (html.includes('<li>')) {
    html = html.replace(/(<li>.*<\/li>)/gim, '<ul>$1</ul>');
  }

  return `<p>${html}</p>`;
}

function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;

  const typeLabels = {
    success: 'SUCCESS',
    error: 'ERROR',
    info: 'INFO',
    warning: 'WARN'
  };

  toast.innerHTML = `
    <span class="badge badge-gray" style="font-size:0.65rem; padding:0.15rem 0.4rem; background:#121212; color:#fff;">${typeLabels[type] || 'NOTICE'}</span>
    <span>${message}</span>
  `;
  container.appendChild(toast);
  
  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3800);
}

function statusBadge(status) {
  const map = {
    todo: ['yellow', 'To Do'],
    in_progress: ['blue', 'In Progress'],
    done: ['green', 'Done'],
    blocked: ['red', 'Blocked'],
    dropped: ['gray', 'Dropped']
  };
  const [color, label] = map[status] || ['gray', status ? status.replace(/_/g, ' ') : 'To Do'];
  return `<span class="badge badge-${color}"><span class="status-dot dot-${color}"></span> ${label}</span>`;
}

function priorityBadge(priority) {
  const map = {
    low: ['green', 'Low'],
    medium: ['yellow', 'Medium'],
    high: ['orange', 'High'],
    critical: ['red', 'Critical'],
  };
  const [color, label] = map[priority] || ['gray', priority || 'Medium'];
  return `<span class="badge badge-${color}">${label.toUpperCase()}</span>`;
}

function avatarInitials(name) {
  if (!name) return '??';
  return name.trim().split(/\s+/).map(w => w[0]).join('').toUpperCase().slice(0, 2);
}

function renderMemberAvatar(member, sizeClass = '') {
  if (member && member.pfp) {
    return `<div class="avatar ${sizeClass}"><img src="${member.pfp}" alt="${member.name}" onerror="this.onerror=null; this.parentElement.innerText='${avatarInitials(member.name)}';"></div>`;
  }
  return `<div class="avatar ${sizeClass}">${avatarInitials(member ? member.name : '??')}</div>`;
}

function relativeTime(iso) {
  if (!iso) return 'recently';
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

function setLoading(btn, loading, text = null) {
  if (!btn) return;
  if (loading) {
    btn.dataset.origText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner"></span> Working...';
    btn.disabled = true;
  } else {
    btn.innerHTML = text || btn.dataset.origText || 'Submit';
    btn.disabled = false;
  }
}

// Refresh Lucide icons if loaded
function refreshIcons() {
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }
}

window.renderMarkdown = renderMarkdown;
window.showToast = showToast;
window.statusBadge = statusBadge;
window.priorityBadge = priorityBadge;
window.avatarInitials = avatarInitials;
window.renderMemberAvatar = renderMemberAvatar;
window.relativeTime = relativeTime;
window.setLoading = setLoading;
window.refreshIcons = refreshIcons;
