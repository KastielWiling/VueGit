<template>
  <div>
    <h1>Estimates</h1>
    <button @click="openCreateEstimateModal" class="create-button">Create Estimate</button>
    <div class="card-container">
      <div v-for="estimate in estimates" :key="estimate._id" class="card">
        <div class="card-content">
          <span>{{ estimate.tag }}</span>
          <p>Frame Interval: {{ estimate.frame_interval.join(', ') }}</p>
          <p>ROI: {{ estimate.roi.join(', ') }}</p>
        </div>
        <div class="card-actions">
          <button @click="selectEstimate(estimate._id)" class="action-button">Select</button>
          <button @click="editEstimate(estimate)" class="action-button">Edit</button>
          <button @click="deleteEstimate(estimate._id)" class="action-button delete">Delete</button>
        </div>
      </div>
    </div>

    <!-- Чат-окно -->
    <ChatWindow v-if="selectedEstimateId" :estimateId="selectedEstimateId" />

    <!-- Модальное окно для создания/редактирования оценки -->
    <div v-if="isModalOpen" class="modal">
      <h2>{{ isEditing ? 'Edit Estimate' : 'Create Estimate' }}</h2>
      <input v-model="estimateForm.tag" placeholder="Tag" />
      <input v-model="estimateForm.frame_interval" placeholder="Frame Interval (comma separated)" />
      <input v-model="estimateForm.roi" placeholder="ROI (comma separated)" />
      <button @click="saveEstimate" class="modal-button">Save</button>
      <button @click="closeModal" class="modal-button cancel">Cancel</button>
    </div>
  </div>
</template>

<script>
import api from '@/api';
import ChatWindow from '@/components/ChatWindow.vue'; // Импортируем компонент чата

export default {
  components: {
    ChatWindow, // Регистрируем компонент чата
  },
  props: ['fileId'],
  data() {
    return {
      estimates: [],
      isModalOpen: false,
      isEditing: false,
      estimateForm: {
        tag: '',
        frame_interval: [],
        roi: [],
      },
      currentEstimateId: null,
      selectedEstimateId: null, // Для выбранной оценки
    };
  },
  async created() {
    await this.fetchEstimates();
  },
  methods: {
    async fetchEstimates() {
      const response = await api.get(`/estimates/by_file/${this.fileId}`);
      this.estimates = response.data;
    },
    openCreateEstimateModal() {
      this.isModalOpen = true;
      this.isEditing = false;
      this.estimateForm = {
        tag: '',
        frame_interval: [],
        roi: [],
      };
    },
    editEstimate(estimate) {
      this.isModalOpen = true;
      this.isEditing = true;
      this.estimateForm = {
        ...estimate,
        frame_interval: estimate.frame_interval.join(','),
        roi: estimate.roi.join(','),
      };
      this.currentEstimateId = estimate._id;
    },
    async saveEstimate() {
  const payload = {
    file_id: [this.fileId], // Передаем как массив строк
    frame_interval: Array.isArray(this.estimateForm.frame_interval)
      ? this.estimateForm.frame_interval
      : this.estimateForm.frame_interval.split(',').map(Number),
    roi: Array.isArray(this.estimateForm.roi)
      ? this.estimateForm.roi
      : this.estimateForm.roi.split(',').map(Number),
    tag: this.estimateForm.tag,
    settings: {},
  };

  try {
    console.log("Sending payload:", payload);
    if (this.isEditing) {
      await api.put(`/estimates/${this.currentEstimateId}`, payload);
    } else {
      await api.post('/estimates/', payload);
    }
    this.closeModal();
    await this.fetchEstimates();
  } catch (error) {
    console.error("Error saving estimate:", error.response?.data || error.message);
  }
},
    async deleteEstimate(estimateId) {
      await api.delete(`/estimates/${estimateId}`);
      await this.fetchEstimates();
    },
    closeModal() {
      this.isModalOpen = false;
    },
    // Метод для выбора оценки
    selectEstimate(estimateId) {
      this.selectedEstimateId = estimateId; // Устанавливаем выбранную оценку
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