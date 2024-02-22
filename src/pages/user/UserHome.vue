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
                                <input v-model="query" class="form-control me-2" type="search"
                                    :placeholder="'Search by ' + searchBy" aria-label="Search">
                                <!-- Example split danger button -->
                                <div class="btn-group">
                                    <button type="button" class="btn btn-info">Search</button>
                                    <button type="button" class="btn btn-info dropdown-toggle dropdown-toggle-split"
                                        data-bs-toggle="dropdown" aria-expanded="false">
                                        <span class="visually-hidden">Toggle Dropdown</span>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><button @click="searchBy = 'title'"
                                                class="w-100 bg-white text-dark">Title</button></li>
                                        <li><button @click="searchBy = 'artist'"
                                                class="w-100 bg-white text-dark">Artist</button></li>
                                        <li><button @click="searchBy = 'genres'"
                                                class="w-100 bg-white text-dark">Genre</button></li>
                                    </ul>
                                </div>

                            </form>

                        </div>

                        <Modal v-if="playListToEdit != null" @close="toggleAssignPlaylistModal"
                            :modalActive="assignPlaylistModalActive">
                            <AssignPlaylistForm @close-modal="toggleAssignPlaylistModal" ref="assignPlaylistFormRef"
                                :songs="songs" :playlist-id="playListToEdit">
                            </AssignPlaylistForm>
                        </Modal>


                        <!-- Flexible section _-->
                        <div v-if="pane === 'music'" class="mb-auto h-100">

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
                        <div v-else-if="pane === 'albums'" class="mb-auto h-100">
                            <div v-for="album in albums" :key="album.id" class="song-item d-flex border ">
                                <!-- Cover Pic -->
                                <img :src="album.coverpath" alt="Cover" class="cover-pic align-self-center ms-3" />

                                <!-- Song Details -->
                                <div class="song-details d-flex align-items-center">
                                    <!-- Song Name -->
                                    <h3>{{ album.title }}</h3>

                                    <!-- Album -->
                                    <p class="ms-3">{{ album.artist }}</p>

                                    <button @click="togglePlaylistModal(album)" class="btn btn-info ms-auto me-3">
                                        <i class="bi bi-music-note-list"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div v-else class="mb-auto h-100">
                            <div v-for="playlist in playlists" :key="playlist.id" class="song-item d-flex border ">
                                <!-- Playlist Details -->

                                <div class="song-details d-flex align-items-center">
                                    <!-- Playlist Name -->
                                    <h3 class="ms-3">{{ playlist.name }}</h3>


                                    <button @click="toggleAssignPlaylistModal(playlist.id)"
                                        class="btn btn-info ms-auto me-3">
                                        <i class="bi bi-music-note-list"></i>
                                    </button>
                                </div>
                            </div>
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
import AssignPlaylistForm from '../../components/playlists/AssignPlaylistForm.vue';
import Modal from "../../components/Modal.vue";
import { ref } from "vue";

export default {
    // Your component logic goes here
    components: {
        AudioPlayer,
        draggable: VueDraggableNext,
        Modal,
        AssignPlaylistForm
    },
    setup() {
        const assignPlaylistModalActive = ref(false);

        return { assignPlaylistModalActive };
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
            query: '',

            playListToEdit: null,
        };
    },
    beforeMount() {
        this.updateMusicList();
        this.updatePlaylistList();
        this.updateAlbumList();
    },
    watch: {
        query(newVal) {
            this.filterFunction(this.sortBy);
        }
    },
    methods: {
        updateMusicList() {
            // Update URL as per your actual API endpoint
            axios.get('http://localhost:5000/songs')
                .then(response => {
                    this.songs = response.data;
                    this.filteredSongs = this.songs.slice(); // Initial filtered list is all songs
                    this.audioList = this.generateAudioList(); // Generate initial audio list

                    for (const element of this.songs) {
                        if (element.coverpath == null)
                            element.coverpath = "../src/assets/placeholder.webp"
                    }
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
        updateAlbumList() {
            const API_ENDPOINT = 'http://localhost:5000/';
            // Make an API request to fetch songs
            axios.get(API_ENDPOINT + 'albums')  // Update the URL as per your actual API endpoint
                .then(response => {
                    this.albums = response.data;
                    for (const element of this.albums) {
                        if (element.coverpath == null)
                            element.coverpath = "../src/assets/placeholder.webp"
                    }
                })
                .catch(error => {
                    console.error('Error fetching albums:', error);
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
            console.log(this.songs);
            this.sortBy = value;
            // Update filteredSongs based on chosen criteria (adjust logic based on your data structure)
            this.filteredSongs = this.songs.slice().filter(song => {
                // Check if the song matches the search criteria based on searchBy
                if (this.searchBy === 'genres') {
                    // Check if any genre matches the query
                    return song[this.searchBy].some(genre => genre.toLowerCase().includes(this.query.toLowerCase()));
                } else {
                    // Check if the value of searchBy matches the query
                    return song[this.searchBy].toLowerCase().includes(this.query.toLowerCase());
                }
            }).sort((a, b) => {
                if (value === 'title') return a.title.localeCompare(b.title);
                else if (value === 'artist') return a.artist.localeCompare(b.artist);
                // Add logic for other sort criteria
            });
        },

        switchToPane(value) {
            if (value === 'music') {
                this.pane = value;
                this.updateMusicList();
            } else if (value == 'playlists') {
                this.pane = value;
                this.updatePlaylistList();
            } else if (value == 'albums') {
                this.pane = value;
                this.updateAlbumList();

            }
        },
        createNewPlaylist(name) {
            // Implement logic to create a new playlist
            if (name) {
                axios.post('http://localhost:5000/playlist/create', {
                    name: name
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
        formatCreatedAt(timestamp) {
            // Implement your own formatting logic
            return new Date(timestamp).toLocaleDateString();
        },
        toggleAddPlaylistModal() {
            this.addPlaylistModalActive = !this.addPlaylistModalActive;
            // Optionally, you can reset the new playlist name when closing the modal
            if (!this.addPlaylistModalActive) {
                this.newPlaylistName = '';
                this.updatePlaylistList();
            }
        },
        toggleAssignPlaylistModal(id) {
            this.playListToEdit = id;
            this.assignPlaylistModalActive = !this.assignPlaylistModalActive;
            if (!this.assignPlayListModalActive) {
                this.playListToEdit = null;
                this.updatePlaylistList();
            }
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
