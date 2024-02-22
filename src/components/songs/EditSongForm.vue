<template>
  <!-- Left section for upload song and cover pic -->
  <div class="position-absolute top-50 start-50 translate-middle modal-content">
    <!-- Modal Header -->
    <div class="modal-header">
      <h5 class="modal-title fs-4">Edit Song</h5>
      <button type="button" class="close" @click="closeModal" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>

    <div class="modal-body">
      <div class="row h-100">
        <div class="col w-50" style="border-right: 1px solid #ffffff;">
          <div class="modal-left-section d-flex flex-column justify-content-center h-100">
            <!-- Upload Song -->
            <label class="my-4 fs-4" for="songFile">Edit Song: {{ songTitle }}</label>
            <uploader ref="musicReplacerRef" :options="musicReplacerOptions" :autoStart="false"
              class="drop-zone d-flex flex-column flex-column align-items-center justify-content-center"
              :style="{ 'padding-right': isMusicReplacerSelected ? '28px' : '0' }" @file-added="onMusicReplacerAdded"
              @file-success="onMusicReplacerSuccess" @files-submitted="onMusicReplacerSubmitted"
              @file-error="onMusicReplacerError">
              <uploader-drop v-if="!isMusicReplacerSelected"
                class="d-flex h-100 w-100 flex-column align-items-center justify-content-center">
                <span>Drop mp3 file</span>
                <span class="my-1">Or</span>
                <uploader-btn class="btn btn-outline-light">Select MP3 file</uploader-btn>
              </uploader-drop>
              <uploader-list></uploader-list>
            </uploader>

            <!--             
            <div v-if="isMusicReplacerSelected">
              <img class="drop-zone" :src="replacerMusic" alt="Replacer Music">
            </div> -->


            <button type="button" class="clear-button btn btn-outline-danger mt-3"
              @click="clearMusicReplacerSection">Clear Music</button>

            <!-- Upload Cover Picture -->
            <label class="my-4 fs-4" for="coverPic">Upload Cover Picture:</label>
            <uploader ref="coverReplacerRef" :options="coverReplacerOptions" :autoStart="false" class="drop-zone"
              :style="{ 'padding-right': isCoverReplacerSelected ? '28px' : '0' }" @file-added="onCoverReplacerAdded"
              @file-success="onCoverReplacerSuccess" @files-submitted="onCoverReplacerSubmitted"
              @file-error="onCoverReplacerError">
              <uploader-drop class="d-flex h-100 w-100 flex-column align-items-center justify-content-center">
                <span>Drop image file</span>
                <span class="my-1">Or</span>
                <uploader-btn class="btn btn-outline-light">Select image file</uploader-btn>
              </uploader-drop>
              <uploader-list></uploader-list>
            </uploader>
            <div v-if="isCoverReplacerSelected">
              <img class="drop-zone" :src="replacerCover" alt="Replacer Cover">
            </div>
            <button type="button" class="clear-button btn btn-outline-danger mt-3"
              @click="clearCoverReplacerSection">Clear Cover</button>
          </div>
        </div>
        <div class="col w-50">
          <div class="modal-right-section d-flex flex-column justify-content-center h-100 px-3">
            <!-- Existing code for title, lyrics, and genres -->
            <div class="modal-right-section d-flex flex-column justify-content-center h-100 px-3">
              <!-- Add your fields (title, lyrics, etc.) component or content here -->
              <label class="py-3" for="songTitle">Title:</label>
              <input type="text" id="songTitle" v-model="songTitle" class="form-control bg-transparent text-white">

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
                      <button type="button" @click="removeGenre(index)" class="p-1 fs-5 text-white bg-transparent"
                        aria-label="Close">&times;</button>
                    </span>
                  </span>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Footer -->
    <div class="modal-footer">
      <button type="button" class="btn btn-primary" @click="updateSong">Update Song</button>
      <button type="button" class="btn btn-primary" @click="closeModal">Close</button>
    </div>

  </div>
</template>



<script>
import axios from 'axios';
import { ref } from 'vue';

