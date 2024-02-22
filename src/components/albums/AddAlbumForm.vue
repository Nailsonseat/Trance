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
            <!-- Add your upload song and cover pic components or content here -->

            <label class="my-4 fs-4" for="coverPic">Upload Album Cover</label>

            <!-- Add your upload cover image components here -->
            <div class="align-self-center justify-content-center" v-show="!isCoverSelected">
                <uploader ref="coverUploaderRef" :options="coverUploaderOptions" :autoStart="false" class="drop-zone"
                    :style="{ 'padding-right': isCoverSelected ? '28px' : '0' }" @file-added="onCoverAdded"
                    @file-success="onCoverSuccess" @files-submitted="onCoverSubmitted" @file-error="onCoverError">
                    <uploader-drop class="d-flex h-100 w-100 flex-column align-items-center justify-content-center">
                        <span>Drop image file</span>
                        <span class="my-1">Or</span>
                        <uploader-btn class="btn btn-outline-light">Select image file</uploader-btn>
                    </uploader-drop>
                    <uploader-list></uploader-list>
                </uploader>
            </div>

            <label class="py-3" for="songLyrics">Album Name</label>
            <textarea id="albumName" v-model="albumName" class="form-control bg-transparent text-white"></textarea>

            <div v-if="isCoverSelected">
                <img class="drop-zone" :src="cover" alt="Hello">
            </div>
            <button type="button" class="clear-button btn btn-outline-danger mt-3" @click="">Clear
                Cover
            </button>



        </div>


        <!-- Modal Footer -->
        <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="uploadCover">Add
                Album</button>
            <button type="button" class="btn btn-primary" @click="closeModal">Close</button>
        </div>
    </div>
</template>


<script>
import axios from 'axios';
import { ref } from 'vue';

export default {

    setup() {
        const coverUploaderRef = ref(null)

        return { coverUploaderRef };
    },
    data() {
        return {
            albumName: '',
            isCoverSelected: false,
            cover: null,
            coverUploaderOptions: {
                target: '//localhost:5000/albumcover/upload',
                testChunks: false,
                accept: 'image/*',
                singleFile: true,
            }
        }
    },
    methods: {
        onCoverAdded(file) {
            const allowedExtensions = ['jpg', 'jpeg', 'png'];
            const extension = file.name.split('.').pop().toLowerCase();

            if (file.size > 20 * 1024 * 1024) {
                file.ignored = true;
                // Clear the cover upload section and show an alert
                this.clearCoverUploadSection();
                alert('Maximum file size allowed is 20MB.');
            } else if (!allowedExtensions.includes(extension)) {
                file.ignored = true;
                // Clear the cover upload section and show an alert
                this.clearCoverUploadSection();
                alert('Please upload a valid image file (JPG, JPEG, PNG).');
            } else {

                this.isCoverSelected = !this.isCoverSelected;
                // This method will be called when a cover image file is added
                console.log('Cover file added:', file);
            }
        },
        onCoverSubmitted(files, fileList, event) {
            if (files[0]) {
                this.cover = URL.createObjectURL(files[0].file)
                this.isCoverSelected = true;
            }
        },
        uploadCover() {
            if (this.isCoverSelected) {
                const albumCoverUploader = this.coverUploaderRef.uploader;
                albumCoverUploader.upload();
            } else {
                this.createAlbumEntry();
            }
        },
        onCoverSuccess(rootFile, file, message, chunk) {
            console.log("Cover Sucessfully Uploaded : ", message);
            this.coverSelectionResponse = JSON.parse(message)
            this.createAlbumEntry();
        },
        onCoverError(rootFile, file, message, chunk) {
            console.log("Message", message);
        },
        clearCoverUploadSection() {
            this.isCoverSelected = false;
            this.coverUploaderRef.uploader.files.forEach(file => {
                file.cancel();
            });
        },
        createAlbumEntry() {
            const API_ENDPOINT = 'http://localhost:5000/';
            // what if the album cover is not selected?
            const payload = {
                title: this.albumName,
                artist: 'aadarsh',
                cover_path: this.coverSelectionResponse ? this.coverSelectionResponse.path : null,
            };


            axios.post(API_ENDPOINT + 'albums/create', payload)
                .then(response => {
                    console.log('Album created successfully:', response);
                    this.closeModal();
                })
                .catch(error => {
                    console.error('Error creating album:', error);
                });
        },
        closeModal() {
            this.clearCoverUploadSection();
            this.albumName = '';
            this.$emit('close-modal');
        },
    },
}


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

.clear-button {
    width: 200px;
    align-self: center;
}


.close {
    border: 1px solid #fff;
    background-color: red;
}
</style>