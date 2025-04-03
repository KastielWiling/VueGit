<template>
  <div class="admin-panel">
    <h1>Admin Panel</h1>
    
    <!-- Вкладки для навигации -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.value"
        :class="{ active: activeTab === tab.value }"
        @click="activeTab = tab.value"
      >
        {{ tab.label }}
        <span class="badge" v-if="tab.count > 0">{{ tab.count }}</span>
      </button>
    </div>

    <!-- Индикатор загрузки -->
    <div class="loading-overlay" v-if="isLoading">
      <div class="loader"></div>
    </div>

    <!-- Контент вкладок -->
    <div class="tab-content">
      <!-- Пользователи -->
      <div v-show="activeTab === 'users'" class="section">
        <div class="section-header">
          <h2>Users Management</h2>
          <div class="controls">
            <div class="search-box">
              <input 
                v-model="searchQuery" 
                placeholder="Search users..." 
                @keyup.enter="fetchUsers"
              >
              <i class="fas fa-search"></i>
            </div>
            <button @click="openCreateUserModal" class="create-button">
              <i class="fas fa-plus"></i> Add User
            </button>
          </div>
        </div>
        
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th @click="sortTable('username')">
                  Username
                  <i class="fas" :class="sortIcon('username')"></i>
                </th>
                <th @click="sortTable('email')">
                  Email
                  <i class="fas" :class="sortIcon('email')"></i>
                </th>
                <th @click="sortTable('role')">
                  Role
                  <i class="fas" :class="sortIcon('role')"></i>
                </th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in paginatedItems" :key="user._id">
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span class="role-badge" :class="user.role">
                    {{ user.role }}
                  </span>
                </td>
                <td class="actions">
                  <button @click="editUser(user)" class="edit" title="Edit">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button @click="confirmDelete(user._id, 'user')" class="delete" title="Delete">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredItems.length === 0">
                <td colspan="4" class="no-results">No users found</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Пагинация -->
        <div class="pagination-controls">
          <div class="items-per-page">
            <span>Items per page:</span>
            <select v-model="itemsPerPage" @change="currentPage = 1">
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="20">20</option>
              <option value="50">50</option>
            </select>
          </div>
          <div class="pagination-buttons">
            <button @click="prevPage" :disabled="currentPage === 1">
              <i class="fas fa-chevron-left"></i>
            </button>
            <span>Page {{ currentPage }} of {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Projects -->
      <div v-show="activeTab === 'projects'" class="section">
  <div class="section-header">
    <h2>Projects Management</h2>
    <div class="controls">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          placeholder="Search projects..." 
          @keyup.enter="fetchProjects"
        >
        <i class="fas fa-search"></i>
      </div>
      <button @click="openCreateProjectModal" class="create-button">
        <i class="fas fa-plus"></i> Add Project
      </button>
    </div>
  </div>
  
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th @click="sortTable('name')">
            Name
            <i class="fas" :class="sortIcon('name')"></i>
          </th>
          <th>Description</th>
          <th @click="sortTable('tag')">
            Tag
            <i class="fas" :class="sortIcon('tag')"></i>
          </th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="project in paginatedItems" :key="project._id">
          <td>{{ project.name }}</td>
          <td>{{ project.desc }}</td>
          <td>{{ project.tag }}</td>
          <td class="actions">
            <button @click="editProject(project)" class="edit" title="Edit">
              <i class="fas fa-edit"></i>
            </button>
            <button @click="confirmDelete(project._id, 'project')" class="delete" title="Delete">
              <i class="fas fa-trash"></i>
            </button>
          </td>
        </tr>
        <tr v-if="filteredItems.length === 0">
          <td colspan="4" class="no-results">No projects found</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Пагинация -->
  <div class="pagination-controls">
    <div class="items-per-page">
      <span>Items per page:</span>
      <select v-model="itemsPerPage" @change="currentPage = 1">
        <option value="5">5</option>
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="50">50</option>
      </select>
    </div>
    <div class="pagination-buttons">
      <button @click="prevPage" :disabled="currentPage === 1">
        <i class="fas fa-chevron-left"></i>
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
</div>

      <!-- Files -->
      <div v-show="activeTab === 'files'" class="section">
  <div class="section-header">
    <h2>Files Management</h2>
    <div class="controls">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          placeholder="Search files..." 
          @keyup.enter="fetchFiles"
        >
        <i class="fas fa-search"></i>
      </div>
      <button @click="openCreateFileModal" class="create-button">
        <i class="fas fa-plus"></i> Add File
      </button>
    </div>
  </div>
  
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th @click="sortTable('name')">
            Name
            <i class="fas" :class="sortIcon('name')"></i>
          </th>
          <th>File Path</th>
          <th @click="sortTable('tag')">
            Type
            <i class="fas" :class="sortIcon('tag')"></i>
          </th>
          <th>Frame Count</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="file in paginatedItems" :key="file._id">
          <td>{{ file.name }}</td>
          <td>{{ file.filePath }}</td>
          <td>{{ file.tag }}</td>
          <td>{{ file.frameCount }}</td>
          <td class="actions">
            <button @click="editFile(file)" class="edit" title="Edit">
              <i class="fas fa-edit"></i>
            </button>
            <button @click="confirmDelete(file._id, 'file')" class="delete" title="Delete">
              <i class="fas fa-trash"></i>
            </button>
          </td>
        </tr>
        <tr v-if="filteredItems.length === 0">
          <td colspan="5" class="no-results">No files found</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="pagination-controls">
    <div class="items-per-page">
      <span>Items per page:</span>
      <select v-model="itemsPerPage" @change="currentPage = 1">
        <option value="5">5</option>
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="50">50</option>
      </select>
    </div>
    <div class="pagination-buttons">
      <button @click="prevPage" :disabled="currentPage === 1">
        <i class="fas fa-chevron-left"></i>
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
</div>

      <!-- Estimates -->
      <div v-show="activeTab === 'estimates'" class="section">
  <div class="section-header">
    <h2>Estimates Management</h2>
    <div class="controls">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          placeholder="Search estimates..." 
          @keyup.enter="fetchEstimates"
        >
        <i class="fas fa-search"></i>
      </div>
      <button @click="openCreateEstimateModal" class="create-button">
        <i class="fas fa-plus"></i> Add Estimate
      </button>
    </div>
  </div>
  
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th @click="sortTable('tag')">
            Tag
            <i class="fas" :class="sortIcon('tag')"></i>
          </th>
          <th>Frame Interval</th>
          <th>ROI</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="estimate in paginatedItems" :key="estimate._id">
          <td>{{ estimate.tag }}</td>
          <td>{{ estimate.frame_interval?.join(', ') || 'N/A' }}</td>
          <td>{{ estimate.roi?.join(', ') || 'N/A' }}</td>
          <td class="actions">
            <button @click="editEstimate(estimate)" class="edit" title="Edit">
              <i class="fas fa-edit"></i>
            </button>
            <button @click="confirmDelete(estimate._id, 'estimate')" class="delete" title="Delete">
              <i class="fas fa-trash"></i>
            </button>
          </td>
        </tr>
        <tr v-if="filteredItems.length === 0">
          <td colspan="4" class="no-results">No estimates found</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="pagination-controls">
    <div class="items-per-page">
      <span>Items per page:</span>
      <select v-model="itemsPerPage" @change="currentPage = 1">
        <option value="5">5</option>
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="50">50</option>
      </select>
    </div>
    <div class="pagination-buttons">
      <button @click="prevPage" :disabled="currentPage === 1">
        <i class="fas fa-chevron-left"></i>
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
</div>
<!-- User Activity -->
<div v-show="activeTab === 'activity'" class="section">
  <div class="section-header">
    <h2>User Activity Log</h2>
    <div class="controls">
      <div class="filters">
        <select v-model="activityFilters.user" @change="fetchActivityLogs">
          <option value="">All Users</option>
          <option v-for="user in users" :value="user._id" :key="user._id"> {{ user.username }} </option>
        </select>
        
        <select v-model="activityFilters.action" @change="fetchActivityLogs">
          <option value="">All Actions</option>
          <option value="create">Create</option>
          <option value="update">Update</option>
          <option value="delete">Delete</option>
          <option value="login">Login</option>
        </select>
        
        <input type="date" v-model="activityFilters.dateFrom" @change="fetchActivityLogs">
        <input type="date" v-model="activityFilters.dateTo" @change="fetchActivityLogs">
      </div>
    </div>
  </div>
  
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>User</th>
          <th>Action</th>
          <th>Entity</th>
          <th>Details</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in activityLogs" :key="log._id">
          <td>{{ log.user_name || 'Unknown' }}</td>
          <td>{{ log.action }}</td>
          <td>{{ log.entity_type }}: {{ log.entity_name || log.entity_id }}</td>
          <td>{{ log.details }}</td>
          <td>{{ formatDate(log.timestamp) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
<!-- В template AdminPanel.vue, в разделе stats -->
<div v-show="activeTab === 'stats'" class="section">
  <h2>Projects Statistics</h2>
  <ProjectsHistogram 
    :projects="projects" 
    :files="files"
    @project-selected="onProjectSelected"
  />
</div>
    </div>

    <!-- Модальные окна -->
    <!-- User Modal -->
    <div v-if="isUserModalOpen" class="modal-overlay" @click.self="closeUserModal">
      <div class="modal-content">
        <h2>{{ isEditingUser ? 'Edit User' : 'Create User' }}</h2>
        <div class="form-group">
          <label>Username</label>
          <input v-model="userForm.username" placeholder="Enter username">
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="userForm.email" placeholder="Enter email" type="email">
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="userForm.password" placeholder="Enter password" type="password">
        </div>
        <div class="form-group">
          <label>Role</label>
          <select v-model="userForm.role">
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div class="modal-actions">
          <button @click="saveUser" class="save-button">
            <i class="fas fa-save"></i> Save
          </button>
          <button @click="closeUserModal" class="cancel-button">
            <i class="fas fa-times"></i> Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Project Modal -->
    <div v-if="isProjectModalOpen" class="modal-overlay" @click.self="closeProjectModal">
      <div class="modal-content">
        <h2>{{ isEditingProject ? 'Edit Project' : 'Create Project' }}</h2>
        <div class="form-group">
          <label>Name</label>
          <input v-model="projectForm.name" placeholder="Enter project name">
        </div>
        <div class="form-group">
          <label>Description</label>
          <textarea v-model="projectForm.desc" placeholder="Enter description"></textarea>
        </div>
        <div class="form-group">
          <label>Tag</label>
          <input v-model="projectForm.tag" placeholder="Enter tag">
        </div>
        <div class="modal-actions">
          <button @click="saveProject" class="save-button">
            <i class="fas fa-save"></i> Save
          </button>
          <button @click="closeProjectModal" class="cancel-button">
            <i class="fas fa-times"></i> Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- File Modal -->
    <div v-if="isFileModalOpen" class="modal-overlay" @click.self="closeFileModal">
      <div class="modal-content">
        <h2>{{ isEditingFile ? 'Edit File' : 'Create File' }}</h2>
        <div class="form-group">
          <label>Name</label>
          <input v-model="fileForm.name" placeholder="Enter file name">
        </div>
        <div class="form-group">
          <label>File Path</label>
          <input v-model="fileForm.filePath" placeholder="Enter file path">
        </div>
        <div class="form-group">
          <label>Type</label>
          <select v-model="fileForm.tag">
            <option value="meta_file">Meta File</option>
            <option value="meta_photo">Meta Photo</option>
          </select>
        </div>
        <div v-if="fileForm.tag === 'meta_file'" class="form-group">
          <label>FPS</label>
          <input v-model="fileForm.fps" placeholder="Enter FPS (comma separated)">
        </div>
        <div v-if="fileForm.tag === 'meta_file'" class="form-group">
          <label>Frame Size</label>
          <input v-model="fileForm.frameSize" placeholder="Enter frame size (comma separated)">
        </div>
        <div class="form-group">
          <label>Frame Count</label>
          <input v-model="fileForm.frameCount" type="number" placeholder="Enter frame count">
        </div>
        <div class="form-group">
          <label>Project</label>
          <select v-model="fileForm.projectID">
            <option v-for="project in projects" :key="project._id" :value="project._id">
              {{ project.name }}
            </option>
          </select>
        </div>
        <div class="modal-actions">
          <button @click="saveFile" class="save-button">
            <i class="fas fa-save"></i> Save
          </button>
          <button @click="closeFileModal" class="cancel-button">
            <i class="fas fa-times"></i> Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Estimate Modal -->
    <div v-if="isEstimateModalOpen" class="modal-overlay" @click.self="closeEstimateModal">
      <div class="modal-content">
        <h2>{{ isEditingEstimate ? 'Edit Estimate' : 'Create Estimate' }}</h2>
        <div class="form-group">
          <label>Tag</label>
          <input v-model="estimateForm.tag" placeholder="Enter estimate tag">
        </div>
        <div class="form-group">
          <label>Frame Interval</label>
          <input v-model="estimateForm.frame_interval" placeholder="Enter frame interval (comma separated)">
        </div>
        <div class="form-group">
          <label>ROI</label>
          <input v-model="estimateForm.roi" placeholder="Enter ROI (comma separated)">
        </div>
        <div class="form-group">
          <label>File</label>
          <select v-model="estimateForm.file_id">
            <option v-for="file in files" :key="file._id" :value="file._id">
              {{ file.name }}
            </option>
          </select>
        </div>
        <div class="modal-actions">
          <button @click="saveEstimate" class="save-button">
            <i class="fas fa-save"></i> Save
          </button>
          <button @click="closeEstimateModal" class="cancel-button">
            <i class="fas fa-times"></i> Cancel
          </button>
        </div>
      </div>
    </div>

    <div v-if="selectedProjectModal" class="modal-overlay" @click.self="closeProjectModalHist">
  <div class="modal-content">
    <h2>Project Details: {{ selectedProjectModal.name }}</h2>
    
    <div class="project-stats">
      <div class="stat-item">
        <span class="stat-label">Files:</span>
        <span class="stat-value">{{ selectedProjectStats.fileCount }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Created:</span>
        <span class="stat-value">{{ formatDate(selectedProjectModal.createdAt) }}</span>
      </div>
    </div>
    
    <div class="project-actions">
      <button @click="openEditProjectModal(selectedProjectModal)" class="action-button">
        <i class="fas fa-edit"></i> Edit Project
      </button>
      <button @click="confirmDelete(selectedProjectModal._id, 'project')" class="action-button delete">
        <i class="fas fa-trash"></i> Delete Project
      </button>
    </div>
    
    <button @click="closeProjectModalHist" class="cancel-button">
      <i class="fas fa-times"></i> Close
    </button>
  </div>
</div>

    <!-- Диалог подтверждения удаления -->
    <div v-if="showDeleteConfirm" class="confirm-dialog-overlay">
      <div class="confirm-dialog">
        <h3>Confirm Delete</h3>
        <p>Are you sure you want to delete this {{ itemToDeleteType }}? This action cannot be undone.</p>
        <div class="dialog-actions">
          <button @click="executeDelete" class="confirm-button">Delete</button>
          <button @click="cancelDelete" class="cancel-button">Cancel</button>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import api from '@/api';
import { useToast } from 'vue-toastification';
import ProjectsHistogram from '@/components/ProjectsHistogram.vue';

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },
  components: {
    ProjectsHistogram
  },
  data() {
    return {
      // Навигация
      activeTab: 'users',
      tabs: [
        { label: 'Users', value: 'users', count: 0 },
        { label: 'Projects', value: 'projects', count: 0 },
        { label: 'Files', value: 'files', count: 0 },
        { label: 'Estimates', value: 'estimates', count: 0 },
        { label: 'Activity Log', value: 'activity', count: 0 },
        { label: 'Statistics', value: 'stats', count: 0 }
      ],
      // Под гистограмму
      selectedProjectModal: null,
      selectedProjectStats: {
        fileCount: 0
      },
      // История действий
      activityLogs: [],
      activityFilters: {
        user: null,
        action: null,
        dateFrom: null,
        dateTo: null
      },
      // Данные
      users: [],
      projects: [],
      files: [],
      estimates: [],
      
      // Поиск и сортировка
      searchQuery: '',
      sortConfig: {
        key: 'username',
        direction: 'asc'
      },
      
      // Пагинация
      currentPage: 1,
      itemsPerPage: 10,
      
      // Состояние загрузки
      isLoading: false,
      
      // Модальные окна
      isUserModalOpen: false,
      isEditingUser: false,
      userForm: {
        username: '',
        email: '',
        password: '',
        role: 'user'
      },
      currentUserId: null,
      
      isProjectModalOpen: false,
      isEditingProject: false,
      projectForm: {
        name: '',
        desc: '',
        tag: 'default_tag'
      },
      currentProjectId: null,
      
      isFileModalOpen: false,
      isEditingFile: false,
      fileForm: {
        name: '',
        filePath: '',
        tag: 'meta_file',
        fps: '',
        frameSize: '',
        frameCount: 0,
        projectID: null
      },
      currentFileId: null,
      
      isEstimateModalOpen: false,
      isEditingEstimate: false,
      estimateForm: {
        tag: '',
        frame_interval: '',
        roi: '',
        file_id: null
      },
      currentEstimateId: null,
      
      // Подтверждение удаления
      showDeleteConfirm: false,
      itemToDeleteId: null,
      itemToDeleteType: null
    };
  },
  computed: {
    // Текущие элементы для активной вкладки
    currentItems() {
      switch (this.activeTab) {
        case 'users': return this.users;
        case 'projects': return this.projects;
        case 'files': return this.files;
        case 'estimates': return this.estimates;
        default: return [];
      }
    },
    
    // Отфильтрованные элементы
    filteredItems() {
      let filtered = this.currentItems;
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(item => {
          // Для пользователей
          if (this.activeTab === 'users') {
            return (
              item.username.toLowerCase().includes(query) ||
              item.email.toLowerCase().includes(query) ||
              item.role.toLowerCase().includes(query))
          }
          // Для проектов
          else if (this.activeTab === 'projects') {
            return (
              item.name.toLowerCase().includes(query) ||
              item.desc.toLowerCase().includes(query) ||
              item.tag.toLowerCase().includes(query))
          }
          // Для файлов
          else if (this.activeTab === 'files') {
            return (
              item.name.toLowerCase().includes(query) ||
              item.filePath.toLowerCase().includes(query) ||
              item.tag.toLowerCase().includes(query))
          }
          // Для оценок
          else if (this.activeTab === 'estimates') {
            const frameInterval = item.frame_interval ? item.frame_interval.join(',') : '';
            const roi = item.roi ? item.roi.join(',') : '';
            return (
              item.tag?.toLowerCase().includes(query) ||
              frameInterval.toLowerCase().includes(query) ||
              roi.toLowerCase().includes(query))
          }
          return true;
        });
      }
      
      // Сортировка
      return filtered.sort((a, b) => {
        if (a[this.sortConfig.key] < b[this.sortConfig.key]) {
          return this.sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (a[this.sortConfig.key] > b[this.sortConfig.key]) {
          return this.sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    },
    
    // Элементы для текущей страницы
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredItems.slice(start, end);
    },
    
    // Общее количество страниц
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    
    // Иконка сортировки
    sortIcon() {
      return (key) => ({
        'fa-sort': this.sortConfig.key !== key,
        'fa-sort-up': this.sortConfig.key === key && this.sortConfig.direction === 'asc',
        'fa-sort-down': this.sortConfig.key === key && this.sortConfig.direction === 'desc'
      });
    }
  },
  watch: {
    activeTab() {
      this.searchQuery = '';
      this.currentPage = 1;
      this.loadData();
    }
  },
  async created() {
    await this.loadData();
  },
  methods: {
    // Загрузка данных
    async loadData() {
      this.isLoading = true;
      try {
        switch (this.activeTab) {
          case 'users':
            await this.fetchUsers();
            break;
          case 'projects':
            await this.fetchProjects();
            break;
          case 'files':
            await this.fetchFiles();
            break;
          case 'estimates':
            await this.fetchEstimates();
            break;
          case 'activity':
            await this.fetchActivityLogs();
            break;
          case 'stats':
            await this.fetchProjects();
            await this.fetchFiles();
            break;
        }
      } catch (error) {
        this.toast.error(`Error loading ${this.activeTab}: ${error.message}`);
      } finally {
        this.isLoading = false;
      }
    },
    // Под гистограмму
    onProjectSelected(project) {
      this.selectedProjectModal = project;
      this.calculateProjectStats(project);
    },
  
    calculateProjectStats(project) {
      this.selectedProjectStats.fileCount = this.files.filter(file => 
        file.projectID && file.projectID.includes(project._id)
      ).length;
    },
    
    closeProjectModalHist() {
      this.selectedProjectModal = null;
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    },
    
    openEditProjectModal(project) {
      this.closeProjectModal();
      this.selectedProjectModal = null; // Сначала закрываем модалку деталей
    this.$nextTick(() => {
      this.editProject(project); // Затем открываем модалку редактирования
    });
    },

    // Получение истории действий
    async fetchActivityLogs() {
      try {
        const params = {
          user: this.activityFilters.user,
          action: this.activityFilters.action,
          dateFrom: this.activityFilters.dateFrom,
          dateTo: this.activityFilters.dateTo
        };
        
        const response = await api.get('/admin/activity', { params });
        this.activityLogs = response.data;
        this.tabs.find(t => t.value === 'activity').count = this.activityLogs.length;
      } catch (error) {
        this.toast.error('Failed to load activity logs');
      }
    },
    getUserName(userId) {
      const user = this.users.find(u => u._id === userId);
      return user ? user.username : 'Unknown';
    },
    async logAction(action, entityType = null, entityId = null, details = '') {
  try {
    await api.post('/admin/activity', {
      action,
      entity_type: entityType,
      entity_id: entityId,
      details
    });
  } catch (error) {
    console.error('Error logging action:', error);
  }
},
    // Получение пользователей
    async fetchUsers() {
      try {
        const response = await api.get('/admin/users/');
        this.users = response.data;
        this.tabs.find(t => t.value === 'users').count = this.users.length;
      } catch (error) {
        this.toast.error('Failed to fetch users');
      }
    },
    
    // Получение проектов
    async fetchProjects() {
      try {
        const response = await api.get('/projects/');
        this.projects = response.data;
        this.tabs.find(t => t.value === 'projects').count = this.projects.length;
      } catch (error) {
        this.toast.error('Failed to fetch projects');
      }
    },
    
    // Получение файлов
    async fetchFiles() {
      try {
        const response = await api.get('/files/');
        this.files = response.data;
        this.tabs.find(t => t.value === 'files').count = this.files.length;
      } catch (error) {
        this.toast.error('Failed to fetch files');
      }
    },
    
    // Получение оценок
    async fetchEstimates() {
      try {
        const response = await api.get('/estimates/');
        this.estimates = response.data.map(est => ({
          ...est,
          frame_interval: est.frame_interval || [],
          roi: est.roi || []
        }));
        this.tabs.find(t => t.value === 'estimates').count = this.estimates.length;
      } catch (error) {
        this.toast.error('Failed to fetch estimates');
      }
    },
    
    // Сортировка таблицы
    sortTable(key) {
      if (this.sortConfig.key === key) {
        this.sortConfig.direction = this.sortConfig.direction === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortConfig.key = key;
        this.sortConfig.direction = 'asc';
      }
    },
    
    // Навигация по страницам
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    
    // Подтверждение удаления
    confirmDelete(id, type) {
      this.itemToDeleteId = id;
      this.itemToDeleteType = type;
      this.showDeleteConfirm = true;
    },
    
    // Выполнение удаления
    async executeDelete() {
      try {
        let endpoint = '';
        switch (this.itemToDeleteType) {
          case 'user':
            endpoint = `/admin/users/${this.itemToDeleteId}`;
            break;
          case 'project':
            endpoint = `/projects/${this.itemToDeleteId}`;
            break;
          case 'file':
            endpoint = `/files/${this.itemToDeleteId}`;
            break;
          case 'estimate':
            endpoint = `/estimates/${this.itemToDeleteId}`;
            break;
        }
        
        await api.delete(endpoint);
        
        // Логируем действие
        await this.logAction(
          'delete', 
          this.itemToDeleteType, 
          this.itemToDeleteId,
          `Deleted ${this.itemToDeleteType} with ID ${this.itemToDeleteId}`
        );
        
        this.toast.success(`${this.itemToDeleteType} deleted successfully`);
        await this.loadData();
      } catch (error) {
        this.toast.error(`Failed to delete ${this.itemToDeleteType}`);
      } finally {
        this.cancelDelete();
      }
    },
    
    // Отмена удаления
    cancelDelete() {
      this.itemToDeleteId = null;
      this.itemToDeleteType = null;
      this.showDeleteConfirm = false;
    },
    
    // Открытие модальных окон создания
    openCreateUserModal() {
      this.isUserModalOpen = true;
      this.isEditingUser = false;
      this.userForm = {
        username: '',
        email: '',
        password: '',
        role: 'user'
      };
    },
    
    openCreateProjectModal() {
      this.isProjectModalOpen = true;
      this.isEditingProject = false;
      this.projectForm = {
        name: '',
        desc: '',
        tag: 'default_tag'
      };
    },
    
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
        projectID: this.projects[0]?._id || null
      };
    },
    
    openCreateEstimateModal() {
      this.isEstimateModalOpen = true;
      this.isEditingEstimate = false;
      this.estimateForm = {
        tag: '',
        frame_interval: '',
        roi: '',
        file_id: this.files[0]?._id || null
      };
    },
    
    // Редактирование элементов
    editUser(user) {
      this.isUserModalOpen = true;
      this.isEditingUser = true;
      this.userForm = { ...user };
      this.currentUserId = user._id;
    },
    
    editProject(project) {
      this.isProjectModalOpen = true;
      this.isEditingProject = true;
      this.projectForm = { ...project };
      this.currentProjectId = project._id;
    },
    
    editFile(file) {
      this.isFileModalOpen = true;
      this.isEditingFile = true;
      this.fileForm = {
        ...file,
        fps: file.fps ? file.fps.join(',') : '',
        frameSize: file.frameSize ? file.frameSize.join(',') : '',
        projectID: file.projectID[0]?.toString()
      };
      this.currentFileId = file._id;
    },
    
    editEstimate(estimate) {
      this.isEstimateModalOpen = true;
      this.isEditingEstimate = true;
      this.estimateForm = {
        ...estimate,
        frame_interval: estimate.frame_interval ? estimate.frame_interval.join(',') : '',
        roi: estimate.roi ? estimate.roi.join(',') : '',
        file_id: estimate.file_id?.[0]?.toString()
      };
      this.currentEstimateId = estimate._id;
    },
    
    // Сохранение элементов
    async saveUser() {
      try {
        const payload = { ...this.userForm };
        
        if (this.isEditingUser) {
          await api.put(`/admin/users/${this.currentUserId}`, payload);
          
          // Логируем действие
          await this.logAction(
            'update', 
            'user', 
            this.currentUserId,
            `Updated user ${this.userForm.username}`
          );
          
          this.toast.success('User updated successfully');
        } else {
          const response = await api.post('/admin/users/', payload);
          
          // Логируем действие
          await this.logAction(
            'create', 
            'user', 
            response.data._id,
            `Created new user ${this.userForm.username}`
          );
          
          this.toast.success('User created successfully');
        }
        
        this.closeUserModal();
        await this.fetchUsers();
      } catch (error) {
        this.toast.error(error.response?.data?.message || 'Failed to save user');
      }
    },
    
    async saveProject() {
      try {
        const payload = { ...this.projectForm };
        
        if (this.isEditingProject) {
          await api.put(`/projects/${this.currentProjectId}`, payload);
          
          // Логируем действие
          await this.logAction(
            'update', 
            'project', 
            this.currentProjectId,
            `Updated project ${this.projectForm.name}`
          );
          
          this.toast.success('Project updated successfully');
        } else {
          const response = await api.post('/projects/', payload);
          
          // Логируем действие
          await this.logAction(
            'create', 
            'project', 
            response.data._id,
            `Created new project ${this.projectForm.name}`
          );
          
          this.toast.success('Project created successfully');
        }
        
        this.closeProjectModal();
        await this.fetchProjects();
      } catch (error) {
        this.toast.error(error.response?.data?.message || 'Failed to save project');
      }
    },
    
    async saveFile() {
      try {
        const payload = {
          name: this.fileForm.name,
          filePath: this.fileForm.filePath,
          tag: this.fileForm.tag,
          projectID: [this.fileForm.projectID],
          frameCount: this.fileForm.frameCount,
          fps: this.fileForm.tag === 'meta_file' 
            ? (this.fileForm.fps ? this.fileForm.fps.split(',').map(Number) : [])
            : [],
          frameSize: this.fileForm.tag === 'meta_file'
            ? (this.fileForm.frameSize ? this.fileForm.frameSize.split(',').map(Number) : [])
            : []
        };
        
        if (this.isEditingFile) {
          await api.put(`/files/${this.currentFileId}`, payload);
          
          // Логируем действие
          await this.logAction(
            'update', 
            'file', 
            this.currentFileId,
            `Updated file ${this.fileForm.name}`
          );
          
          this.toast.success('File updated successfully');
        } else {
          const response = await api.post('/files/', payload);
          
          // Логируем действие
          await this.logAction(
            'create', 
            'file', 
            response.data._id,
            `Created new file ${this.fileForm.name}`
          );
          
          this.toast.success('File created successfully');
        }
        
        this.closeFileModal();
        await this.fetchFiles();
      } catch (error) {
        this.toast.error(error.response?.data?.message || 'Failed to save file');
      }
    },
    
    async saveEstimate() {
      try {
        const payload = {
          tag: this.estimateForm.tag,
          frame_interval: this.estimateForm.frame_interval.split(',').map(Number),
          roi: this.estimateForm.roi.split(',').map(Number),
          file_id: [this.estimateForm.file_id],
          settings: {}
        };
        
        if (this.isEditingEstimate) {
          await api.put(`/estimates/${this.currentEstimateId}`, payload);
          
          // Логируем действие
          await this.logAction(
            'update', 
            'estimate', 
            this.currentEstimateId,
            `Updated estimate ${this.estimateForm.tag}`
          );
          
          this.toast.success('Estimate updated successfully');
        } else {
          const response = await api.post('/estimates/', payload);
          
          // Логируем действие
          await this.logAction(
            'create', 
            'estimate', 
            response.data._id,
            `Created new estimate ${this.estimateForm.tag}`
          );
          
          this.toast.success('Estimate created successfully');
        }
        
        this.closeEstimateModal();
        await this.fetchEstimates();
      } catch (error) {
        this.toast.error(error.response?.data?.message || 'Failed to save estimate');
      }
    },
    
    // Закрытие модальных окон
    closeUserModal() {
      this.isUserModalOpen = false;
    },
    
    closeProjectModal() {
      this.isProjectModalOpen = false;
    },

    closeFileModal() {
      this.isFileModalOpen = false;
    },
    
    closeEstimateModal() {
      this.isEstimateModalOpen = false;
    }
  }
};
</script>

<style scoped>
.filters {
  display: flex;
  gap: 10px;
  align-items: center;
}

.filters select, .filters input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.admin-panel {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

h1 {
  color: #292961;
  margin-bottom: 20px;
}

/* Стили для вкладок */
.tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
  gap: 5px;
}

.tabs button {
  padding: 12px 20px;
  background: none;
  border: none;
  cursor: pointer;
  position: relative;
  font-weight: 500;
  color: #666;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
}

.tabs button:hover {
  color: #292961;
}

.tabs button.active {
  color: #292961;
  border-bottom-color: #292961;
}

.tabs button .badge {
  background: #292961;
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 0.8em;
  margin-left: 5px;
}

/* Секции */
.section {
  margin-bottom: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.section-header h2 {
  margin: 0;
  color: #444;
}

.controls {
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-box {
  position: relative;
}

.search-box input {
  padding: 8px 15px 8px 35px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 250px;
}

.search-box i {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.create-button {
  background: #292961;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  white-space: nowrap;
}

.create-button:hover {
  background: #3a3a7a;
  transform: translateY(-2px);
}

/* Таблица */
.table-container {
  overflow-x: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background: #f8f8f8;
  font-weight: 500;
  cursor: pointer;
  user-select: none;
}

th:hover {
  background: #f0f0f0;
}

th i {
  margin-left: 5px;
}

.role-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85em;
  text-transform: capitalize;
}

.role-badge.admin {
  background: #ffebee;
  color: #c62828;
}

.role-badge.user {
  background: #e8f5e9;
  color: #2e7d32;
}

.actions {
  display: flex;
  gap: 8px;
}

.actions button {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.actions button.edit {
  background: #e3f2fd;
  color: #1565c0;
}

.actions button.delete {
  background: #ffebee;
  color: #c62828;
}

.actions button:hover {
  opacity: 0.8;
  transform: scale(1.05);
}

.no-results {
  text-align: center;
  padding: 20px;
  color: #999;
}

/* Пагинация */
.pagination-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 10px;
}

.items-per-page select {
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.pagination-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pagination-buttons button {
  background: #f8f8f8;
  border: 1px solid #ddd;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-buttons button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Модальные окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  padding: 20px;
  margin: 0;
  border-bottom: 1px solid #eee;
  color: #292961;
}

.form-group {
  padding: 0 20px;
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group textarea {
  min-height: 80px;
  resize: vertical;
}

.modal-actions {
  padding: 15px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid #eee;
}

.save-button {
  background: #292961;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.cancel-button {
  background: #f0f0f0;
  color: #555;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.save-button:hover, .cancel-button:hover {
  opacity: 0.9;
}

/* Диалог подтверждения */
.confirm-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.confirm-dialog {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 400px;
  max-width: 90%;
  padding: 20px;
}

.confirm-dialog h3 {
  margin-top: 0;
  color: #292961;
}

.confirm-dialog p {
  margin-bottom: 20px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirm-button {
  background: #ff4d4d;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-button {
  background: #f0f0f0;
  color: #555;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
}

/* Индикатор загрузки */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #292961;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Адаптивность */
@media (max-width: 768px) {
  .tabs {
    overflow-x: auto;
    padding-bottom: 5px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .controls {
    width: 100%;
    flex-direction: column;
  }
  
  .search-box {
    width: 100%;
  }
  
  .search-box input {
    width: 100%;
    min-width: auto;
  }
  
  .create-button {
    width: 100%;
    justify-content: center;
  }
  
  .pagination-controls {
    flex-direction: column;
    gap: 15px;
  }
}
.project-stats {
  display: flex;
  gap: 30px;
  margin: 20px 0;
  padding: 20px;
  background: #f8f8f8;
  border-radius: 8px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 1.2em;
  font-weight: bold;
  color: #292961;
}

.project-actions {
  display: flex;
  gap: 15px;
  margin: 25px 0;
  justify-content: center;
}

.action-button {
  padding: 10px 15px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.action-button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.action-button.delete {
  background: #ffebee;
  color: #c62828;
}

.action-button.delete:hover {
  background: #ffcdd2;
}
</style>