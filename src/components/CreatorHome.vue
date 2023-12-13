<script>
import Modal from "../components/Modal.vue";
import { ref, onMounted, nextTick } from "vue";
import VuePictureCropper, { cropper } from 'vue-picture-cropper'


export default {
    data() {
        return {
            songTitle: '',
            songLyrics: '',
            selectedCover: null,
            selectedMusic: '',
            uploadStatus: '',
            musicSizeExceeded: false,
            headers: {
                'Content-type': 'audio/mpeg',
                'Accept': 'audio/mpeg'
            },
            isMusicSelected: false,
            musicUploaderOptions: {
                target: '//localhost:5000/songs/upload',
                testChunks: false,
                chunkSize: 1 * 1024 * 1024 * 20,
                accept: 'audio/*',
                singleFile: true,
                maxSize: 90 * 1024,
            },

            isCoverSelected: false,
            coverSizeExceeded: false,
            coverUploaderOptions: {
                target: '//localhost:5000/covers/upload',
                testChunks: false,
                chunkSize: 1 * 1024 * 1024 * 20,
                accept: 'image/*',
                singleFile: true,
                maxSize: 20 * 1024 * 1024,
            },
            cover: null,
            textInput: '',
            genres: [],
        };
    },
    components: {
        Modal,
        VuePictureCropper,
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
                window.uploader = musicUploaderRef.uploader
                window.coverUploader = coverUploaderRef.uploader
            })
        });
        return { modalActive, toggleModal, musicUploaderRef, coverUploaderRef };
    },
    methods: {
        onMusicAdded(file) {
            if (file.size > 20 * 1024 * 1024) {
                this.musicSizeExceeded = true;
            } else {
                this.musicSizeExceeded = false;
                // This method will be called when a file is added
                console.log('File added:', file);
            }
        },
        onMusicSubmitted(files, fileList, event) {
            if (!this.musicSizeExceeded) {
                this.isMusicSelected = !this.isMusicSelected;
            }
        },
        onCoverAdded(file) {
            if (file.size > 20 * 1024 * 1024) {
                this.coverSizeExceeded = true;
            } else {
                this.coverSizeExceeded = false;

                // This method will be called when a cover image file is added
                console.log('Cover file added:', file);
            }
        },
        onCoverSubmitted(files, fileList, event) {
            if (!this.coverSizeExceeded) {
                this.cover = URL.createObjectURL(files[0].file)
                this.isCoverSelected = !this.isCoverSelected;
            }
        },
        addChip() {
            if (this.textInput.trim() !== '') {
                this.genres.push(this.textInput.trim());
                this.textInput = '';
            }
        },
        removeChip(index) {
            this.genres.splice(index, 1);
        },
        getColorClass(index) {
            const colorClasses = ['bg-primary', 'bg-secondary', 'bg-success', 'bg-danger', 'bg-warning', 'bg-info', 'bg-light'];
            const colorIndex = index % colorClasses.length;
            return `text-${colorClasses[colorIndex]}`;
        },
        uploadMedia(file) {
            const musicUploader = this.musicUploaderRef.uploader
            const coverUploader = this.coverUploaderRef.uploader
            musicUploader.upload()
            coverUploader.upload()
        },
        onMusicSuccess(rootFile, file, message, chunk) {
            console.log("Message", message);
        },
        onMusicError(rootFile, file, message, chunk) {
            console.log("Message", message);
        },
        onCoverSuccess(rootFile, file, message, chunk) {
            console.log("Message", message);
        },
        onCoverError(rootFile, file, message, chunk) {
            console.log("Message", message);
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
