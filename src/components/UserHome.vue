<template>
    <div>
        <!-- Your main content goes here -->
        <div class="container-fluid">
            <div style="background-color: black;">
                <div class="row">
                    <div class="col-3 d-flex align-items-center justify-content-center"
                        style="height: 800px; background-color: rebeccapurple;">
                        <span>Queue</span>
                    </div>
                    <div class="col d-flex align-items-center justify-content-center">
                        <span>Music</span>
                    </div>
                </div>
            </div>
        </div>



        <!-- Audio Player -->
        <div class="audio-player">
            <audio-player ref="audioPlayer" :audio-list="audioList.map(elm => elm.url)" theme-color="#42b883"
                v-model:shuffleOn="shuffleOn" />
        </div>
    </div>
</template>

<script>
import AudioPlayer from '@liripeng/vue-audio-player'
export default {
    // Your component logic goes here
    data() {
        return {
            currentAudioName: '',
            audioList: [
                {
                    name: 'audio1',
                    url: "src/assets/The Living Tombstone - My Ordinary Life.mp3"
                },
                {
                    name: 'audio2',
                    url: 'https://www.0dutv.com/upload/dance/20200316/C719452E3C7834080007662021EA968E.mp3'
                },
            ],
            shuffleOn: false,
        };
    },
    components: {
        AudioPlayer
    },
};
</script>

<style scoped>
/* Your component-specific styles go here */

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
