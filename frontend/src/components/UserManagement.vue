<template>
    <div class="user-management">
      <h1>User Management</h1>
      <div class="user-form">
        <input v-model="newUser.username" placeholder="Username" class="user-input" />
        <input v-model="newUser.email" placeholder="Email" class="user-input" />
        <button @click="createUser" class="user-button">Create User</button>
      </div>
      <ul class="user-list">
        <li v-for="user in users" :key="user._id" class="user-item">
          <div class="user-content">
            <h3>{{ user.username }}</h3>
            <p>{{ user.email }}</p>
            <small>Admin: {{ user.is_admin ? 'Yes' : 'No' }}</small>
          </div>
          <div class="user-actions">
            <button @click="toggleAdmin(user)" class="user-button">
              {{ user.is_admin ? 'Revoke Admin' : 'Make Admin' }}
            </button>
            <button @click="deleteUser(user._id)" class="user-button delete">Delete</button>
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
        users: [],
        newUser: {
          username: '',
          email: '',
          is_admin: false,
        },
      };
    },
    async created() {
      await this.fetchUsers();
    },
    methods: {
      async fetchUsers() {
        const response = await axios.get('http://localhost:8000/admin/users/');
        this.users = response.data;
      },
      async createUser() {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(this.newUser.email)) {
          alert('Please enter a valid email address.');
          return;
        }
        await axios.post('http://localhost:8000/admin/users/', this.newUser);
        await this.fetchUsers();
        this.newUser = { username: '', email: '', is_admin: false };
      },
      async toggleAdmin(user) {
        user.is_admin = !user.is_admin;
        await axios.put(`http://localhost:8000/admin/users/${user._id}`, user);
        await this.fetchUsers();
      },
      async deleteUser(userId) {
        await axios.delete(`http://localhost:8000/admin/users/${userId}`);
        await this.fetchUsers();
      },
    },
  };
  </script>
  
  <style scoped>
  .user-management {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .user-form {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
  }
  
  .user-input {
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-family: 'Source Sans Pro', sans-serif;
  }
  
  .user-button {
    background-color: #5c5cff;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-family: 'Source Sans Pro', sans-serif;
  }
  
  .user-button.delete {
    background-color: #ff5c5c;
  }
  
  .user-list {
    list-style: none;
    padding: 0;
  }
  
  .user-item {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .user-content h3 {
    margin: 0;
    color: #292961;
  }
  
  .user-content p {
    margin: 0.5rem 0;
    color: #666;
  }
  
  .user-actions {
    display: flex;
    gap: 0.5rem;
  }
  </style>