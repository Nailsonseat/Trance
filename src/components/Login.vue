<template>
    <div class="login-container">
        <h1>{{ isLogin ? 'Login' : 'Register' }}</h1>
        <form @submit.prevent="submitForm">
            <label for="username">Email:</label>
            <input type="text" id="username" v-model="email" />

            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" />

            <!-- Additional fields for registration -->
            <label v-if="!isLogin" for="confirm-password">Confirm Password:</label>
            <input v-if="!isLogin" type="password" id="confirm-password" v-model="confirmPassword" />

            <button type="submit">{{ isLogin ? 'Login' : 'Register' }}</button>
        </form>

        <!-- Switch to toggle between login and register forms -->
        <label class="switch">

        </label>

        <Toggle v-model="isLogin" on-label="Login" off-label="Register" />
        <span>{{ isLogin ? 'Login' : 'Register' }}</span>
    </div>
</template>
<style src="@vueform/toggle/themes/default.css"></style>
<script>
import axios from 'axios';
import Toggle from '@vueform/toggle'

export default {
    data() {
        return {
            email: '',
            password: '',
            confirmPassword: '',
            isLogin: true, // Default to show login form
        };
    },
    components: {
        Toggle,
    },
    methods: {
        async submitForm() {
            // Add your logic for login or register based on the value of isLogin
            if (this.isLogin) {
                // Login logic
                console.log('Logging in with:', this.email, this.password);
            } else {
                // Register logic
                console.log('Registering with:', this.email, this.password, this.confirmPassword);
            }

            const path = 'http://127.0.0.1:5000/';
            axios.post(path + 'login-user', { email: this.email, password: this.password }, { headers: { 'Access-Control-Allow-Origin': '*' } })
                .then(response => {
                    console.log('Operation successful:', response.data);
                    // Redirect to the dashboard or perform other actions based on the response
                    this.$router.push('/dashboard');
                })
                .catch(error => {
                    console.error('Operation error:', error.response.data.error);
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

/* Switch styles */
.switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
}

.slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
}

input:checked+.slider {
    background-color: #42b883;
}

input:focus+.slider {
    box-shadow: 0 0 1px #42b883;
}

input:checked+.slider:before {
    -webkit-transform: translateX(26px);
    -ms-transform: translateX(26px);
    transform: translateX(26px);
}
</style>
