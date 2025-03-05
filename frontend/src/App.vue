<template>
  <div class="main-layout">
    <!-- Шапка с кнопками -->
    <div class="header">
      <div class="header-buttons">
        <button v-if="isAuthenticated && currentUserRole === 'admin'" @click="goToAdmin" class="admin-button">
          Admin Panel
        </button>
        <button v-if="isAuthenticated" @click="logout" class="logout-button">
          Logout
        </button>
      </div>
    </div>

    <!-- Боковая панель -->
    <div class="sidebar">
      <div class="logo">Velocimetry</div>
      <ul>
        <li v-if="!isAuthenticated" @click="openLoginModal">Login</li>
        <li v-if="isAuthenticated" @click="goToProjects" :class="{ active: currentView === 'projects' }">
          Projects
          <ul v-if="selectedProject">
            <li @click.stop="goToFiles" :class="{ active: currentView === 'files' }">
              Files
              <ul v-if="selectedFile">
                <li @click.stop="goToEstimates" :class="{ active: currentView === 'estimates' }">
                  Estimates
                </li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </div>

    <!-- Основная часть -->
    <div class="content">
      <button v-if="isAuthenticated && currentView !== 'projects'" @click="goBack" class="back-button">← Back</button>
      <ProjectList
        v-if="isAuthenticated && currentView === 'projects'"
        ref="projectList"
        @select-project="handleProjectSelect"
      />
      <FileList
        v-if="isAuthenticated && currentView === 'files'"
        :projectId="selectedProject"
        @select-file="handleFileSelect"
      />
      <EstimateList
        v-if="isAuthenticated && currentView === 'estimates'"
        :fileId="selectedFile"
      />
      <AdminPanel
        v-if="isAuthenticated && currentView === 'admin'"
      />
    </div>

    <!-- Модальное окно для авторизации -->
    <div v-if="showLoginModal" class="modal">
      <h2>Login</h2>
      <input v-model="loginForm.username" placeholder="Username" />
      <input v-model="loginForm.password" placeholder="Password" type="password" />
      <button @click="login">Login</button>
      <button @click="closeLoginModal">Cancel</button>
    </div>
  </div>
</template>

<script>
import api from '@/api';
import ProjectList from '@/components/ProjectList.vue';
import FileList from '@/components/FileList.vue';
import EstimateList from '@/components/EstimateList.vue';
import AdminPanel from '@/components/AdminPanel.vue';

export default {
  components: {
    ProjectList,
    FileList,
    EstimateList,
    AdminPanel,
  },
  data() {
    return {
      isAuthenticated: false,
      currentUserRole: null,
      showLoginModal: false,
      loginForm: {
        username: '',
        password: '',
      },
      currentView: 'projects',
      selectedProject: null,
      selectedFile: null,
      navigationStack: [],
    };
  },
  methods: {
    openLoginModal() {
      this.showLoginModal = true;
    },
    closeLoginModal() {
      this.showLoginModal = false;
    },
    async login() {
      try {
        const formData = new FormData();
        formData.append('username', this.loginForm.username);
        formData.append('password', this.loginForm.password);

        const response = await api.post('/token/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        localStorage.setItem('token', response.data.access_token);
        this.isAuthenticated = true;

        const token = response.data.access_token;
        const payload = JSON.parse(atob(token.split('.')[1]));
        this.currentUserRole = payload.role;

        this.closeLoginModal();
        this.loginForm = { username: '', password: '' };

        this.currentView = 'projects';

        this.$nextTick(() => {
          if (this.$refs.projectList && this.$refs.projectList.fetchProjects) {
            this.$refs.projectList.fetchProjects();
          }
        });
      } catch (error) {
        console.error("Login failed:", error);
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.isAuthenticated = false;
      this.currentUserRole = null;
    },
    handleProjectSelect(projectId) {
      this.selectedProject = projectId;
      this.navigationStack.push('projects');
      this.currentView = 'files';
    },
    handleFileSelect(fileId) {
      this.selectedFile = fileId;
      this.navigationStack.push('files');
      this.currentView = 'estimates';
    },
    goBack() {
      if (this.navigationStack.length > 0) {
        const previousView = this.navigationStack.pop();
        this.currentView = previousView;

        if (previousView === 'projects') {
          this.selectedProject = null;
          this.selectedFile = null;
        } else if (previousView === 'files') {
          this.selectedFile = null;
        }
      } else {
        this.currentView = 'projects';
        this.selectedProject = null;
        this.selectedFile = null;
      }
    },
    goToProjects() {
      this.currentView = 'projects';
      this.selectedProject = null;
      this.selectedFile = null;
      this.navigationStack = [];
    },
    goToFiles() {
      if (this.selectedProject) {
        this.currentView = 'files';
        this.navigationStack = ['projects'];
      }
    },
    goToEstimates() {
      if (this.selectedFile) {
        this.currentView = 'estimates';
        this.navigationStack = ['projects', 'files'];
      }
    },
    goToAdmin() {
      this.navigationStack.push(this.currentView);
      this.currentView = 'admin';
    },
  },
  async created() {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        this.currentUserRole = payload.role;
        this.isAuthenticated = true;
      } catch (error) {
        localStorage.removeItem('token');
      }
    }
  },
};
</script>

<style>

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: linear-gradient(135deg, #967a7a, #ca5e5e);
  min-height: 100vh;
}

.main-layout {
  display: flex;
  min-height: 100vh;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.sidebar {
  width: 200px;
  background-color: #292961;
  color: white;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar .logo {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar ul li {
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
  margin-bottom: 5px;
  transition: background-color 0.3s;
}

.sidebar ul li:hover {
  background-color: #3a3a7a;
}

.sidebar ul li.active {
  background-color: #4a4a8a;
}

.sidebar ul ul {
  margin-left: 20px;
  margin-top: 5px;
}

.header {
  position: fixed;
  top: 0;
  right: 0;
  padding: 10px;
  /*background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);*/
  z-index: 1000;
}

.header-buttons {
  display: flex;
  gap: 10px;
}

.admin-button,
.logout-button {
  background-color: #292961;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.admin-button:hover,
.logout-button:hover {
  background-color: #3a3a7a;
}

.content {
  flex-grow: 1;
  padding: 20px;
  margin-top: 60px;
}
.back-button {
  background-color: #292961;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #3a3a7a;
}
</style>