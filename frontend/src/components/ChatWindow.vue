<template>
    <div class="chat-window">
      <div class="chat-header">
        <h2>Chat Logs</h2>
        <button @click="clearChat" class="clear-button">Clear</button>
      </div>
      <div class="chat-content">
        <div v-for="(record, index) in records" :key="index" class="record-item">
          <h3>Record {{ index + 1 }}</h3>
          <p><strong>Frame:</strong> {{ record.frame }}</p>
          <p><strong>Data:</strong></p>
          <pre>{{ formatRecordData(record.record) }}</pre>
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
      };
    },
    async created() {
      await this.fetchRecords();
    },
    methods: {
      async fetchRecords() {
        if (this.estimateId) {
          const response = await api.get(`/records/by_estimate/${this.estimateId}`);
          this.records = response.data;
        }
      },
      formatRecordData(data) {
        return JSON.stringify(data, null, 2);
      },
      clearChat() {
        this.records = [];
      },
    },
    watch: {
      estimateId: {
        immediate: true,
        handler: 'fetchRecords',
      },
    },
  };
  </script>
  
  <style scoped>
  .chat-window {
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 16px;
    background-color: #f9f9f9;
    max-height: 400px;
    overflow-y: auto;
    margin-top: 20px;
  }
  
  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }
  
  .clear-button {
    background-color: #ff4d4d;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .clear-button:hover {
    background-color: #ff6666;
  }
  
  .record-item {
    margin-bottom: 16px;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
  }
  
  pre {
    background-color: #f5f5f5;
    padding: 8px;
    border-radius: 4px;
    overflow-x: auto;
  }
  </style>