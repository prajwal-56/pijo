// api.js — Centralized API Client for PIJO with Multi-Team Workspace Support

const urlParams = new URLSearchParams(window.location.search);
const inviteTeam = urlParams.get('team');
if (inviteTeam) {
  localStorage.setItem('pijo_team_id', inviteTeam);
}

const API = {
  base: '',
  currentTeamId: localStorage.getItem('pijo_team_id') || 'team-default',

  async _req(method, path, body = null, isForm = false) {
    const opts = { method, headers: {} };

    // Attach active Team ID header on every request
    opts.headers['X-Team-Id'] = this.currentTeamId;

    if (body) {
      if (isForm) {
        opts.body = body; // FormData handles its own boundary
      } else {
        opts.headers['Content-Type'] = 'application/json';
        opts.body = JSON.stringify(body);
      }
    }
    const res = await fetch(this.base + path, opts);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Request failed');
    }
    return res.json();
  },

  // Teams Workspace API
  getTeams: () => API._req('GET', '/api/teams/'),
  getTeam: (id) => API._req('GET', `/api/teams/${id}`),
  createTeam: (data) => API._req('POST', '/api/teams/', data),
  deleteTeam: (id) => API._req('DELETE', `/api/teams/${id}`),
  setCurrentTeam: (teamId) => {
    API.currentTeamId = teamId;
    localStorage.setItem('pijo_team_id', teamId);
  },

  // Members API (Scoped to active team)
  getMembers: () => API._req('GET', '/api/members/'),
  getMember: (id) => API._req('GET', `/api/members/${id}`),
  createMember: (formData) => API._req('POST', '/api/members/', formData, true),
  deleteMember: (id) => API._req('DELETE', `/api/members/${id}`),
  extractSkills: (id) => API._req('POST', `/api/members/${id}/extract-skills`),

  // Tasks API (Scoped to active team)
  getTasks: () => API._req('GET', '/api/tasks/'),
  createTask: (data) => API._req('POST', '/api/tasks/', data),
  uploadTasksCSV: (formData) => API._req('POST', '/api/tasks/upload', formData, true),
  updateTaskStatus: (id, status) => API._req('PATCH', `/api/tasks/${id}/status`, { status }),
  assignTask: (id, member_id, reason = 'Manually assigned') => API._req('PATCH', `/api/tasks/${id}/assign`, { member_id, reason }),
  aiAssign: () => API._req('POST', '/api/tasks/assign'),
  aiPrioritize: () => API._req('POST', '/api/tasks/prioritize'),
  deleteTask: (id) => API._req('DELETE', `/api/tasks/${id}`),
  clearTasks: () => API._req('DELETE', '/api/tasks/'),
  getColumns: () => API._req('GET', '/api/tasks/columns'),
  addColumn: (data) => API._req('POST', '/api/tasks/columns', data),
  deleteColumn: (id) => API._req('DELETE', `/api/tasks/columns/${id}`),

  // AI Assistant API (Scoped to active team)
  chat: (message) => API._req('POST', '/api/ai/chat', { message }),
  summary: () => API._req('GET', '/api/ai/summary'),
};

window.API = API;
