<script>
import axios from 'axios';

export default {
  data() {
    return {
      showDisplayNavbar: false,
      showAdminButton: false,
      showLogoutButton: false,
    };
  },
  methods: {
    goToAdminAuth() {
      this.$router.push('/admin-auth')
    },
    logout() {
      const path = 'http://127.0.0.1:5000/';
      axios.post(path + 'logout')
        .then(response => {
          console.log('Logout successful:', response.data);
          // Clear auth token and role from local storage

          const tokenKey = 'auth-token';
          const roleKey = 'role';
          localStorage.removeItem(tokenKey);
          localStorage.removeItem(roleKey);
          // Redirect to the login page or perform other actions based on the response
          this.$router.push('/login-user');
        })
        .catch(error => {
          console.error('Logout error:', error.response.data.error);
        });
    },
    shouldDisplayNavbarOnRoute(route) {
      //return route.name !== 'UserHome'
      return true;
    },
    shouldDisplayAdminButton(route) {
      return route.name === 'UserAuth' || route.name === 'CreatorAuth';
    },
    shouldDisplayLogoutButton(route) {
      return route.name !== 'UserAuth' && route.name !== 'CreatorAuth';
    }
  },
  watch: {
    // Watch for changes in the route and update shouldDisplayNavbar accordingly
    $route(to, from) {
      this.showDisplayNavbar = this.shouldDisplayNavbarOnRoute(to);
      this.showLogoutButton = this.shouldDisplayLogoutButton(to);
      this.showAdminButton = this.shouldDisplayAdminButton(to);
    },
  },
  created() {
    // Set the initial value of shouldDisplayNavbar based on the current route
    this.showDisplayNavbar = this.shouldDisplayNavbarOnRoute(this.$route);
    this.showDisplayLogoutButton = this.shouldDisplayLogoutButton(this.$route);
    this.showAdminButton = this.shouldDisplayAdminButton(this.$route);
  },
};
</script>

<template>
  <div>
    <!-- Navbar -->
    <nav v-show="showDisplayNavbar" class="navbar">
      <a href="https://vuejs.org/" target="_blank" class="logo-container">
        <img src="./assets/vue.svg" class="logo" alt="Vue logo" />
      </a>
      <h2>Trance</h2>
      <router-link class="nav-link" to="/">Home</router-link>
      <router-link class="nav-link" to="/login-user">Login</router-link>
      <router-link class="nav-link" to="/home-user">User Home</router-link>
      <router-link class="nav-link" to="/home-creator">Creator Home</router-link>
      <button v-if="showAdminButton" @click="goToAdminAuth()" class="logout-btn">Admin</button>
      <button v-if="showLogoutButton" @click="logout()" class="logout-btn">Logout</button>
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
  padding: 20px;
  box-shadow: 0 0 50px rgba(255, 255, 255, 0.1);
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
