<template>
  <div class="admin-panel">
    <h1>Admin Panel</h1>

    <!-- Переключатель для выбора таблицы -->
    <div class="table-selector">
      <label for="table-select">Выберите таблицу:</label>
      <select id="table-select" v-model="currentTable">
        <option value="all">All</option>
        <option value="users">Users</option>
        <option value="projects">Projects</option>
        <option value="files">Files</option>
        <option value="estimates">Estimates</option>
      </select>
    </div>

    <!-- Управление пользователями -->
    <div class="section" v-if="currentTable === 'users' || currentTable === 'all'">
      <h2>Users</h2>
      <button @click="openCreateUserModal" class="create-button">Create User</button>
      <ul>
        <li v-for="user in users" :key="user._id">
          {{ user.username }} ({{ user.role }})
          <button @click="editUser(user)">Edit</button>
          <button @click="deleteUser(user._id)">Delete</button>
        </li>
      </ul>
    </div>

    <!-- Управление проектами -->
    <div class="section" v-if="currentTable === 'projects' || currentTable === 'all'">
      <h2>Projects</h2>
      <button @click="openCreateProjectModal" class="create-button">Create Project</button>
      <ul>
        <li v-for="project in projects" :key="project._id">
          {{ project.name }} ({{ project.tag }})
          <button @click="editProject(project)">Edit</button>
          <button @click="deleteProject(project._id)">Delete</button>
        </li>
      </ul>
    </div>

    <!-- Управление файлами -->
    <div class="section" v-if="currentTable === 'files' || currentTable === 'all'">
      <h2>Files</h2>
      <button @click="openCreateFileModal" class="create-button">Create File</button>
      <ul>
        <li v-for="file in files" :key="file._id">
          {{ file.name }}
          <button @click="editFile(file)">Edit</button>
          <button @click="deleteFile(file._id)">Delete</button>
        </li>
      </ul>
    </div>

    <!-- Управление оценками -->
    <div class="section" v-if="currentTable === 'estimates' || currentTable === 'all'">
      <h2>Estimates</h2>
      <button @click="openCreateEstimateModal" class="create-button">Create Estimate</button>
      <ul>
        <li v-for="estimate in estimates" :key="estimate._id">
          {{ estimate.tag }}
          <button @click="editEstimate(estimate)">Edit</button>
          <button @click="deleteEstimate(estimate._id)">Delete</button>
        </li>
      </ul>
    </div>

    <!-- Модальные окна для создания/редактирования пользователя -->
    <div v-if="isUserModalOpen" class="modal">
      <h2>{{ isEditingUser ? 'Edit User' : 'Create User' }}</h2>
      <input v-model="userForm.username" placeholder="Username" />
      <input v-model="userForm.email" placeholder="Email" />
      <input v-model="userForm.password" placeholder="Password" type="password" />
      <select v-model="userForm.role">
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </select>
      <button @click="saveUser">Save</button>
      <button @click="closeUserModal">Cancel</button>
    </div>

    <!-- Модальное окно для создания/редактирования проекта -->
    <div v-if="isProjectModalOpen" class="modal">
      <h2>{{ isEditingProject ? 'Edit Project' : 'Create Project' }}</h2>
      <input v-model="projectForm.name" placeholder="Name" />
      <input v-model="projectForm.desc" placeholder="Description" />
      <input v-model="projectForm.tag" placeholder="Tag" />
      <button @click="saveProject">Save</button>
      <button @click="closeProjectModal">Cancel</button>
    </div>

    <!-- Модальное окно для создания/редактирования файла -->
    <div v-if="isFileModalOpen" class="modal">
      <h2>{{ isEditingFile ? 'Edit File' : 'Create File' }}</h2>
      <input v-model="fileForm.name" placeholder="Name" />
      <input v-model="fileForm.filePath" placeholder="File Path" />
      <select v-model="fileForm.tag">
        <option value="meta_file">meta_file</option>
        <option value="meta_photo">meta_photo</option>
      </select>
      <input v-if="fileForm.tag === 'meta_file'" v-model="fileForm.fps" placeholder="FPS" />
      <input v-if="fileForm.tag === 'meta_file'" v-model="fileForm.frameSize" placeholder="Frame Size" />
      <input v-model="fileForm.frameCount" placeholder="Frame Count" />

      <!-- Выбор проекта -->
      <label for="project-select">Select Project:</label>
      <select id="project-select" v-model="fileForm.projectID">
        <option v-for="project in projects" :key="project._id" :value="project._id">
          {{ project.name }}
        </option>
      </select>

      <button @click="saveFile">Save</button>
      <button @click="closeFileModal">Cancel</button>
    </div>

    <!-- Модальное окно для создания/редактирования оценки -->
    <div v-if="isEstimateModalOpen" class="modal">
      <h2>{{ isEditingEstimate ? 'Edit Estimate' : 'Create Estimate' }}</h2>
      <input v-model="estimateForm.tag" placeholder="Tag" />
      <input v-model="estimateForm.frame_interval" placeholder="Frame Interval (comma separated)" />
      <input v-model="estimateForm.roi" placeholder="ROI (comma separated)" />

      <!-- Выбор файла -->
      <label for="file-select">Select File:</label>
      <select id="file-select" v-model="estimateForm.file_id">
        <option v-for="file in files" :key="file._id" :value="file._id">
          {{ file.name }}
        </option>
      </select>

      <button @click="saveEstimate">Save</button>
      <button @click="closeEstimateModal">Cancel</button>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  data() {
    return {
      users: [],
      projects: [],
      files: [],
      estimates: [],

      
      currentTable: 'all',

      // Пользователи
      isUserModalOpen: false,
      isEditingUser: false,
      userForm: {
        username: '',
        email: '',
        password: '',
        role: 'user',
      },
      currentUserId: null,

      // Проекты
      isProjectModalOpen: false,
      isEditingProject: false,
      projectForm: {
        name: '',
        desc: '',
        tag: '',
      },
      currentProjectId: null,

      // Файлы
      isFileModalOpen: false,
      isEditingFile: false,
      fileForm: {
        name: '',
        filePath: '',
        tag: 'meta_file',
        fps: '',
        frameSize: '',
        frameCount: 0,
        projectID: null, 
      },
      currentFileId: null,

      // Эстимейты
      isEstimateModalOpen: false,
      isEditingEstimate: false,
      estimateForm: {
        tag: '',
        frame_interval: [],
        roi: [],
        file_id: null, 
      },
      currentEstimateId: null,
    };
  },
  async created() {
    await this.fetchUsers();
    await this.fetchProjects();
    await this.fetchFiles();
    await this.fetchEstimates();
  },
  methods: {
    // Загрузка данных
    async fetchUsers() {
      const response = await api.get('/admin/users');
      this.users = response.data;
    },
    async fetchProjects() {
      const response = await api.get('/projects/');
      this.projects = response.data;
    },
    async fetchFiles() {
      const response = await api.get('/files/');
      this.files = response.data;
    },
    async fetchEstimates() {
      const response = await api.get('/estimates/');
      this.estimates = response.data;
    },

    // Пользователи
    openCreateUserModal() {
      this.isUserModalOpen = true;
      this.isEditingUser = false;
      this.userForm = {
        username: '',
        email: '',
        password: '',
        role: 'user',
      };
    },
    editUser(user) {
      this.isUserModalOpen = true;
      this.isEditingUser = true;
      this.userForm = { ...user };
      this.currentUserId = user._id;
    },
    async saveUser() {
      const payload = {
        username: this.userForm.username,
        email: this.userForm.email,
        password: this.userForm.password,
        role: this.userForm.role,
      };

      if (this.isEditingUser) {
        await api.put(`/admin/users/${this.currentUserId}`, payload);
      } else {
        await api.post('/admin/users/', payload);
      }
      this.closeUserModal();
      await this.fetchUsers();
    },
    async deleteUser(userId) {
      await api.delete(`/admin/users/${userId}`);
      await this.fetchUsers();
    },
    closeUserModal() {
      this.isUserModalOpen = false;
    },

    // Проекты
    openCreateProjectModal() {
      this.isProjectModalOpen = true;
      this.isEditingProject = false;
      this.projectForm = {
        name: '',
        desc: '',
        tag: '',
      };
    },
    editProject(project) {
      this.isProjectModalOpen = true;
      this.isEditingProject = true;
      this.projectForm = { ...project };
      this.currentProjectId = project._id;
    },
    async saveProject() {
      const payload = {
        name: this.projectForm.name,
        desc: this.projectForm.desc,
        something: [], 
        tag: this.projectForm.tag, 
      };

      try {
        if (this.isEditingProject) {
          await api.put(`/projects/${this.currentProjectId}`, payload);
        } else {
          await api.post('/projects/', payload);
        }
        this.closeProjectModal();
        await this.fetchProjects();
      } catch (error) {
        console.error("Error saving project:", error.response?.data || error.message);
      }
    },
    async deleteProject(projectId) {
      await api.delete(`/projects/${projectId}`);
      await this.fetchProjects();
    },
    closeProjectModal() {
      this.isProjectModalOpen = false;
    },

    // Файлы
    openCreateFileModal() {
      this.isFileModalOpen = true;
      this.isEditingFile = false;
      this.fileForm = {
        name: '',
        filePath: '',
        tag: 'meta_file',
        fps: '',
        frameSize: '',
        frameCount: 0,
        projectID: null, 
      };
    },
    editFile(file) {
  this.isFileModalOpen = true;
  this.isEditingFile = true;
  this.fileForm = {
    ...file,
    fps: file.fps ? file.fps.join(',') : '',
    frameSize: file.frameSize ? file.frameSize.join(',') : '',
    projectID: file.projectID[0]?.toString() // Преобразуем в строку
  };
  this.currentFileId = file._id;
},

async saveFile() {
  if (!this.fileForm.projectID) {
    console.error("Project ID is not set.");
    return;
  }

  const payload = {
    name: this.fileForm.name,
    filePath: this.fileForm.filePath,
    tag: this.fileForm.tag,
    projectID: [this.fileForm.projectID], // Массив строк
    frameCount: this.fileForm.frameCount,
    fps: this.fileForm.tag === 'meta_file'
      ? (this.fileForm.fps ? this.fileForm.fps.split(',').map(Number) : [])
      : [],
    frameSize: this.fileForm.tag === 'meta_file'
      ? (this.fileForm.frameSize ? this.fileForm.frameSize.split(',').map(Number) : [])
      : []
  };

  try {
    if (this.isEditingFile) {
      await api.put(`/files/${this.currentFileId}`, payload);
    } else {
      await api.post('/files/', payload);
    }
    this.closeFileModal();
    await this.fetchFiles();
  } catch (error) {
    console.error("Error saving file:", error.response?.data || error.message);
  }
},
    async deleteFile(fileId) {
      await api.delete(`/files/${fileId}`);
      await this.fetchFiles();
    },
    closeFileModal() {
      this.isFileModalOpen = false;
    },

    // Оценки
    openCreateEstimateModal() {
      this.isEstimateModalOpen = true;
      this.isEditingEstimate = false;
      this.estimateForm = {
        tag: '',
        frame_interval: [],
        roi: [],
        file_id: null, 
      };
    },
    editEstimate(estimate) {
  this.isEstimateModalOpen = true;
  this.isEditingEstimate = true;
  this.estimateForm = {
    ...estimate,
    frame_interval: estimate.frame_interval.join(','),
    roi: estimate.roi.join(','),
    file_id: estimate.file_id[0]?.toString() // Преобразуем в строку
  };
  this.currentEstimateId = estimate._id;
},

async saveEstimate() {
  if (!this.estimateForm.file_id) {
    console.error("File ID is not set.");
    return;
  }

  const payload = {
    tag: this.estimateForm.tag,
    frame_interval: this.estimateForm.frame_interval.split(',').map(Number),
    roi: this.estimateForm.roi.split(',').map(Number),
    file_id: [this.estimateForm.file_id], // Массив строк
    settings: {}
  };

  try {
    if (this.isEditingEstimate) {
      await api.put(`/estimates/${this.currentEstimateId}`, payload);
    } else {
      await api.post('/estimates/', payload);
    }
    this.closeEstimateModal();
    await this.fetchEstimates();
  } catch (error) {
    console.error("Error saving estimate:", error.response?.data || error.message);
  }
},
    async deleteEstimate(estimateId) {
      await api.delete(`/estimates/${estimateId}`);
      await this.fetchEstimates();
    },
    closeEstimateModal() {
      this.isEstimateModalOpen = false;
    },
  },
};
</script>

<style scoped>
.admin-panel {
  padding: 20px;
}

.table-selector {
  margin-bottom: 20px;
}

.table-selector label {
  margin-right: 10px;
}

.section {
  margin-bottom: 20px;
}

.create-button {
  background-color: #292961;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 10px;
}

.create-button:hover {
  background-color: #3a3a7a;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

button {
  background-color: #292961;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 5px;
}

button:hover {
  background-color: #3a3a7a;
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  width: 300px;
}

.modal h2 {
  margin-top: 0;
}

.modal input,
.modal select {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal button {
  margin-right: 10px;
}
</style>