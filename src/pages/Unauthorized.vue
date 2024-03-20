<template>
    <div class="unauthorized">
        <h1>Unauthorized</h1>
        <p>You are not authorized to access this page.</p>
    </div>
</template>

<style scoped>
.unauthorized {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    font-family: Arial, sans-serif;
}

h1 {
    font-size: 24px;
    margin-bottom: 10px;
}

p {
    font-size: 16px;
    color: #888;
}
</style>