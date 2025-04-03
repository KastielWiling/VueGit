<template>
  <div class="estimate-list-container">
    <div class="header-section">
      <h1>Estimates</h1>
      <button @click="openCreateEstimateModal" class="create-button">
        Create Estimate
      </button>
    </div>

    <div class="split-layout">
      <div class="estimates-panel">
        <div class="search-controls">
          <input 
            v-model="searchEstimate" 
            placeholder="Search estimates..." 
            class="search-input"
          >
        </div>
        <div class="estimates-list">
          <div 
            v-for="estimate in filteredEstimates" 
            :key="estimate._id" 
            class="estimate-card"
            :class="{ 'selected': estimate._id === selectedEstimateId }"
          >
            <div class="estimate-content" @click="selectEstimate(estimate._id)">
              <div class="estimate-info">
                <span class="estimate-tag">{{ estimate.tag }}</span>
                <div class="estimate-details">
                  <span>Frames: {{ estimate.frame_interval.join(', ') }}</span>
                  <span>ROI: {{ estimate.roi.join(', ') }}</span>
                </div>
              </div>
            </div>
            <div class="estimate-actions">
              <button @click.stop="openEditEstimateModal(estimate)" class="action-button edit">
                Edit
              </button>
              <button @click.stop="deleteEstimate(estimate._id)" class="action-button delete">
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="records-panel">
        <ChatWindow 
          v-if="selectedEstimateId" 
          :estimateId="selectedEstimateId"
          :key="selectedEstimateId"
        />
        <div v-else class="empty-state">
          Select an estimate to view records
        </div>
      </div>
    </div>

    <EstimateModal
      v-if="isModalOpen"
      :isOpen="isModalOpen"
      :isEditing="isEditing"
      :estimateData="estimateForm"
      @save="handleSaveEstimate"
      @close="closeModal"
      :key="modalKey"
    />
  </div>
</template>

<script>
import api from '@/api';
import ChatWindow from '@/components/ChatWindow.vue';
import EstimateModal from '@/components/EstimateModal.vue';

export default {
  components: {
    ChatWindow,
    EstimateModal
  },
  props: {
    fileId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      estimates: [],
      searchEstimate: '',
      isModalOpen: false,
      isEditing: false,
      estimateForm: {
        tag: '',
        frame_interval: '',
        roi: ''
      },
      currentEstimateId: null,
      selectedEstimateId: null,
      modalKey: 0
    };
  },
  computed: {
    filteredEstimates() {
      return this.estimates.filter(est => 
        est.tag.toLowerCase().includes(this.searchEstimate.toLowerCase()) ||
        est.frame_interval.join(',').includes(this.searchEstimate) ||
        est.roi.join(',').includes(this.searchEstimate)
      );
    }
  },
  methods: {
    async fetchEstimates() {
      try {
        const response = await api.get(`/estimates/by_file/${this.fileId}`);
        this.estimates = response.data;
      } catch (error) {
        console.error("Error fetching estimates:", error);
        alert("Failed to load estimates");
      }
    },

    selectEstimate(estimateId) {
      this.selectedEstimateId = estimateId;
    },

    openCreateEstimateModal() {
      this.isModalOpen = true;
      this.isEditing = false;
      this.estimateForm = {
        tag: '',
        frame_interval: '',
        roi: ''
      };
      this.currentEstimateId = null;
      this.modalKey += 1;
    },

    openEditEstimateModal(estimate) {
      this.isModalOpen = true;
      this.isEditing = true;
      this.estimateForm = {
        tag: estimate.tag,
        frame_interval: estimate.frame_interval.join(','),
        roi: estimate.roi.join(',')
      };
      this.currentEstimateId = estimate._id;
      this.modalKey += 1;
    },

    async handleSaveEstimate(estimateData) {
      try {
        // Преобразование данных в правильный формат
        const frameInterval = typeof estimateData.frame_interval === 'string'
          ? estimateData.frame_interval.split(',').map(Number).filter(n => !isNaN(n))
          : estimateData.frame_interval;
        
        const roi = typeof estimateData.roi === 'string'
          ? estimateData.roi.split(',').map(Number).filter(n => !isNaN(n))
          : estimateData.roi;

        const payload = {
          file_id: [this.fileId],
          frame_interval: frameInterval,
          roi: roi,
          tag: estimateData.tag,
          settings: {}
        };

        if (this.isEditing) {
          await api.put(`/estimates/${this.currentEstimateId}`, payload);
          alert("Estimate updated successfully");
        } else {
          await api.post('/estimates/', payload);
          alert("Estimate created successfully");
        }
        
        this.closeModal();
        await this.fetchEstimates();
      } catch (error) {
        console.error("Error saving estimate:", error);
        alert(`Error: ${error.response?.data?.message || error.message}`);
      }
    },

    async deleteEstimate(estimateId) {
      if (confirm("Are you sure you want to delete this estimate?")) {
        try {
          await api.delete(`/estimates/${estimateId}`);
          await this.fetchEstimates();
          if (this.selectedEstimateId === estimateId) {
            this.selectedEstimateId = null;
          }
          alert("Estimate deleted successfully");
        } catch (error) {
          console.error("Error deleting estimate:", error);
          alert("Failed to delete estimate");
        }
      }
    },

    closeModal() {
      this.isModalOpen = false;
    }
  },
  async created() {
    await this.fetchEstimates();
  },
  watch: {
    fileId: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchEstimates();
        }
      }
    }
  }
};
</script>

<style scoped>
.estimate-list-container {
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.create-button {
  background-color: #292961;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.create-button:hover {
  background-color: #3a3a7a;
  transform: translateY(-1px);
}

.split-layout {
  display: flex;
  flex: 1;
  gap: 20px;
  height: calc(100% - 60px);
}

.estimates-panel {
  width: 350px;
  border-right: 1px solid #eee;
  display: flex;
  flex-direction: column;
}

.records-panel {
  flex: 1;
  min-width: 0;
}

.search-controls {
  padding: 10px;
  background: #f8f8f8;
  border-bottom: 1px solid #eee;
}

.search-input {
  width: 90%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.estimates-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.estimate-card {
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 6px;
  transition: all 0.2s;
  display: flex;
  justify-content: space-between;
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.estimate-card:hover {
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.estimate-card.selected {
  border-left: 3px solid #292961;
  background-color: #f0f0ff;
}

.estimate-content {
  flex: 1;
  cursor: pointer;
}

.estimate-info {
  margin-bottom: 5px;
}

.estimate-tag {
  font-weight: bold;
  display: block;
  color: #292961;
}

.estimate-details {
  font-size: 0.85em;
  color: #666;
}

.estimate-details span {
  display: block;
  margin: 2px 0;
}

.estimate-actions {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.action-button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85em;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s;
}

.action-button.edit {
  background-color: #292961;
  color: white;
}

.action-button.delete {
  background-color: #ff4d4d;
  color: white;
}

.action-button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  font-size: 1.1em;
}

.empty-state i {
  font-size: 2em;
  margin-bottom: 10px;
}
</style>