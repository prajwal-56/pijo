// teams.js — Multi-Team Workspace Switcher & Team Hub Component

(function () {
  let allTeams = [];
  let currentTeam = null;

  async function loadTeamsData() {
    try {
      allTeams = await API.getTeams();
      if (!allTeams || allTeams.length === 0) {
        allTeams = [{ id: 'team-default', name: 'Alpha Hackers', description: 'Primary workspace' }];
      }

      currentTeam = allTeams.find(t => t.id === API.currentTeamId) || allTeams[0];
      if (currentTeam.id !== API.currentTeamId) {
        API.setCurrentTeam(currentTeam.id);
      }

      updateTeamSwitcherUI();
    } catch (err) {
      console.warn('Failed to load teams:', err);
    }
  }

  function updateTeamSwitcherUI() {
    const badge = document.getElementById('active-team-badge');
    const nameEl = document.getElementById('active-team-name');
    const countEl = document.getElementById('team-total-count');
    const listEl = document.getElementById('team-list-items');

    if (badge && currentTeam) {
      badge.textContent = currentTeam.name.charAt(0).toUpperCase();
    }
    if (nameEl && currentTeam) {
      nameEl.textContent = currentTeam.name;
    }
    if (countEl) {
      countEl.textContent = allTeams.length;
    }

    if (listEl) {
      listEl.innerHTML = allTeams.map(t => {
        const isActive = t.id === currentTeam.id;
        return `
          <div class="team-item-row ${isActive ? 'active' : ''}" onclick="switchTeam('${t.id}')">
            <div style="display:flex; align-items:center; gap:0.6rem; overflow:hidden;">
              <span class="team-avatar-mini">${t.name.charAt(0).toUpperCase()}</span>
              <div style="overflow:hidden;">
                <div style="font-family:var(--font-heading); font-weight:800; font-size:0.85rem; text-overflow:ellipsis; overflow:hidden; white-space:nowrap;">
                  ${t.name}
                </div>
                <div style="font-size:0.7rem; font-weight:600; color:rgba(18,18,18,0.65);">
                  ${t.member_count || 0} members · ${t.task_count || 0} tasks
                </div>
              </div>
            </div>
            ${isActive ? `<span class="badge badge-green" style="font-size:0.6rem; padding:0.15rem 0.35rem;">ACTIVE</span>` : ''}
          </div>
        `;
      }).join('');
    }

    // Update team banner on page if present
    const pageTeamName = document.getElementById('page-team-name');
    const pageTeamDesc = document.getElementById('page-team-desc');
    const pageTeamIdChip = document.getElementById('page-team-id-chip');

    if (pageTeamName && currentTeam) pageTeamName.textContent = currentTeam.name;
    if (pageTeamDesc && currentTeam) pageTeamDesc.textContent = currentTeam.description || 'Active Workspace';
    if (pageTeamIdChip && currentTeam) pageTeamIdChip.textContent = `ID: ${currentTeam.id}`;

    if (window.refreshIcons) window.refreshIcons();
  }

  function injectTeamSwitcher() {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;

    // Check if already injected
    if (document.getElementById('team-switcher-box')) return;

    const logoContainer = sidebar.querySelector('.logo-container');
    const switcherBox = document.createElement('div');
    switcherBox.id = 'team-switcher-box';
    switcherBox.className = 'team-switcher-box';
    switcherBox.innerHTML = `
      <button id="btn-team-dropdown" class="team-dropdown-btn" onclick="toggleTeamPopover(event)">
        <div style="display:flex; align-items:center; gap:0.6rem; overflow:hidden;">
          <span class="team-avatar-badge" id="active-team-badge">T</span>
          <span class="team-name-label" id="active-team-name">Alpha Hackers</span>
        </div>
        <i data-lucide="chevrons-up-down" style="width:16px; height:16px; flex-shrink:0;"></i>
      </button>

      <!-- Popover Menu -->
      <div id="team-menu-popover" class="team-menu-popover" style="display:none;">
        <div class="team-menu-header">
          <span>TEAMS & WORKSPACES</span>
          <span class="badge badge-yellow" id="team-total-count">1</span>
        </div>
        <div id="team-list-items" class="team-list-items">
          Loading workspaces...
        </div>
        <div class="team-menu-footer">
          <button class="btn btn-sm btn-cyan" style="width:100%; margin-bottom:0.4rem;" onclick="openCreateTeamModal()">
            <i data-lucide="plus" style="width:14px; height:14px;"></i> Create Team
          </button>
          <button class="btn btn-sm btn-yellow" style="width:100%;" onclick="copyTeamInviteLink()">
            <i data-lucide="link" style="width:14px; height:14px;"></i> Share Invite Link
          </button>
        </div>
      </div>
    `;

    if (logoContainer && logoContainer.nextSibling) {
      sidebar.insertBefore(switcherBox, logoContainer.nextSibling);
    } else {
      sidebar.prepend(switcherBox);
    }

    // Inject Create Team Modal if not already present
    if (!document.getElementById('create-team-modal')) {
      const modal = document.createElement('div');
      modal.id = 'create-team-modal';
      modal.className = 'modal-overlay';
      modal.innerHTML = `
        <div class="modal-content">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem;">
            <h3 style="font-family: var(--font-heading); font-size: 1.35rem; font-weight: 900;">
              Create New Team Workspace
            </h3>
            <button class="btn btn-sm btn-yellow" onclick="closeCreateTeamModal()">
              <i data-lucide="x" style="width:14px; height:14px;"></i>
            </button>
          </div>
          <form id="create-team-form" onsubmit="handleCreateTeam(event)">
            <div class="form-group">
              <label class="form-label">Team / Project Name *</label>
              <input type="text" id="new-team-name" class="form-control" placeholder="e.g. Fintech Titans, Robotics Team..." required>
            </div>
            <div class="form-group">
              <label class="form-label">Project Mission / Bio</label>
              <textarea id="new-team-desc" class="form-control" placeholder="What is this team building during the hackathon?"></textarea>
            </div>
            <div class="form-group" style="background:#FFFEE8; border:var(--border-thin); padding:0.85rem; border-radius:var(--radius-md);">
              <label style="display:flex; align-items:center; gap:0.6rem; cursor:pointer; font-weight:700; font-size:0.85rem;">
                <input type="checkbox" id="seed-template-checkbox" checked style="width:18px; height:18px; accent-color:var(--neo-black);">
                <span>Seed with Starter Hackathon Template (3 member profiles & 8 tasks)</span>
              </label>
            </div>
            <div style="display:flex; justify-content:flex-end; gap:0.6rem; margin-top:1.5rem;">
              <button type="button" class="btn" onclick="closeCreateTeamModal()">Cancel</button>
              <button type="submit" class="btn btn-pink" id="btn-save-new-team">
                <i data-lucide="check" style="width:16px; height:16px;"></i> Create Workspace
              </button>
            </div>
          </form>
        </div>
      `;
      document.body.appendChild(modal);
    }

    // Close popover when clicking outside
    document.addEventListener('click', (e) => {
      const popover = document.getElementById('team-menu-popover');
      const btn = document.getElementById('btn-team-dropdown');
      if (popover && btn && !btn.contains(e.target) && !popover.contains(e.target)) {
        popover.style.display = 'none';
      }
    });
  }

  window.toggleTeamPopover = function (e) {
    if (e) e.stopPropagation();
    const popover = document.getElementById('team-menu-popover');
    if (popover) {
      popover.style.display = popover.style.display === 'none' ? 'block' : 'none';
    }
  };

  window.switchTeam = function (teamId) {
    if (teamId === API.currentTeamId) {
      document.getElementById('team-menu-popover').style.display = 'none';
      return;
    }
    API.setCurrentTeam(teamId);
    if (window.showToast) window.showToast(`Switched workspace`, 'info');
    if (window.triggerConfetti) window.triggerConfetti();
    // Reload page data to reflect new team
    setTimeout(() => {
      window.location.search = `?team=${teamId}`;
    }, 250);
  };

  window.openCreateTeamModal = function () {
    const pop = document.getElementById('team-menu-popover');
    if (pop) pop.style.display = 'none';
    const modal = document.getElementById('create-team-modal');
    if (modal) {
      modal.classList.add('active');
      document.getElementById('new-team-name').focus();
    }
  };

  window.closeCreateTeamModal = function () {
    const modal = document.getElementById('create-team-modal');
    if (modal) modal.classList.remove('active');
  };

  window.handleCreateTeam = async function (e) {
    e.preventDefault();
    const name = document.getElementById('new-team-name').value.trim();
    const description = document.getElementById('new-team-desc').value.trim();
    const seed = document.getElementById('seed-template-checkbox').checked;
    if (!name) return;

    const btn = document.getElementById('btn-save-new-team');
    if (window.setLoading) window.setLoading(btn, true);

    try {
      const newTeam = await API.createTeam({ name, description, seed_template: seed });
      if (window.showToast) window.showToast(`Workspace "${name}" created!`, 'success');
      if (window.triggerConfetti) window.triggerConfetti();
      API.setCurrentTeam(newTeam.id);
      closeCreateTeamModal();
      setTimeout(() => {
        window.location.search = `?team=${newTeam.id}`;
      }, 350);
    } catch (err) {
      if (window.showToast) window.showToast(err.message, 'error');
    } finally {
      if (window.setLoading) window.setLoading(btn, false, '<i data-lucide="check" style="width:16px; height:16px;"></i> Create Workspace');
      if (window.refreshIcons) window.refreshIcons();
    }
  };

  window.copyTeamInviteLink = function () {
    const inviteUrl = `${window.location.origin}${window.location.pathname}?team=${API.currentTeamId}`;
    navigator.clipboard.writeText(inviteUrl).then(() => {
      if (window.showToast) window.showToast('Team invite link copied to clipboard!', 'success');
    }).catch(() => {
      prompt('Copy team link:', inviteUrl);
    });
    const pop = document.getElementById('team-menu-popover');
    if (pop) pop.style.display = 'none';
  };

  // Initialize on page load
  document.addEventListener('DOMContentLoaded', () => {
    injectTeamSwitcher();
    loadTeamsData();
  });

  // If DOM is already ready
  if (document.readyState === 'interactive' || document.readyState === 'complete') {
    injectTeamSwitcher();
    loadTeamsData();
  }

  window.refreshTeamUI = loadTeamsData;
})();
