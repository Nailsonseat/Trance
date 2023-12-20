<template>
    <div>
        <div class="container-fluid">
            <div style="background-color: black;">
                <div class="row">
                    <div class="col-3 d-flex" style="height: 800px; background-color: teal">
                        <draggable class="dragArea list-group w-100" :list="audioList" group="queue">
                            <div class="list-group-item bg-gray-300 m-1 mt-3 p-3 rounded-md text-center"
                                v-for="element in audioList" :key="element.name">
                                <span class="w-100">{{ element.name }}</span>
                            </div>
                        </draggable>
                    </div>
                    <div class="col d-flex flex-column">
                        <div class="mb-auto d-flex w-100" style="padding: 20px; background-color: #333;color: #fff;">
                            <div class="btn-group me-auto">
                                <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                                    aria-expanded="false">
                                    Filter by
                                </button>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" @click="filterFunction('title')">Name</a></li>
                                    <li><a class="dropdown-item" @click="filterFunction('artist')">Artist</a></li>
                                    <li><a class="dropdown-item" @click="filterFunction('artist')">Likes</a></li>
                                </ul>
                            </div>

                            <div v-if="pane === 'playlists'" class="d-flex me-3"><button @click="toggleAddPlaylistModal"
                                    class="btn btn-success">Add
                                    Playlist</button>
                            </div>

                            <div class="d-flex flex-row">
                                <button @click="switchToPane('music')" class="me-3">Songs</button>
                                <button @click="switchToPane('playlists')" class="me-3">Playlists</button>
                                <button @click="switchToPane('albums')" class="me-3">Albums</button>
                            </div>

                            <form class="d-flex" role="search">
                                <input class="form-control me-2" type="search" :placeholder="'Search by ' + searchBy"
                                    aria-label="Search">
                                <!-- Example split danger button -->
                                <div class="btn-group">
                                    <button type="button" class="btn btn-info">Search</button>
                                    <button type="button" class="btn btn-info dropdown-toggle dropdown-toggle-split"
                                        data-bs-toggle="dropdown" aria-expanded="false">
                                        <span class="visually-hidden">Toggle Dropdown</span>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><button @click="searchByChange('Title')"
                                                class="w-100 bg-white text-dark">Title</button></li>
                                        <li><button @click="searchByChange('Artist')"
                                                class="w-100 bg-white text-dark">Artist</button></li>
                                        <li><button @click="searchByChange('Genre')"
                                                class="w-100 bg-white text-dark">Genre</button></li>
                                    </ul>
                                </div>

                            </form>

                        </div>

                        <!-- Flexible section _-->
                        <div v-if="pane === 'music'" class="mb-auto h-100">

                            <Modal @close="togglePlaylistModal" :modalActive="isPlaylistModalActive">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title">Manage Playlists</h5>
                                            <button type="button" class="btn-close" @click="togglePlaylistModal"
                                                aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div v-for="playlist in playlists" :key="playlist.id">
                                                <label>
                                                    <input type="checkbox" v-model="selectedPlaylists"
                                                        :value="playlist.id" />
                                                    {{ playlist.name }}
                                                </label>
                                            </div>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary"
                                                @click="togglePlaylistModal">Close</button>
                                            <button type="button" class="btn btn-primary" @click="updateSongPlaylists">Save
                                                Changes</button>
                                        </div>
                                    </div>
                                </div>
                            </Modal>
                            <div v-for="song in filteredSongs" :key="song.id" class="song-item d-flex border ">
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
                                        {{ song.hours > 0 ? song.hours + 'h ' : '' }} {{ song.minutes }}m {{ song.seconds
                                        }}s
                                    </p>

                                    <button @click="togglePlaylistModal(song)" class="btn btn-info ms-auto me-3">
                                        <i class="bi bi-music-note-list"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div v-else>
                            <Modal @close="toggleAddPlaylistModal" :modalActive="addPlaylistModalActive">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title text-black">Create New Playlist</h5>
                                            <button type="button" class="btn-close" @click="toggleAddPlaylistModal"
                                                aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="mb-3">
                                                <label for="newPlaylistName" class="form-label text-black">Playlist
                                                    Name</label>
                                                <input type="text" class="form-control" id="newPlaylistName"
                                                    v-model="newPlaylistName" />
                                            </div>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary"
                                                @click="toggleAddPlaylistModal">Close</button>
                                            <button type="button" class="btn btn-primary"
                                                @click="createNewPlaylist(newPlaylistName)">Create
                                                Playlist</button>
                                        </div>
                                    </div>
                                </div>
                            </Modal>
                            <div v-for="playlist in playlists" :key="playlist.id" class="playlist-item d-flex border ">
                                <!-- Playlist Details -->
                                <div class="playlist-details d-flex align-items-center">
                                    <h3>{{ playlist.name }}</h3>
                                    <p>Created at: {{ formatCreatedAt(playlist.created_at) }}</p>
                                </div>
                            </div>
                        </div>



                    </div>
                </div>
            </div>
        </div>



        <!-- Audio Player -->
        <div class="audio-player">
            <audio-player ref="audioPlayer" :audio-list="audioList.map(elm => elm.url)" theme-color="#42b883"
                v-model:shuffleOn="shuffleOn" />
        </div>
    </div>
</template>



<script>
import AudioPlayer from '@liripeng/vue-audio-player'
import axios from 'axios';
import { VueDraggableNext } from 'vue-draggable-next';
import Modal from "../components/Modal.vue";

export default {
    // Your component logic goes here
    components: {
        AudioPlayer,
        draggable: VueDraggableNext,
        Modal
    },
    data() {
        return {
            currentAudioName: '',
            songs: [],
            audioList: [],
            filteredSongs: [], // For music section filtering
            shuffleOn: false,
            sortBy: 'title', // Initial sort criteria
            searchBy: 'title',
            pane: 'music',
            playlists: [],
            addPlaylistModalActive: false,
            isPlaylistModalActive: false,
            newPlaylistName: '',
        };
    },
    beforeMount() {
        this.updateMusicList();
        this.updatePlaylistList();
    },
        updateMusicList() {
            // Update URL as per your actual API endpoint
            axios.get('http://localhost:5000/songs')
                .then(response => {
                    this.songs = response.data;
                    this.filteredSongs = this.songs.slice(); // Initial filtered list is all songs
                    this.audioList = this.generateAudioList(); // Generate initial audio list
                })
                .catch(error => {
                    console.error('Error fetching songs:', error);
                });
        },
        updatePlaylistList() {
            axios.get('http://localhost:5000/playlists')
                .then(response => {
                    this.playlists = response.data;
                })
                .catch(error => {
                    console.error('Error fetching playlists:', error);
                });
        },
};
</script>

<style scoped>
/* Your component-specific styles go here */

.audio-player {
    position: fixed;
    bottom: 0;
    padding-right: 20px;
    padding-top: 20px;
    width: 98.5%;
    height: 120px;
    background-color: #242424;
    text-align: center;
    box-shadow: 0px -5px 5px rgba(0, 0, 0, 0.1);
}

span {
    display: inline-block;
    vertical-align: middle;
    line-height: normal;
}
</style>
