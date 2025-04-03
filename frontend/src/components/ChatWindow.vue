<template>
  <div class="chat-window">
    <div class="controls">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.type"
          :class="{ active: activeTab === tab.type }"
          @click="activeTab = tab.type"
        >
          {{ tab.label }}
        </button>
      </div>
      <div class="search-sort">
        <input 
          v-model="searchQuery" 
          placeholder="Search by frame..." 
          class="search-input"
        >
        <select v-model="sortField" class="sort-select">
          <option value="frame">Sort by Frame</option>
          <option value="tag">Sort by Type</option>
        </select>
      </div>
    </div>

    <div class="records-container">
      <div 
        v-for="record in paginatedRecords" 
        :key="record._id" 
        class="record-item"
        :class="record.tag"
      >
        <div class="record-header">
          <span class="record-tag">{{ record.tag }}</span>
          <span class="record-frame">Frame: {{ record.frame }}</span>
        </div>
        <pre>{{ formatRecordData(record.record) }}</pre>
      </div>
    </div>

    <div class="footer-controls">
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">
          <i class="fas fa-chevron-left"></i>
        </button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
      <div class="page-size">
        <span>Items per page:</span>
        <select v-model="itemsPerPage">
          <option value="10">10</option>
          <option value="20">20</option>
          <option value="50">50</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  props: ['estimateId'],
  data() {
    return {
      records: [],
      activeTab: 'all',
      searchQuery: '',
      sortField: 'frame',
      currentPage: 1,
      itemsPerPage: 20,
      tabs: [
        { type: 'all', label: 'All' },
        { type: 'meta_crack_model', label: 'Crack Model' },
        { type: 'meta_record', label: 'Meta Record' },
        { type: 'interface_moire', label: 'Interface Moire' },
        { type: 'velocimetry', label: 'Velocimetry' }
      ]
    };
  },
  computed: {
    filteredRecords() {
      let filtered = this.records;
      
      if (this.activeTab !== 'all') {
        filtered = filtered.filter(r => r.tag === this.activeTab);
      }
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(r => 
          String(r.frame).includes(query) || 
          JSON.stringify(r.record).toLowerCase().includes(query)
        );
      }
      
      return filtered.sort((a, b) => {
        // Сортировка по типу
        const typeOrder = {
          'meta_crack_model': 1,
          'interface_moire': 2,
          'velocimetry': 3,
          'meta_record': 4
        };
        
        if (this.sortField === 'tag' && typeOrder[a.tag] !== typeOrder[b.tag]) {
          return typeOrder[a.tag] - typeOrder[b.tag];
        }
        // Сортировка по frame
        return a.frame - b.frame;
      });
    },
    paginatedRecords() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredRecords.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredRecords.length / this.itemsPerPage);
    }
  },
  methods: {
    async fetchRecords() {
      if (this.estimateId) {
        try {
          const response = await api.get(`/records/by_estimate/${this.estimateId}`);
          this.records = response.data;
          this.currentPage = 1;
        } catch (error) {
          console.error("Error fetching records:", error);
          this.records = [];
        }
      }
    },
    formatRecordData(data) {
      return JSON.stringify(data, null, 2);
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    }
  },
  watch: {
    estimateId: {
      immediate: true,
      handler: 'fetchRecords'
    },
    itemsPerPage() {
      this.currentPage = 1;
    }
  }
};
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.controls {
  padding: 15px;
  background: #f8f8f8;
  border-bottom: 1px solid #eee;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.tabs button {
  padding: 8px 15px;
  border: none;
  background: #e0e0e0;
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.9em;
}

.tabs button.active {
  background: #292961;
  color: white;
}

.search-sort {
  display: flex;
  gap: 10px;
  flex-grow: 1;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

.sort-select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.records-container {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
}

.record-item {
  margin-bottom: 15px;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.record-header {
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9em;
}

.record-tag {
  font-weight: bold;
  text-transform: capitalize;
}

.record-frame {
  color: #666;
}

pre {
  margin: 0;
  padding: 15px;
  background: #f8f8f8;
  overflow-x: auto;
  max-height: 200px;
}

.footer-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  border-top: 1px solid #eee;
  background: #f8f8f8;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pagination button {
  width: 30px;
  height: 30px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-size {
  display: flex;
  align-items: center;
  gap: 5px;
}

.page-size select {
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* Цветовые метки для разных типов записей */
.record-item.meta_crack_model .record-header {
  background: #ffebee;
}

.record-item.meta_record .record-header {
  background: #e8f5e9;
}

.record-item.interface_moire .record-header {
  background: #e3f2fd;
}

.record-item.velocimetry .record-header {
  background: #f3e5f5;
}
</style>