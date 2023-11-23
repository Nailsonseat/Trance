<script>
export default {
    methods: {
        createSong() {
            // Implement logic for creating a new song
            console.log("Creating a new song");
        },
        editSong() {
            // Implement logic for editing an existing song
            console.log("Editing an existing song");
        },
        removeSong() {
            // Implement logic for removing an existing song
            console.log("Removing an existing song");
        },
        createAlbum() {
            // Implement logic for creating a new album
            console.log("Creating a new album");
        },
        editAlbum() {
            // Implement logic for editing an existing album
            console.log("Editing an existing album");
        },
        removeAlbum() {
            // Implement logic for removing an existing album
            console.log("Removing an existing album");
        },
        assignSongToAlbum() {
            // Implement logic for assigning a song to an album
            console.log("Assigning a song to an album");
        },
    },
};
</script>

<template>
    <div>
        <h2 style="text-align: start; font-size: 45px; margin-top: 30px; margin-left: 50px;">Trance Creator Studio</h2>
        <div class="functionality-section">
            <h3>User Functionalities</h3>
            <!-- Include user functionalities here -->
            <router-link :to="{ name: 'UserAuth' }">Go to User Home</router-link>
        </div>
        <div class="functionality-section">
            <h3>Creator Functionalities</h3>
            <!-- Include creator functionalities here -->
            <button @click="createSong">Create Song</button>
            <button @click="editSong">Edit Song</button>
            <button @click="removeSong">Remove Song</button>
            <button @click="createAlbum">Create Album</button>
            <button @click="editAlbum">Edit Album</button>
            <button @click="removeAlbum">Remove Album</button>
            <button @click="assignSongToAlbum">Assign Song to Album</button>
        </div>
    </div>
</template>

<style scoped>
.functionality-section {
    margin-top: 20px;
}
</style>
