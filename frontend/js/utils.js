// utils.js — Shared Utilities & UI Helpers

function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  const icons = { success: '✓', error: '✕', info: 'ℹ', warning: '⚠' };
  toast.innerHTML = `
    <span style="font-weight:bold;">${icons[type] || 'ℹ'}</span>
    <span>${message}</span>
  `;
  container.appendChild(toast);
  
  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function statusBadge(status) {
  const map = {
    todo: ['gray', 'To Do'],
    in_progress: ['blue', 'In Progress'],
    done: ['green', 'Done'],
    blocked: ['red', 'Blocked'],
  };
  const [color, label] = map[status] || ['gray', status || 'To Do'];
  return `<span class="badge badge-${color}">${label}</span>`;
}

function priorityBadge(priority) {
  const map = {
    low: ['green', '↓ Low'],
    medium: ['yellow', '→ Med'],
    high: ['orange', '↑ High'],
    critical: ['red', '🔥 Critical'],
  };
  const [color, label] = map[priority] || ['gray', priority || 'Medium'];
  return `<span class="badge badge-${color}">${label}</span>`;
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
    btn.innerHTML = '<span class="spinner"></span>';
    btn.disabled = true;
  } else {
    btn.innerHTML = text || btn.dataset.origText || 'Submit';
    btn.disabled = false;
  }
}

window.showToast = showToast;
window.statusBadge = statusBadge;
window.priorityBadge = priorityBadge;
window.avatarInitials = avatarInitials;
window.renderMemberAvatar = renderMemberAvatar;
window.relativeTime = relativeTime;
window.setLoading = setLoading;
