<!--<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>y

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
-->

<template>
  <div id="app">
    <header class="navbar">
      <div class="navbar-logo">TestApp</div>
    </header>
    <div class="container">
      <aside class="sidebar">
        <nav>
          <ul>
            <li><router-link to="/">Tasks</router-link></li>
            <li><router-link to="/admin">Admin</router-link></li>
          </ul>
        </nav>
      </aside>
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
body {
  margin: 0;
  font-family: 'Source Sans Pro', sans-serif;
  background-color: #f0f0f0;
  color: #333333;
}

.navbar {
  background-color: #292961;
  color: white;
  padding: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.container {
  display: flex;
}

.sidebar {
  width: 200px;
  background-color: white;
  padding: 1rem;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar ul li {
  margin: 1rem 0;
}

.sidebar ul li a {
  text-decoration: none;
  color: #333333;
}

.sidebar ul li a:hover {
  color: #5c5cff;
}

.content {
  flex-grow: 1;
  padding: 1rem;

.router-link-active {
  color: #5c5cff;
  font-weight: bold;
}
}
</style>