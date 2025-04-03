<template>
    <div class="modal-overlay" v-if="isOpen" @click.self="close">
      <div class="modal-content">
        <h2>{{ isEditing ? 'Edit Estimate' : 'Create Estimate' }}</h2>
        
        <div class="form-group">
          <label>Tag:</label>
          <input 
            v-model="formData.tag" 
            placeholder="Estimate tag" 
            @keyup.enter="save"
          />
        </div>
        
        <div class="form-group">
          <label>Frame Interval (comma separated):</label>
          <input 
            v-model="formData.frame_interval" 
            placeholder="e.g. 1,2,3,4" 
            @keyup.enter="save"
          />
        </div>
        
        <div class="form-group">
          <label>ROI (comma separated):</label>
          <input 
            v-model="formData.roi" 
            placeholder="e.g. 10,20,30,40" 
            @keyup.enter="save"
          />
        </div>
  
        <div class="modal-actions">
          <button @click="save" class="save-button">
            <i class="fas fa-save"></i> {{ isEditing ? 'Update' : 'Create' }}
          </button>
          <button @click="close" class="cancel-button">
            <i class="fas fa-times"></i> Cancel
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      isOpen: {
        type: Boolean,
        required: true
      },
      isEditing: {
        type: Boolean,
        default: false
      },
      estimateData: {
        type: Object,
        default: () => ({
          tag: '',
          frame_interval: '',
          roi: ''
        })
      }
    },
    data() {
      return {
        formData: {
          tag: '',
          frame_interval: '',
          roi: ''
        }
      };
    },
    watch: {
      estimateData: {
        immediate: true,
        deep: true,
        handler(newVal) {
          console.log("Modal received new data:", newVal);
          this.formData = {
            tag: newVal.tag || '',
            frame_interval: newVal.frame_interval || '',
            roi: newVal.roi || ''
          };
        }
      }
    },
    methods: {
      save() {
        console.log("Saving form data:", this.formData);
        
        // Валидация данных
        if (!this.formData.tag.trim()) {
          alert("Please enter a tag");
          return;
        }
  
        if (!this.formData.frame_interval || !this.formData.roi) {
          alert("Please enter frame interval and ROI");
          return;
        }
  
        // Преобразуем строки в массивы чисел
        const dataToSave = {
          tag: this.formData.tag.trim(),
          frame_interval: this.parseNumberArray(this.formData.frame_interval),
          roi: this.parseNumberArray(this.formData.roi)
        };
  
        this.$emit('save', dataToSave);
      },
      close() {
        this.$emit('close');
      },
      parseNumberArray(str) {
        try {
          return str.split(',')
            .map(item => item.trim())
            .filter(item => item !== '')
            .map(Number);
        } catch (e) {
          console.error("Error parsing array:", e);
          return [];
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: white;
    padding: 25px;
    border-radius: 8px;
    width: 450px;
    max-width: 90%;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  }
  
  h2 {
    margin-top: 0;
    color: #292961;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #555;
  }
  
  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
  }
  
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
  }
  
  button {
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s;
  }
  
  .save-button {
    background-color: #292961;
    color: white;
  }
  
  .cancel-button {
    background-color: #f0f0f0;
    color: #555;
  }
  
  button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
  }
  
  button:active {
    transform: translateY(0);
  }
  
  button i {
    font-size: 14px;
  }
  </style>