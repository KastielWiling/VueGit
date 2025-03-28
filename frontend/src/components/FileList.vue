<template>
  <div>
    <h1>Files</h1>
    <button @click="openCreateFileModal" class="create-button">Create File</button>
    <div class="card-container">
      <div v-for="file in files" :key="file._id" class="card">
        <div class="card-content">
          <span>{{ file.name }}</span>
          <p>{{ file.filePath }}</p>
        </div>
        <div class="card-actions">
          <button @click="selectFile(file._id)" class="action-button">Select</button>
          <button @click="editFile(file)" class="action-button">Edit</button>
          <button @click="deleteFile(file._id)" class="action-button delete">Delete</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для создания/редактирования файла -->
    <div v-if="isModalOpen" class="modal">
      <h2>{{ isEditing ? 'Edit File' : 'Create File' }}</h2>
      <input v-model="fileForm.name" placeholder="Name" />
      <input v-model="fileForm.filePath" placeholder="File Path" />
      <select v-model="fileForm.tag">
        <option value="meta_file">meta_file</option>
        <option value="meta_photo">meta_photo</option>
      </select>
      <input v-if="fileForm.tag === 'meta_file'" v-model="fileForm.fps" placeholder="FPS" />
      <input v-if="fileForm.tag === 'meta_file'" v-model="fileForm.frameSize" placeholder="Frame Size" />
      <input v-model="fileForm.frameCount" placeholder="Frame Count" />
      <button @click="saveFile" class="modal-button">Save</button>
      <button @click="closeModal" class="modal-button cancel">Cancel</button>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  props: ['projectId'],
  data() {
    return {
      files: [],
      isModalOpen: false,
      isEditing: false,
      fileForm: {
        name: '',
        filePath: '',
        tag: 'meta_file',
        fps: '',
        frameSize: '',
        frameCount: 0,
      },
      currentFileId: null,
    };
  },
  async created() {
    await this.fetchFiles();
  },
  methods: {
    async fetchFiles() {
      console.log("Fetching files for project ID:", this.projectId);
      try {
        const response = await api.get(`/files/by_project/${this.projectId}`);
        console.log("Files found:", response.data);
        this.files = response.data;
      } catch (error) {
        console.error("Error fetching files:", error);
        this.files = [];
      }
    },
    selectFile(fileId) {
      this.$emit('select-file', fileId);
    },
    openCreateFileModal() {
      this.isModalOpen = true;
      this.isEditing = false;
      this.fileForm = {
        name: '',
        filePath: '',
        tag: 'meta_file',
        fps: '',
        frameSize: '',
        frameCount: 0,
      };
    },
    editFile(file) {
  this.isModalOpen = true;
  this.isEditing = true;
  this.fileForm = {
    ...file,
    fps: file.fps ? file.fps.join(',') : '',
    frameSize: file.frameSize ? file.frameSize.join(',') : '',
    projectID: file.projectID[0], // Убедитесь, что это строка
  };
  this.currentFileId = file._id;
},
async saveFile() {
  const payload = {
    name: this.fileForm.name,
    filePath: this.fileForm.filePath,
    tag: this.fileForm.tag,
    projectID: [this.projectId], // Убедитесь, что это строка
    frameCount: this.fileForm.frameCount,
    fps: this.fileForm.tag === 'meta_file' 
      ? (this.fileForm.fps ? this.fileForm.fps.split(',').map(Number) : [])
      : [],
    frameSize: this.fileForm.tag === 'meta_file'
      ? (this.fileForm.frameSize ? this.fileForm.frameSize.split(',').map(Number) : [])
      : []
  };

  try {
    if (this.isEditing) {
      await api.put(`/files/${this.currentFileId}`, payload);
    } else {
      await api.post('/files/', payload);
    }
    this.closeModal();
    await this.fetchFiles();
  } catch (error) {
    console.error("Error saving file:", error);
  }
},
    async deleteFile(fileId) {
      await api.delete(`/files/${fileId}`);
      await this.fetchFiles();
    },
    closeModal() {
      this.isModalOpen = false;
    },
  },
};
</script>

<style scoped>
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

.modal input,
.modal select {
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