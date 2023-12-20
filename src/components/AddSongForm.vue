<template>
    <!-- Left section for upload song and cover pic -->

    <div class="position-absolute top-50 start-50 translate-middle modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
            <h5 class="modal-title fs-4">Add a Song</h5>
            <button type="button" class="close" @click="closeModal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>


        <div class="modal-body">
            <div class="row h-100">
                <div class="col w-50" style="border-right: 1px solid #ffffff;">
                    <div class="modal-left-section d-flex flex-column justify-content-center h-100">
                        <!-- Add your upload song and cover pic components or content here -->
                        <label class="my-4 fs-4" for="songFile">Upload Song:</label>

                        <uploader ref="musicUploaderRef" :options="musicUploaderOptions" :autoStart="false"
                            class="drop-zone d-flex flex-column flex-column align-items-center justify-content-center"
                            :style="{ 'padding-right': isMusicSelected ? '28px' : '0' }" @file-added="onMusicAdded"
                            @file-success="onMusicSuccess" @files-submitted="onMusicSubmitted" @file-error="onMusicError">
                            <uploader-drop v-if="!isMusicSelected"
                                class="d-flex h-100 w-100 flex-column align-items-center justify-content-center">
                                <span>Drop mp3 file</span>
                                <span class="my-1">Or</span>
                                <uploader-btn class="btn btn-outline-light">Select MP3 file</uploader-btn>
                            </uploader-drop>
                            <uploader-list></uploader-list>
                        </uploader>
                        <button type="button" class="clear-button btn btn-outline-danger mt-3"
                            @click="clearMusicUploadSection">Clear
                            Music</button>



                        <label class="my-4 fs-4" for="coverPic">Upload Cover Picture:</label>

                        <!-- Add your upload cover image components here -->
                        <div class="align-self-center justify-content-center" v-show="!isCoverSelected">
                            <uploader ref="coverUploaderRef" :options="coverUploaderOptions" :autoStart="false"
                                class="drop-zone" :style="{ 'padding-right': isCoverSelected ? '28px' : '0' }"
                                @file-added="onCoverAdded" @file-success="onCoverSuccess"
                                @files-submitted="onCoverSubmitted" @file-error="onCoverError">
                                <uploader-drop
                                    class="d-flex h-100 w-100 flex-column align-items-center justify-content-center">
                                    <span>Drop image file</span>
                                    <span class="my-1">Or</span>
                                    <uploader-btn class="btn btn-outline-light">Select image file</uploader-btn>
                                </uploader-drop>
                                <uploader-list></uploader-list>
                            </uploader>
                        </div>
                        <div v-if="isCoverSelected">
                            <img class="drop-zone" :src="cover" alt="Hello">
                        </div>
                        <button type="button" class="clear-button btn btn-outline-danger mt-3"
                            @click="clearCoverUploadSection">Clear
                            Cover</button>



                    </div>
                </div>
                <div class="col w-50">
                    <div class="modal-right-section d-flex flex-column justify-content-center h-100 px-3">
                        <!-- Add your fields (title, lyrics, etc.) component or content here -->
                        <label class="py-3" for="songTitle">Title:</label>
                        <input type="text" id="songTitle" v-model="songTitle"
                            class="form-control bg-transparent text-white">

                        <label class="py-3" for="songLyrics">Lyrics:</label>
                        <textarea id="songLyrics" v-model="songLyrics" class="form-control bg-transparent text-white"
                            placeholder="La La La"></textarea>

                        <label class="py-3" for="songGenres">Genres:</label>
                        <div>
                            <div class="input-group mb-3">
                                <input v-model="genreInput" @keyup.enter="addGenre" @keyup.space="addGenre" type="text"
                                    class="form-control bg-transparent text-white" placeholder="Type and press Enter...">
                            </div>

                            <div class="mt-3">
                                <span v-for="(chip, index) in genres" :key="index"
                                    :class="['badge', 'rounded-pill', getGenreColor(index), 'mr-2', 'ps-3', 'm-1']">
                                    <span class="d-flex align-items-center fs-6 fw-light">{{ chip }}
                                        <button type="button" @click="removeGenre(index)"
                                            class="p-1 fs-5 text-white bg-transparent" aria-label="Close">&times;</button>
                                    </span>
                                </span>
                            </div>
                        </div>

                    </div>
                </div>

            </div>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="startUpload">Add
                Song</button>
            <button type="button" class="btn btn-primary" @click="closeModal">Close</button>
        </div>
    </div>
</template>


<script>
import { ref } from 'vue';
import axios from 'axios';
export default {
    setup() {
        const musicUploaderRef = ref(null)
        const coverUploaderRef = ref(null)

        return { musicUploaderRef, coverUploaderRef };
    },
    data() {
        return {
            songTitle: '',
            songLyrics: '',
            genreInput: '',
            genres: [],

            isMusicSelected: false,
            isCoverSelected: false,
            musicSelectionResponse: null,
            coverSelectionResponse: null,

            musicUploaderOptions: {
                target: '//localhost:5000/songs/upload',
                testChunks: false,
                chunkSize: 1 * 1024 * 1024 * 20,
                accept: 'audio/*',
                singleFile: true,
            },


            coverUploaderOptions: {
                target: '//localhost:5000/covers/upload',
                testChunks: false,
                accept: 'image/*',
                singleFile: true,
            },


        }
    },
    methods: {
        addGenre() {
            if (this.genreInput.trim() !== '') {
                this.genres.push(this.genreInput.trim());
                this.genreInput = '';
            }
        },
        removeGenre(index) {
            this.genres.splice(index, 1);
        },
        getGenreColor(index) {
            const colorClasses = ['bg-primary', 'bg-secondary', 'bg-success', 'bg-danger', 'bg-warning', 'bg-info', 'bg-light'];
            const colorIndex = index % colorClasses.length;
            return `text-${colorClasses[colorIndex]}`;
        },




        onMusicAdded(file) {
            if (file.size > 20 * 1024 * 1024) {
                file.ignored = true;
                // Clear the music upload section and show an alert
                this.clearMusicUploadSection();
                alert('Maximum file size allowed is 20MB.');
            } else if (!file.name.toLowerCase().endsWith('.mp3')) {

                file.ignored = true;
                // Clear the music upload section and show an alert
                this.clearMusicUploadSection();
                alert('Please upload an MP3 file.');
            } else {
                this.isMusicSelected = !this.isMusicSelected;
                // This method will be called when a file is added
                console.log('File added:', file);
            }
        },
        onMusicSubmitted(files, fileList, event) {

            this.isMusicSelected = true;

        },
        uploadMusic() {
            const musicUploader = this.musicUploaderRef.uploader
            musicUploader.upload()
        },
        onMusicSuccess(rootFile, file, message, chunk) {
            console.log("Music Sucessfully Uploaded : ", message);
            this.musicSelectionResponse = JSON.parse(message);
            if (this.isCoverSelected) {
                this.uploadCover();
            } else {
                this.createMusicEntry()
            }

        },
        onMusicError(rootFile, file, message, chunk) {
            console.log("Message", message);
        },

