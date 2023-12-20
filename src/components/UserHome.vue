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
    methods: {
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
        generateAudioList() {
            let audioList = this.songs.map(song => ({
                name: song.title,
                url: song.filepath,
            }));

            if (this.shuffleOn) {
                const currentIndex = audioList.findIndex(song => song.name === this.currentAudioName);
                const shuffledSongs = [...audioList.slice(currentIndex + 1), ...audioList.slice(0, currentIndex + 1)];
                audioList = [...audioList.slice(0, currentIndex + 1), ...shuffledSongs];
            }

            return audioList;
        },
        removeFromQueue(item) {
            // Remove item from both audioList and `queue` draggable group
            this.audioList.splice(this.audioList.indexOf(item), 1);
            draggable.removeFromGroup('queue', item);
        },
        filterFunction(value) {
            this.sortBy = value;
            // Update filteredSongs based on chosen criteria (adjust logic based on your data structure)
            this.filteredSongs = this.songs.slice().sort((a, b) => {
                if (value === 'title') return a.title.localeCompare(b.title);
                else if (value === 'artist') return a.artist.localeCompare(b.artist);
                // Add logic for other sort criteria
            });
        },
        searchByChange(value) {
            this.searchBy = value.toLowerCase();

            // logic
        },

        switchToPane(value) {
            if (value === 'music') {
                this.pane = value;
                this.updateMusicList();
            } else if (value == 'playlists') {
                this.pane = value;
                this.updatePlaylistList();
            } else if (value == 'albums') { }
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
        createNewPlaylist(name) {
            // Implement logic to create a new playlist
            if (name) {
                axios.post('http://localhost:5000/playlist/create', {
                    name: name,
                    songs: [],  // You may provide an initial list of song IDs if needed
                })
                    .then(response => {
                        console.log(response)
                        //this.playlists.push(response.data);
                        alert('Playlist created successfully!');
                    })
                    .catch(error => {
                        console.error('Error creating playlist:', error);
                        alert('Error creating playlist. Please try again.');
                    });
            }
        },
        updateSongPlaylists() {
            // Update the playlists for the current song on the server
            const selectedPlaylists = this.selectedPlaylists.map(id => ({ id }));
            axios.put(`http://localhost:5000/playlists/${this.currentSongId}`, {
                songs_to_add: selectedPlaylists,
                songs_to_remove: this.playlists
                    .filter(playlist => !this.selectedPlaylists.includes(playlist.id))
                    .map(playlist => ({ id: playlist.id })),
            })
                .then(response => {
                    // Optionally handle the response
                    console.log('Playlists updated successfully:', response.data);
                })
                .catch(error => {
                    console.error('Error updating playlists:', error);
                })
                .finally(() => {
                    this.closePlaylistModal();
                });
        },
        formatCreatedAt(timestamp) {
            // Implement your own formatting logic
            return new Date(timestamp).toLocaleDateString();
        },
        toggleAddPlaylistModal() {
            this.addPlaylistModalActive = !this.addPlaylistModalActive;
            // Optionally, you can reset the new playlist name when closing the modal
            if (!this.addPlaylistModalActive) {
                this.newPlaylistName = '';
            }
        },
        togglePlaylistModal(song) {
            if (song) {
                this.currentSongId = song.id;
                this.selectedPlaylists = this.playlists
                    .filter(playlist => playlist.songs.some(s => s.id === song.id))
                    .map(playlist => playlist.id);
            }
            this.isPlaylistModalActive = !this.isPlaylistModalActive;
        },
    }
};
</script>

<style scoped>
/* Your component-specific styles go here */
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
