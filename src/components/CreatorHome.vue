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
