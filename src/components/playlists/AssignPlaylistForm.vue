<template>
    <div class="position-absolute top-50 start-50 translate-middle modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
            <h5 class="modal-title fs-4 text-dark">Assign Songs to Playlist</h5>
            <button type="button" class="close" @click="closeModal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>


        <div class="modal-body">
            <!-- Add your upload song and cover pic components or content here -->

            <label class="my-4 fs-4 text-black" for="coverPic">Update Playlist</label>

            <VueMultiselect v-model="selectedSongs" :options="songs" :multiple="true"
                placeholder="Select Songs to add to playlist" label="title" track-by="title" :allow-empty="true" />

        </div>


        <!-- Modal Footer -->
        <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="updatePlaylist">Update
                Playlist</button>
            <button type="button" class="btn btn-primary" @click="closeModal">Close</button>
        </div>
    </div>
</template>



<script>
import axios from 'axios';
import VueMultiselect from 'vue-multiselect'

export default {

    data() {
        return {
            selectedSongs: [],
        }
    },
    components: {
        VueMultiselect
    },
    beforeMount() {
        this.fetchPlaylistSongs(this.playlistId);
    },
    methods: {
        updatePlaylist() {
            let songIds = this.selectedSongs.map(song => song.id);
            const API_ENDPOINT = 'http://localhost:5000/';
            axios.put(API_ENDPOINT + `playlist/${this.playlistId}/assign`, { song_ids: songIds })
                .then(response => {
                    console.log('Playlist songs updated successfully:', response.data);
                    this.closeModal();
                })
                .catch(error => {
                    console.error('Error updating playist songs:', error);
                });
        },
        fetchPlaylistSongs(playlistId) {
            const API_ENDPOINT = 'http://localhost:5000/';
            axios.get(API_ENDPOINT + `playlist/${this.playlistId}/assign`)
                .then(response => {
                    console.log('Playlist songs fetched successfully:', response.data);
                    const songIds = response.data.song_ids;
                    this.selectedSongs = this.songs.filter(song => songIds.includes(song.id));
                })
                .catch(error => {
                    console.error('Error fetching playlist songs:', error);
                });
        },
        closeModal() {
            this.selectedSongs = []
            this.$emit('close-modal');
        },
    },
    props: {
        songs: {
            type: Object,
            required: true
        },
        playlistId: {
            type: Number,
            NonNullable: false,
            required: true
        }
    }


}
</script>



<style src="vue-multiselect/dist/vue-multiselect.css"></style>
<style scoped>
.multiselect__tag {
    background: #74a93c;
}

.multiselect__option--highlight {
    background: #74a93c;
}

.multiselect__option--highlight:after {
    background: #74a93c;
}

.multiselect__option--selected.multiselect__option--highlight {
    background: #798b91;
}

.multiselect__option--selected.multiselect__option--highlight:after {
    background: #798b91;
}

.multiselect__tag-icon:hover {
    background: #74a93c;
}

.multiselect__input,
.multiselect__single {
    padding: 0 0 0 0;
}

.multiselect__placeholder {
    margin-left: 4px;
    color: #999999;
}


.drop-zone {
    width: 200px;
    height: 200px;
    border: 2px dashed #ccc;
    padding-right: 0%;
    border-radius: 5px;
    align-self: center;
}

.clear-button {
    width: 200px;
    align-self: center;
}


.close {
    border: 1px solid #fff;
    background-color: red;
}
</style>

