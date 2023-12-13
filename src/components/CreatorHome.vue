<template>
    <div>
        <div class="container mt-5">
            <h2 class="text-start display-4">Trance Creator Studio</h2>
            <div class="functionality-section mt-4">
                <div class="container-fluid">
                    <div class="row">
                        <div class="col-md-4 mb-3 mx-auto">
                            <div class="custom-container mt-5 d-flex flex-column justify-content-end">
                                <div class="w-100 h-100">
                                    <span style="font-size: large;">Total Songs</span>
                                </div>
                                <button @click="toggleModal" class="btn btn-success btn-block">
                                    Add a Song
                                </button>
                                <button @click="createSong" class="btn btn-success btn-block">
                                    Edit Songs
                                </button>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3 mx-auto">
                            <div class="custom-container mt-5 d-flex flex-column justify-content-end">
                                <span>Total albums</span>
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

        <Modal @close="toggleModal" :modalActive="modalActive">
            <div class="position-absolute top-50 start-50 translate-middle modal-content">
                <!-- Modal Header -->
                <div class="modal-header">
                    <h5 class="modal-title fs-4">Add a Song</h5>
                    <button type="button" class="close" @click="toggleModal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <!-- Modal Body -->
                <div class="modal-body">
                    <div class="row h-100">

                        <!-- Left section for upload song and cover pic -->
                        <div class="col w-50" style="border-right: 1px solid #ffffff;">
                            <div class="modal-left-section d-flex flex-column justify-content-center h-100">
                                <!-- Add your upload song and cover pic components or content here -->
                                <label class="my-4 fs-4" for="songFile">Upload Song:</label>

                                <uploader ref="musicUploaderRef" :options="musicUploaderOptions" :autoStart="false"
                                    class="drop-zone d-flex flex-column flex-column align-items-center justify-content-center"
                                    :style="{ 'padding-right': isMusicSelected ? '28px' : '0' }" @file-added="onMusicAdded"
                                    @file-success="onMusicSuccess" @files-submitted="onMusicSubmitted"
                                    @file-error="onMusicError">
                                    <uploader-drop v-if="!isMusicSelected"
                                        class="d-flex h-100 w-100 flex-column align-items-center justify-content-center">
                                        <span>Drop mp3 file</span>
                                        <span class="my-1">Or</span>
                                        <uploader-btn class="btn btn-outline-light">Select MP3 file</uploader-btn>
                                    </uploader-drop>
                                    <uploader-list v-show="!musicSizeExceeded"></uploader-list>
                                    <span v-show="musicSizeExceeded">Maximum file size allowed 20mb</span>
                                </uploader>

                                <label class="my-4 fs-4" for="coverPic">Upload Cover Picture:</label>

                                <!-- Add your upload cover image components here -->
                                <uploader ref="coverUploaderRef" :options="coverUploaderOptions" :autoStart="false"
                                    class="drop-zone d-flex flex-column flex-column align-items-center justify-content-center"
                                    :style="{ 'padding-right': isCoverSelected ? '28px' : '0' }" @file-added="onCoverAdded"
                                    @file-success="onCoverSuccess" @files-submitted="onCoverSubmitted"
                                    @file-error="onCoverError" v-if="!isCoverSelected">
                                    <uploader-drop
                                        class="d-flex h-100 w-100 flex-column align-items-center justify-content-center">
                                        <span>Drop image file</span>
                                        <span class="my-1">Or</span>
                                        <uploader-btn class="btn btn-outline-light">Select image file</uploader-btn>
                                    </uploader-drop>
                                    <uploader-list v-show="!coverSizeExceeded"></uploader-list>
                                    <span v-show="coverSizeExceeded">Maximum file size allowed 20mb</span>
                                </uploader>
                                <div v-if="isCoverSelected">
                                    <img class="drop-zone" :src="cover" alt="Hello">
                                </div>
                            </div>
                        </div>

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
        ready() {
            console.log("Ready event");
        }
    },
};
</script>

<style scoped>
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

onMusicAdded(file) {
    if (file.size > 20 * 1024 * 1024) {
        this.musicSizeExceeded=true;
    }

    else {
        this.musicSizeExceeded=false;
        // This method will be called when a file is added
        console.log('File added:', file);
    }
}

,
onMusicSubmitted(files, fileList, event) {
    if ( !this.musicSizeExceeded) {
        this.isMusicSelected= !this.isMusicSelected;
    }
}

,
.close {
    border: 1px solid #fff;
    background-color: red;
}

.container {}

.btn {
    margin-bottom: 10px;
}
</style>
