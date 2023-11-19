<script>
import axios from 'axios';

export default {
  methods: {
    goToAdminAuth() {
      this.$router.push('/admin-auth')
    },
    logout() {
      // Call the logout endpoint using Axios
      const path = 'http://127.0.0.1:5000/';
      axios.get(path + 'logout')
        .then(response => {
          // Handle the successful logout
          console.log('Logout successful:', response.data);
          // You can perform additional actions here if needed
        })
        .catch(error => {
          // Handle errors
          console.error('Logout error:', error);
        });
    }
  }
};
</script>

<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar">
      <a href="https://vuejs.org/" target="_blank" class="logo-container">
        <img src="./assets/vue.svg" class="logo" alt="Vue logo" />
      </a>
      <h2>Trance</h2>
      <router-link class="nav-link" to="/">Home</router-link>
      <router-link class="nav-link" to="/login">Login</router-link>
      <router-link class="nav-link" to="/home-user">User Home</router-link>
      <button @click="goToAdminAuth()" class="logout-btn">Admin</button>
      <!-- Add more links as needed -->
    </nav>

    <!-- Main Content -->
    <div class="main-content">


      <!-- Router View -->
      <router-view></router-view>
    </div>
  </div>
</template>

<style scoped>
/* Reset default margin and padding */
body,
html {
  margin: 0;
  padding: 0;
}

/* Navbar styles */
.navbar {
  width: 100%;
  display: flex;
  align-items: center;
  padding-left: 2rem;
}

.logo-container {
  margin-right: 1em;
}

/* Logo styles */
.logo {
  height: 3em;
  will-change: filter;
  transition: filter 300ms;
}

/* Hover effect for the Vue logo */
.logo:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

/* Main content styles */
.main-content {
  padding: 1em;
}

/* Navbar link styles */
.nav-link {
  color: white;
  align-self: center;
  text-decoration: none;
  margin-left: 3rem;
}

/* Logout button styles */
.logout-btn {
  padding: 0.5em 1em;
  background-color: #42b883;
  color: white;
  border: none;
  cursor: pointer;
  margin-left: auto;
  margin-right: 3%;
  font-size: 1em;
}
</style>
