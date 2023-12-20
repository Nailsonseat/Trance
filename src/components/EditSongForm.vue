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
