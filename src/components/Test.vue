<template>
    <uploader :options="options" :file-status-text="statusText" class="uploader-example" ref="uploader"
        @file-complete="fileComplete" @complete="complete" @file-added="onFileAdded" :autoStart="false">
        <!-- <uploader-unsupport></uploader-unsupport>
    <uploader-drop>
      <p>Drop files here to upload or</p>
      <uploader-btn>select files</uploader-btn>
      <uploader-btn :attrs="attrs">select images</uploader-btn>
      <uploader-btn :directory="true">select folder</uploader-btn>
    </uploader-drop>
    <uploader-list></uploader-list> -->
    </uploader>
</template>

<script>
import { nextTick, ref, onMounted } from 'vue'
export default {
    setup() {
        const uploader = ref(null)
        const options = {
            target: '//localhost:5000/upload', // '//jsonplaceholder.typicode.com/posts/',
            testChunks: false
        }
        const attrs = {
            accept: 'image/*'
        }
        const statusText = {
            success: 'success',
            error: 'error',
            uploading: 'uploading',
            paused: 'paused',
            waiting: 'waiting'
        }
        const complete = () => {
            console.log('complete', arguments)
        }
        const fileComplete = () => {
            console.log('file complete', arguments)
        }
        onMounted(() => {
            nextTick(() => {
                window.uploader = uploader.value.uploader
            })
        })
        return {
            uploader,
            options,
            attrs,
            statusText,
            complete,
            fileComplete
        }
    },
    methods: {
        onFileAdded(file) {
            // This method will be called when a file is added
            console.log('File added:', file);
            // Composition API
            // Composition API
            const uploader = ref(null)
            // there will be an uploader attribute on the uploader component, which points to the Uploader instance
            const uploaderInstance = this.uploader.uploader
            // now you can call all uploader methods
            // https://github.com/simple-uploader/Uploader#methods
            console.log(uploaderInstance.upload())

            // Perform any other actions you want with the selected file
        },
    }
}
</script>

<style>
.uploader-example {
    width: 880px;
    padding: 15px;
    margin: 40px auto 0;
    font-size: 12px;
    box-shadow: 0 0 10px rgba(0, 0, 0, .4);
}

.uploader-example .uploader-btn {
    margin-right: 4px;
}

.uploader-example .uploader-list {
    max-height: 440px;
    overflow: auto;
    overflow-x: hidden;
    overflow-y: auto;
}
</style>