<!-- Dashboard.vue -->
<template>
  <div class="dashboard">
    <h1>Welcome to the Dashboard, {{ username }}</h1>
    <p>This is a simple Vue dashboard.</p>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: 'John Doe', // Replace with actual username or fetch from the server
    };
  },
  methods: {
    logout() {
      // Implement logout logic here, e.g., redirect to the login page
      this.$router.push('/login'); // Redirect to the login page
    },
  },
};
</script>

<style scoped>
.dashboard {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

button {
  padding: 10px;
  background-color: #42b883;
  color: white;
  border: none;
  cursor: pointer;
  margin-top: 10px;
}
</style>
