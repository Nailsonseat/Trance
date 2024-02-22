<template>
    <div>
        <div class="container mt-5">
            <h2 class="text-start display-3">Trance Creator Studio</h2>
            <div class="functionality-section mt-4">
                <div class="container-fluid">
                    <div class="row">
                        <div class="col-md-4 mb-3 mx-auto">
                            <div class="custom-container mt-5 d-flex flex-column justify-content-end">
                                <div class="w-100 h-100">
                                    <span class="fs-1">Total Songs {{ this.songs.length }}</span>
                                </div>
                                <button @click="toggleAddSongModal" class="btn btn-success btn-block">
                                    Add a Song
                                </button>
                                <button @click="createSong" class="btn btn-success btn-block">
                                    Edit Songs
                                </button>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3 mx-auto">
                            <div class="custom-container mt-5 d-flex flex-column justify-content-end">
                                <div class="w-100 h-100">
                                    <span class="fs-1">Total Songs {{ this.songs.length }}</span>
                                </div>
                                <button @click="toggleAddAlbumModal" class="btn btn-warning btn-block">
                                    Add an Album
                                </button>
                                <button @click="editSong" class="btn btn-warning btn-block">
                                    Edit Albums
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <Modal @close="toggleAddSongModal" :modalActive="addSongModalActive">
            <AddSongForm @close-modal="toggleAddSongModal" ref="addSongFormRef">
            </AddSongForm>
        </Modal>

        <Modal @close="toggleEditSongModal" :modalActive="editSongModalActive">
            <EditSongForm @close-modal="toggleEditSongModal" :songToEdit="songToEdit" ref="editSongFormRef"></EditSongForm>
        </Modal>

        <Modal @close="toggleAddAlbumModal" :modalActive="addAlbumModalActive">
            <AddAlbumForm @close-modal="toggleAddAlbumModal" ref="addAlbumFormRef">
            </AddAlbumForm>
        </Modal>

        <Modal v-if="albumToEdit != null" @close="toggleAssignAlbumModal" :modalActive="assignAlbumModalActive">
            <AssignAlbumForm @close-modal="toggleAssignAlbumModal" ref="assignAlbumFormRef" :songs="songs"
                :album-id="albumToEdit">
            </AssignAlbumForm>
        </Modal>

        <div
            style="width: 90%; height: 1000px; border: 1px solid #ffffff; margin: 100px; border-radius: 20px; position: relative;">

            <!-- Navbar-like layout -->
            <div
                style="display: flex; padding: 20px; background-color: #333; border-top-left-radius: 20px; border-top-right-radius: 20px; color: #fff;">
                <button v-if="false" style="margin-right: auto;">Sort By</button>
                <div class="d-flex flex-row">
                    <button @click="showAlbums = false" style="margin-right: 10px;">Songs</button>
                    <button @click="showAlbums = true">Albums</button>
                </div>
                <!-- Add other navbar items if needed -->
            </div>

            <!-- Song List -->
            <div v-if="songs != null" style="padding: 20px">

                <div v-if="showAlbums">
                    <div v-for="album in albums" :key="album.id" class="song-item d-flex border">
                        <!-- Cover Pic -->
                        <img :src="album.coverpath" alt="Cover" class="cover-pic align-self-center ms-3" />

                        <!-- Song Details -->
                        <div class="song-details d-flex align-items-center">
                            <!-- Song Name -->
                            <h3>{{ album.title }}</h3>

                            <!-- Album -->
                            <p>{{ album.album }}</p>

                            <!-- Duration -->
                            <p class="mx-3">
                                {{ album.total_hours > 0 ? album.total_hours + 'h ' : '' }} {{ album.total_minutes > 0 ?
                                    album.total_minutes +
                                    'm '
                                    : '' }} {{ album.total_seconds > 0 ? album.total_seconds + 's' : '' }}
                            </p>
                            <div class="ms-auto">
                                <button @click="toggleAssignAlbumModal(album.id)" class="btn btn-info me-3">
                                    <i class="bi bi-pencil"></i>
                                </button>
                                <!-- Delete Button -->
                                <button @click="deleteAlbum(album.id)" class="delete-button me-3">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else v-for="song in songs" :key="song.id" class="song-item d-flex border">
                    <!-- Cover Pic -->
                    <img :src="song.coverpath" alt="Cover" class="cover-pic align-self-center ms-3" />

                    <!-- Song Details -->
                    <div class="song-details d-flex align-items-center">
                        <!-- Song Name -->
                        <h3>{{ song.title }}</h3>

                        <!-- Album -->
                        <p>{{ song.album }}</p>

                        <div class="ms-auto">
                            <button @click="toggleEditSongModal(song)" class="btn btn-info me-3">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <!-- Delete Button -->
                            <button @click="deleteSong(song.id)" class="delete-button me-3">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Rest of your content goes here -->

        </div>


    </div>
</template>

<script>
import Modal from "../../components/Modal.vue";
import AddSongForm from '../../components/songs/AddSongForm.vue';
import EditSongForm from '../../components/songs/EditSongForm.vue';
import AddAlbumForm from '../../components/albums/AddAlbumForm.vue';
import AssignAlbumForm from '../../components/albums/AssignAlbumForm.vue';
import { ref } from "vue";
import axios from 'axios'
import VuePictureCropper, { cropper } from 'vue-picture-cropper'
import VueMultiselect from 'vue-multiselect'


