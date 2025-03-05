<template>
  <div>
    <h1>Projects</h1>
    <button @click="openCreateProjectModal" class="create-button">Create Project</button>
    <div class="card-container">
      <div v-for="project in projects" :key="project._id" class="card">
        <div class="card-content">
          <span>{{ project.name }}</span>
          <p>{{ project.desc }}</p>
        </div>
        <div class="card-actions">
          <button @click="selectProject(project._id)" class="action-button">Select</button>
          <button @click="editProject(project)" class="action-button">Edit</button>
          <button @click="deleteProject(project._id)" class="action-button delete">Delete</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для создания/редактирования проекта -->
    <div v-if="isModalOpen" class="modal">
      <h2>{{ isEditing ? 'Edit Project' : 'Create Project' }}</h2>
      <input v-model="projectForm.name" placeholder="Name" />
      <input v-model="projectForm.desc" placeholder="Description" />
      <button @click="saveProject" class="modal-button">Save</button>
      <button @click="closeModal" class="modal-button cancel">Cancel</button>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  data() {
    return {
      projects: [],
      isModalOpen: false,
      isEditing: false,
      projectForm: {
        name: '',
        desc: '',
      },
      currentProjectId: null,
    };
  },
  async created() {
    await this.fetchProjects();
  },
  methods: {
    async fetchProjects() {
      const response = await api.get('/projects/');
      this.projects = response.data;
    },
    selectProject(projectId) {
      this.$emit('select-project', projectId);
    },
    openCreateProjectModal() {
      this.isModalOpen = true;
      this.isEditing = false;
      this.projectForm = { name: '', desc: '' };
    },
    editProject(project) {
      this.isModalOpen = true;
      this.isEditing = true;
      this.projectForm = { name: project.name, desc: project.desc };
      this.currentProjectId = project._id;
    },
    async saveProject() {
      const payload = {
        name: this.projectForm.name,
        desc: this.projectForm.desc,
        something: [],
        tag: "default_tag",
      };

      if (this.isEditing) {
        await api.put(`/projects/${this.currentProjectId}`, payload);
      } else {
        await api.post('/projects/', payload);
      }
      this.closeModal();
      await this.fetchProjects();
    },
    async deleteProject(projectId) {
      await api.delete(`/projects/${projectId}`);
      await this.fetchProjects();
    },
    closeModal() {
      this.isModalOpen = false;
    },
  },
};
</script>

<style>
.create-button {
  background-color: #292961;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s;
}

.create-button:hover {
  background-color: #3a3a7a;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card-content {
  padding: 20px;
}

.card-content span {
  font-size: 18px;
  font-weight: bold;
}

.card-content p {
  margin: 10px 0 0;
  color: #666;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  padding: 10px;
  background-color: #f9f9f9;
}

.action-button {
  background-color: #292961;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #3a3a7a;
}

.action-button.delete {
  background-color: #ff4d4d;
}

.action-button.delete:hover {
  background-color: #ff6666;
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

.modal input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-button {
  background-color: #292961;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
  transition: background-color 0.3s;
}

.modal-button:hover {
  background-color: #3a3a7a;
}

.modal-button.cancel {
  background-color: #ff4d4d;
}

.modal-button.cancel:hover {
  background-color: #ff6666;
}
</style>