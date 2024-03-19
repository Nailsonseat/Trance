<template>
    <div class="auth-component">
        <div class="role-switcher" style="display: flex;">
            <button class="user-role-button">User</button>
            <button @click="goToCreatorAuth()" class="creator-role-button">Creator</button>
        </div>
        <div class="login-container">
            <h1 class="page-title">{{ isLoginPage ? 'Login' : 'Register' }}</h1>
            <form @submit.prevent="submitForm">

                <label class="input-label" v-if="!isLoginPage" for="username">Username</label>
                <input class="input" v-if="!isLoginPage" type="text" id="username" v-model="username" />

                <label class="input-label" for="email">Email</label>
                <input class="input" type="text" id="email" v-model="email" />

                <label class="input-label" for="password">Password</label>
                <input class="input" type="password" id="password" v-model="password"
                    :type="showPassword ? 'text' : 'password'" />

                <!-- Confirm Password field for registration -->
                <label class="input-label" v-if="!isLoginPage" for="confirm-password">Confirm Password</label>
                <input class="input" v-if="!isLoginPage" id="confirm-password" v-model="confirmPassword" />

                <!-- Warning text for password mismatch -->
                <p v-if="!isLoginPage && password !== confirmPassword" class="warning-text">Passwords do not match!</p>



                <button class="submit-button" type="submit">{{ isLoginPage ? 'Login' : 'Register' }}</button>
            </form>

            <!-- Switch to toggle between login and register forms -->
            <div class="toggle-container">
                <span>{{ isLoginPage ? "Don't have an account?" : "Already have an account?" }}</span>
                <Toggle class="switcher" v-model="isLoginPage" on-label="Login" off-label="Register" />
            </div>
        </div>
    </div>
</template>


<style src="@vueform/toggle/themes/default.css"></style>

<script>
import axios from 'axios';
import Toggle from '@vueform/toggle';

export default {
    data() {
        return {
            email: '',
            username: '',
            password: '',
            confirmPassword: '',
            isLoginPage: true,
            showPassword: false,
        };
    },
    components: {
        Toggle,
    },
    methods: {
        goToCreatorAuth() {
            this.$router.push('/login-creator');
        },
        togglePasswordVisibility() {
            this.showPassword = !this.showPassword;
        },
        isLocalStorageSupported() {
            try {
                const testKey = 'test';
                localStorage.setItem(testKey, testKey);
                localStorage.removeItem(testKey);
                return true;
            } catch (e) {
                return false;
            }
        },
        submitForm() {
            const path = 'http://127.0.0.1:5000/';
            if (this.isLoginPage) {
                // Login logic
                console.log('Logging in with:', this.email, this.password);
                axios.post(path + 'login-user', { email: this.email, password: this.password, role: "user" }, { headers: { 'Access-Control-Allow-Origin': '*' } })
                    .then(response => {
                        const token = response.data.token;
                        const role = response.data.role;
                        const id = response.data.id;
                        console.log('Operation successful (Login) :', response.data);
                        // Redirect to the dashboard or perform other actions based on the response

                        if (this.isLocalStorageSupported()) {
                            const tokenKey = 'auth-token';
                            const roleKey = 'role';
                            const idKey = 'id';
                            localStorage.setItem(idKey, id);
                            localStorage.setItem(tokenKey, token);
                            localStorage.setItem(roleKey, role);
                        }


                        this.$router.push('/home-user');
                    })
                    .catch(error => {
                        console.error('Operation error (Login) :', error.response.data.error);
                    });

            } else if (this.password === this.confirmPassword) {
                console.log('Registering in with:', this.email, this.password);
                axios.post(path + 'register-user', { username: this.username, email: this.email, password: this.password, role: 'user' }, { headers: { 'Access-Control-Allow-Origin': '*' } })
                    .then(response => {
                        console.log('Operation successful (Register) :', response.data);
                    }).catch(error => {
                        console.error('Operation error(Register) :', error.response.data.error);
                    });
            }
        },
    },
};
</script>


<style scoped>
.auth-component {
    border: 1px solid #ccc;
    border-radius: 25px;
    max-width: 630px;
    margin: 50px auto 0 auto;
    box-shadow: 0 0 50px rgba(255, 255, 255, 0.1);
}

.page-title {
    margin-top: 40px;
    margin-bottom: 40px;
}

.role-switcher {
    max-width: 630px;
    margin: 0 auto;
    height: 80px;
}

.user-role-button {
    flex: 1;
    border-radius: 25px 0 0 0;
    font-size: x-large;
    color: #42b883;
    background-color: #242424;
    border: 1px solid transparent;
}

.creator-role-button {
    flex: 1;
    border-radius: 0 25px 0 25px;
    font-size: x-large;
    color: white;
    background-color: #242424;
    border: 1px solid;
    border-color: transparent transparent #ccc #ccc;
    position: relative;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.1) inset;
}

.login-container {
    max-width: auto;
    padding-top: 20px;
    padding-bottom: 50px;
    padding-left: 90px;
    padding-right: 90px;

}

.toggle-container {
    display: flex;
    justify-content: center;
    align-items: center;
}

.input {
    margin-bottom: 40px;
    height: 50px;
    border-radius: 20px;
    font-size: medium;
    border-color: #42b883;
    padding-left: 15px;
}

.input-label {
    font-size: large;
    align-self: start;
    margin-bottom: 10px;
}

.switcher {
    --toggle-width: 8rem;
    --toggle-height: 2.3rem;
    --toggle-font-size: 1rem;
    align-items: center;
    margin-left: 15px;
}

form {
    display: flex;
    flex-direction: column;
}

label {
    margin-bottom: 5px;
}

.warning-text {
    color: red;
}

.submit-button {
    padding: 10px;
    height: 50px;
    margin-top: 20px;
    margin-bottom: 40px;
    background-color: #42b883;
    border-radius: 20px;
    color: white;
    border: none;
    cursor: pointer;
    font-size: medium;
}

/* Switch styles */
</style>


<style></style>