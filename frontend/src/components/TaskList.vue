<template>
    <div class="task-manager">
      <h1>Tasks</h1>
      <div class="task-form">
        <input v-model="newTask.title" placeholder="Title" class="task-input" />
        <textarea v-model="newTask.description" placeholder="Description" class="task-textarea"></textarea>
        <button @click="createTask" class="task-button">Create Task</button>
      </div>
      <ul class="task-list">
        <li v-for="task in tasks" :key="task._id" class="task-item">
          <div class="task-content">
            <h3>{{ task.title }}</h3>
            <p>{{ task.description }}</p>
            <small>Created at: {{ new Date(task.created_at).toLocaleString() }}</small>
          </div>
          <div class="task-actions">
            <button @click="toggleComplete(task)" :class="['task-button', task.completed ? 'completed' : '']">
              {{ task.completed ? 'Undo' : 'Complete' }}
            </button>
            <button @click="deleteTask(task._id)" class="task-button delete">Delete</button>
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        tasks: [],
        newTask: {
          title: '',
          description: ''
        }
      };
    },
    async created() {
      await this.fetchTasks();
    },
    methods: {
      async fetchTasks() {
        const response = await axios.get('http://localhost:8000/tasks/');
        this.tasks = response.data;
      },
      async createTask() {
        await axios.post('http://localhost:8000/tasks/', this.newTask);
        await this.fetchTasks();
        this.newTask = { title: '', description: '' };
      },
      async toggleComplete(task) {
        await axios.put(`http://localhost:8000/tasks/${task._id}`, { completed: !task.completed });
        await this.fetchTasks();
      },
      async deleteTask(taskId) {
        await axios.delete(`http://localhost:8000/tasks/${taskId}`);
        await this.fetchTasks();
      }
    }
  };
  </script>
  
  <style scoped>
  .task-manager {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .task-form {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
  }
  
  .task-input, .task-textarea {
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-family: 'Source Sans Pro', sans-serif;
  }
  
  .task-button {
    background-color: #5c5cff;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-family: 'Source Sans Pro', sans-serif;
  }
  
  .task-button.delete {
    background-color: #ff5c5c;
  }
  
  .task-button.completed {
    background-color: #4caf50;
  }
  
  .task-list {
    list-style: none;
    padding: 0;
  }
  
  .task-item {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .task-content h3 {
    margin: 0;
    color: #292961;
  }
  
  .task-content p {
    margin: 0.5rem 0;
    color: #666;
  }
  
  .task-actions {
    display: flex;
    gap: 0.5rem;
  }
  </style>