<template>
    <div class="login-container">
        <h1>Admin Login</h1>
        <form @submit.prevent="login">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" />

            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" />

            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {

    data() {
        return {
            username: '',
            password: '',
        };
    },
    methods: {
        async login() {
            const path = 'http://127.0.0.1:5000/';
            axios.post(path + 'admin-login', { username: this.username, password: this.password })
                .then(response => {
                    console.log('Admin Login successful:', response.data);
                    // You can perform additional actions here if needed
                })
                .catch(error => {
                    console.error('Admin Login error:', error.response.data.error);
                });
        },
    },
};
</script>

<style scoped>
.login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

form {
    display: flex;
    flex-direction: column;
}

label {
    margin-bottom: 5px;
}

input {
    margin-bottom: 10px;
    padding: 8px;
    font-size: 14px;
}

button {
    padding: 10px;
    background-color: #42b883;
    color: white;
    border: none;
    cursor: pointer;
}
</style>