export default {
    data() {
        return {
            albumTitle: '',
            albumSelectionResponse: null,
            isAlbumCoverSelected: false,
            albumCoverSizeExceeded: false,
            albumCover: null,
            albumCoverUploaderOptions: {
                target: '//localhost:5000/albums/upload',
                testChunks: false,
                accept: 'image/*',
                singleFile: true,
            },
            songs: [],
            albums: [],
            songToEdit: null,
            albumToEdit: null,
            playListToEdit: null,

            selected: null,
            showAlbums: false,
        };
    },
    components: {
        Modal,
        VuePictureCropper,
        AddSongForm,
        EditSongForm,
        AddAlbumForm,
        VueMultiselect,
        AssignAlbumForm,
    },
    beforeMount() {
        this.fetchMusicList();
        this.fetchAlbumList();
    },
    setup() {
        const addSongModalActive = ref(null);
        const editSongModalActive = ref(null);
        const addAlbumModalActive = ref(null);
        const assignAlbumModalActive = ref(null);
        return { addSongModalActive, addAlbumModalActive, editSongModalActive, assignAlbumModalActive };
    },
    methods: {
        toggleAssignAlbumModal(id) {
            console.log(id);
            this.albumToEdit = id;
            this.assignAlbumModalActive = !this.assignAlbumModalActive;
            if (!this.assignAlbumModalActive) {
                this.albumToEdit = null;
                this.fetchAlbumList();
            } else {
                this.fetchMusicList();
            }
        },
        toggleAddSongModal() {
            this.addSongModalActive = !this.addSongModalActive;
            if (!this.addSongModalActive) {
                this.fetchMusicList();
            }
        },
        toggleEditSongModal(song = null) {
            this.editSongModalActive = !this.editSongModalActive;
            if (!this.editSongModalActive) {
                this.songToEdit = null;
                this.fetchMusicList();
            } else {
                this.songToEdit = song;
            }
        },
        toggleAddAlbumModal() {
            this.addAlbumModalActive = !this.addAlbumModalActive;
            if (!this.addAlbumModalActive) {
                this.fetchAlbumList();
            }
        },
        fetchMusicList() {
            const API_ENDPOINT = 'http://localhost:5000/';
            // Make an API request to fetch songs
            axios.get(API_ENDPOINT + 'songs')  // Update the URL as per your actual API endpoint
                .then(response => {
                    this.songs = response.data;
                    for (const element of this.songs) {
                        if (element.coverpath == null)
                            element.coverpath = "../src/assets/placeholder.webp"
                    }
                })
                .catch(error => {
                    console.error('Error fetching songs:', error);
                });
        },
        fetchAlbumList() {
            const API_ENDPOINT = 'http://localhost:5000/';
            // Make an API request to fetch songs
            axios.get(API_ENDPOINT + 'albums')  // Update the URL as per your actual API endpoint
                .then(response => {
                    this.albums = response.data;
                    for (const element of this.albums) {
                        if (element.coverpath == null)
                            element.coverpath = "../src/assets/placeholder.webp"
                    }
                    console.log(this.albums);
                })
                .catch(error => {
                    console.error('Error fetching albums:', error);
                });
        },
        deleteSong(songId) {
            axios.delete(`http://localhost:5000/songs/${songId}/manage`)
                .then(response => {
                    if (response.status === 200) {
                        // Assuming you have a way to update the list of songs in your component
                        this.fetchMusicList();
                        console.log('Song deleted successfully');
                    } else {
                        console.error('Failed to delete song:', response.data.message);
                    }
                })
                .catch(error => {
                    console.error('Error deleting song:', error.message);
                });
        },
        deleteAlbum(albumId) {
            axios.delete(`http://localhost:5000/albums/${albumId}/manage`)
                .then(response => {
                    if (response.status === 200) {
                        // Assuming you have a way to update the list of songs in your component
                        this.fetchAlbumList();
                        console.log('Album deleted successfully');
                    } else {
                        console.error('Failed to delete album:', response.data.message);
                    }
                })
                .catch(error => {
                    console.error('Error deleting album:', error.message);
                });
        },
    },
};
</script>



<style scoped>
.song-item {
    height: 90px;
    margin-bottom: 10px;
    border-radius: 12px;
}

.cover-pic {
    width: 60px;
    height: 60px;
    margin-right: 20px;
}

.song-details {
    flex: 1;
}

.delete-button {
    background-color: red;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 5px;
}

.drop-zone {
    width: 200px;
    height: 200px;
    border: 2px dashed #ccc;
    padding-right: 0%;
    border-radius: 5px;
    align-self: center;
}

.cover-image-viewer {}

.modal-dialog {}

.modal-content {
    margin: auto;
    background-color: #242424;
    border: 2px solid #ffffff;
    border-radius: 15px;
    height: 900px;
    width: 1200px;
}

/* Add any other styling you need for the modal */
.modal-left-section,
.modal-right-section {
    /* Add your specific styles for left and right sections if needed */
}

.custom-container {
    border: 2px solid #fff;
    /* White solid border */
    border-radius: 15px;
    /* Border radius of 15px */
    padding: 20px;
    /* Add padding for content inside the container */
    width: 400px;
    height: 400px;
}

.functionality-section {
    margin-top: 20px;
}



.container {}

.btn {
    margin-bottom: 10px;
}

.test {
    background-color: aqua;
    color: black;
    text-decoration: #242424;
}
</style>