export default {
  props: {
    songToEdit: {
      required: true,
    },
  },
  setup() {
    const musicReplacerRef = ref(null);
    const coverReplacerRef = ref(null);

    return { musicReplacerRef, coverReplacerRef };
  },
  data() {
    return {
      songTitle: this.songToEdit ? this.songToEdit.title : '',
      songLyrics: this.songToEdit ? this.songToEdit.lyrics : '',
      genres: this.songToEdit ? this.songToEdit.genres : [],
      genreInput: '',
      isMusicReplacerSelected: false,
      isCoverReplacerSelected: false,

      replacerMusic: null,
      replacerCover: null,


      musicReplacerOptions: {
        target: '//localhost:5000/songs/upload',
        testChunks: false,
        chunkSize: 1 * 1024 * 1024 * 20,
        accept: 'audio/*',
        singleFile: true,
        uploadMethod: 'PUT',
      },


      coverReplacerOptions: {
        target: '//localhost:5000/covers/upload',
        testChunks: false,
        accept: 'image/*',
        singleFile: true,
        uploadMethod: 'PUT'
      },

    };
  },
  watch: {
    songToEdit(newSong) {
      if (newSong) {
        this.songTitle = newSong.title;
        this.songLyrics = newSong.lyrics;
        this.genres = newSong.genres;
      }
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
    onMusicReplacerAdded(file) {
      if (file.size > 20 * 1024 * 1024) {
        file.ignored = true;
        this.clearMusicReplacerSection();
        alert('Maximum file size allowed is 20MB.');
      } else if (!file.name.toLowerCase().endsWith('.mp3')) {
        file.ignored = true;
        this.clearMusicReplacerSection();
        alert('Please upload an MP3 file.');
      } else {
        this.isMusicReplacerSelected = !this.isMusicReplacerSelected;
      }
    },
    onMusicReplacerSuccess(rootFile, file, message, chunk) {
      this.replacerMusic = URL.createObjectURL(file.file);
      if (this.isCoverReplacerSelected) {
        this.uploadCoverReplacer();
      } else {
        this.updateMusicEntry();
      }
    },
    onMusicReplacerError(rootFile, file, message, chunk) {
      console.log('Message', message);
    },
    clearMusicReplacerSection() {
      this.isMusicReplacerSelected = false;
      this.replacerMusic = null;
      this.musicReplacerRef.uploader.files.forEach(file => {
        file.cancel();
      });
    },
    onMusicReplacerSubmitted(files, fileList, event) {
      this.isMusicReplacerSelected = true;
    },

    onCoverReplacerSubmitted(files, fileList, event) {

      this.replacerCover = URL.createObjectURL(files[0].file);
      this.isCoverReplacerSelected = true;
    },
    onCoverReplacerAdded(file) {
      const allowedExtensions = ['jpg', 'jpeg', 'png'];
      const extension = file.name.split('.').pop().toLowerCase();

      if (file.size > 20 * 1024 * 1024) {
        file.ignored = true;
        this.clearCoverReplacerSection();
        alert('Maximum file size allowed is 20MB.');
      } else if (!allowedExtensions.includes(extension)) {
        file.ignored = true;
        this.clearCoverReplacerSection();
        alert('Please upload a valid image file (JPG, JPEG, PNG).');
      } else {
        this.isCoverReplacerSelected = !this.isCoverReplacerSelected;
      }
    },
    onCoverReplacerSuccess(rootFile, file, message, chunk) {
      this.updateMusicEntry();
    },
    onCoverReplacerError(rootFile, file, message, chunk) {
      console.log('Message', message);
    },
    clearCoverReplacerSection() {
      this.isCoverReplacerSelected = false;
      this.replacerCover = null;
      this.coverReplacerRef.uploader.files.forEach(file => {
        file.cancel();
      });
    },
    validateTitle() {
      const titleRegex = /^[a-zA-Z0-9\s]+$/;
      return titleRegex.test(this.songTitle);
    },
    validateGenres() {
      const genreRegex = /^[a-zA-Z0-9\s]+$/;
      return this.genres.every(genre => genreRegex.test(genre));
    },
    updateSong() {
      /// TODO - Update the song entry in the database

    },

    closeModal() {
      this.clearMusicReplacerSection();
      this.clearCoverReplacerSection();
      this.songTitle = '';
      this.songLyrics = '';
      this.genres = [];
      this.isMusicSelected = false;
      this.isCoverSelected = false;
      this.$emit('close-modal');
    },
    updateMusicEntry() {
      const API_ENDPOINT = 'http://localhost:5000/';
      const requestData = {
        title: this.songTitle,
        artist: 'aadarsh', // Replace with actual artist data
        lyrics: this.songLyrics,
        album_id: null, // Replace with actual album ID
        filepath: this.replacerMusic,
        coverpath: this.replacerCover,
        hours: null, // Replace with actual duration data
        minutes: null,
        seconds: null,
        genres: this.genres,
      };

      axios.put(API_ENDPOINT + 'songs/update/' + this.songToEdit.id + '/manage', requestData)
        .then(response => {
          console.log('Song updated successfully:', response);
          this.toggleEditSongModal();
        })
        .catch(error => {
          console.error('Error updating song:', error);
        });
    },
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

.clear-button {
  width: 200px;
  align-self: center;
}


.close {
  border: 1px solid #fff;
  background-color: red;
}
</style>