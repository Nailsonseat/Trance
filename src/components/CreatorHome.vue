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
                                <button @click="editSong" class="btn btn-warning btn-block">
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


        <Modal @close="toggleAlbumModal" :modalActive="albumModalActive">
            <!-- Modal Content for Adding an Album -->
            <div class="position-absolute top-50 start-50 translate-middle modal-content">
                <!-- Modal Header -->
                <div class="modal-header">
                    <h5 class="modal-title fs-4">Add an Album</h5>
                    <button type="button" class="close" @click="toggleAlbumModal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <!-- Modal Body -->
                <div class="modal-body">
                    <!-- Add your fields (title, cover, etc.) component or content here -->
                    <label class="py-3" for="albumTitle">Album Name:</label>
                    <input type="text" id="albumTitle" v-model="albumTitle" class="form-control bg-transparent text-white">

                    <label class="py-3" for="albumCover">Upload Album Cover:</label>
                    <!-- Add your upload album cover image components here -->
                    <!-- Similar to how it's done for adding a song's cover -->

                    <uploader ref="albumCoverUploaderRef" :options="albumCoverUploaderOptions" :autoStart="false"
                        class="drop-zone" :style="{ 'padding-right': isAlbumCoverSelected ? '28px' : '0' }"
                        @file-added="onAlbumCoverAdded" @file-success="onAlbumCoverSuccess"
                        @files-submitted="onAlbumCoverSubmitted" @file-error="onAlbumCoverError">
                        <!-- Similar structure to the one in the song modal -->
                                </uploader>

                    <div v-if="isAlbumCoverSelected">
                        <img class="drop-zone" :src="albumCover" alt="Album Cover Preview">
                    </div>
                                </div>
                <!-- Modal Footer -->
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" @click="uploadAlbumCover">Add Album</button>
                    <button type="button" class="btn btn-primary" @click="toggleAlbumModal">Close</button>
                                </div>
                            </div>
        </Modal>




        <div
            style="width: 90%; height: 1000px; border: 1px solid #ffffff; margin: 100px; border-radius: 20px; position: relative;">

            <!-- Navbar-like layout -->
            <div
                style="display: flex; padding: 20px; background-color: #333; border-top-left-radius: 20px; border-top-right-radius: 20px; color: #fff;">
                <button style="margin-right: auto;">Sort By</button>
                <div class="d-flex flex-row">
                    <button style="margin-right: 10px;">Songs</button>
                    <button>Albums</button>
                                    </div>
                <!-- Add other navbar items if needed -->
                                    </div>

            <!-- Song List -->
            <div v-if="songs != null" style="padding: 20px">
                <div v-for="song in songs" :key="song.id" class="song-item d-flex border">
                    <!-- Cover Pic -->
                    <img :src="song.coverpath" alt="Cover" class="cover-pic align-self-center ms-3" />

                    <!-- Song Details -->
                    <div class="song-details d-flex align-items-center">
                        <!-- Song Name -->
                        <h3>{{ song.title }}</h3>

                        <!-- Album -->
                        <p>{{ song.album }}</p>

                        <!-- Duration -->
                        <p class="mx-3">
                            {{ song.hours > 0 ? song.hours + 'h ' : '' }} {{ song.minutes }}m {{ song.seconds }}s
                        </p>
                        <div class="ms-auto">
                            <button @click="editSong(song)" class="btn btn-info me-3">
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
import Modal from "../components/Modal.vue";
import AddSongForm from '../components/AddSongForm.vue';
import EditSongForm from '../components/EditSongForm.vue';
import { ref } from "vue";
import axios from 'axios'
import VuePictureCropper, { cropper } from 'vue-picture-cropper'


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
            songToEdit: null
        };
    },
    components: {
        Modal,
        VuePictureCropper,
        AddSongForm,
        EditSongForm
    },
    beforeMount() {
        this.fetchMusicList();
    },
    setup() {
        const modalActive = ref(null);

        const toggleModal = () => {
            modalActive.value = !modalActive.value;
        };
        const musicUploaderRef = ref(null)
        const coverUploaderRef = ref(null)
        onMounted(() => {
            nextTick(() => {
                window.wwwwuploader = musicUploaderRef.uploader
                window.coverUploader = coverUploaderRef.uploader
            })
        });
        return { modalActive, toggleModal, musicUploaderRef, coverUploaderRef };
    },
    methods: {
        fetchMusicList() {
            const API_ENDPOINT = 'http://localhost:5000/';
            // Make an API request to fetch songs
            axios.get(API_ENDPOINT + 'songs')  // Update the URL as per your actual API endpoint
                .then(response => {
                    this.songs = response.data;
                })
                .catch(error => {
                    console.error('Error fetching songs:', error);
                });
        },


        onAlbumCoverAdded(file) {
            if (file.size > 20 * 1024 * 1024) {
                this.albumCoverSizeExceeded = true;
                file.ignored = true;
            } else {
                this.albumCoverSizeExceeded = false;
                // This method will be called when an album cover image file is added
                console.log('Album Cover file added:', file);
            }
        },
        onAlbumCoverSubmitted(files, fileList, event) {
            if (!this.albumCoverSizeExceeded) {
                this.isAlbumCoverSelected = !this.isAlbumCoverSelected;
            }
        },
        onAlbumCoverSuccess(rootFile, file, message, chunk) {
            this.albumSelectionResponse = JSON.parse(message);
            // Additional logic if needed
        },
        onAlbumCoverError(rootFile, file, message, chunk) {
            console.log('Error uploading album cover:', message);
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

.close {
    border: 1px solid #fff;
    background-color: red;
}

.container {}

.btn {
    margin-bottom: 10px;
}
</style>
