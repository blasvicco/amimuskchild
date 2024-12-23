<script setup>
  // General imports
  import { reactive, ref } from 'vue';
  import { message } from 'ant-design-vue';
  import { PlusOutlined, LoadingOutlined } from '@ant-design/icons-vue';

  // Modules imports
  import AppAPI from '@/modules/api';

  // Assets imports
  import musk from "@/assets/img/musk.jpeg";
  import putin from "@/assets/img/putin.jpeg";
  import trump from "@/assets/img/trump.jpeg";

  const colour = ref(0);
  const animal = ref(0);
  const dictator = ref(0);
  const fileList = ref([]);
  const loading = ref(false);
  const imageUrl = ref('');
  let headers = reactive({ value: false });
  let response = reactive({ value: false });

  const reload = () => window.location.reload();

  const getBase64 = (img, callback) => {
    const reader = new FileReader();
    reader.addEventListener('load', () => callback(String(reader.result)));
    reader.readAsDataURL(img);
  }

  const getScore = () => {
    return Number(colour.value) + Number(animal.value) + Number(dictator.value);
  };

  const handleChange = (info) => {
    if (info.file.status === 'uploading') {
      loading.value = true;
      return;
    }
    if (info.file.status === 'done') {
      // Get this url from response in real world.
      getBase64(info.file.originFileObj, (base64Url) => {
        imageUrl.value = base64Url;
        loading.value = false;
        response.value = {
          ...info.file.response,
          score: getScore(),
        };
      });
    }
    if (info.file.status === 'error') {
      loading.value = false;
      if (info.file.response && info.file.response[0]) {
        const options = {
          0: 'an abstract art piece',
          1: 'a picture of an orange',
          2: 'a Renaissance sculpture',
          3: 'a Pixar movie character',
          4: 'an extinct animal',
          5: 'a creature from outer space',
          6: 'what you had for breakfast',
        }[Math.floor(Math.random() * 7)];
        return message.error({
          'IMAGE_DOES_NOT_CONTAIN_A_FACE': `Hmm... our AI says, "No face detected". Is this ${options}? Let’s try again!`,
          'NOT_VALID_FACE_FILE_SIZE_TOO_LARGE': 'File size too large.',
        }[info.file.response[0]]);
      }
      message.error('upload error');
    }
  };

  const beforeUpload = (file) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
    if (!isJpgOrPng) {
      message.error('You can only upload JPG file!');
    }
    const isSmallFileSize = file.size / 1024 / 1024 <= 0.5;
    if (!isSmallFileSize) {
      message.error('Image must smaller than 0.5MB. Sorry.');
    }
    return isJpgOrPng && isSmallFileSize;
  };

  const getTokens = async () => {
    // get locations
    await AppAPI.Facecheck.OAuth.regenerate();
    headers.value = AppAPI.Facecheck.header();
  };
  getTokens();
</script>

<template>
  <div v-if="headers.value">
    <a-space direction="vertical" :style="{ marginLeft: '10%', marginTop: '20px', marginBottom: '20px', width: '80%' }">
      <a-card title="Am I a child of Elon Müsk?" :bordered="false">
        <p>Have you ever wondered if you're part of Elon Müsk’s master plan to repopulate Earth with his superior genes? Thanks to his enthusiastic use of in-vitro fertilization, the possibility is... well, non-zero.</p>
        <p>But fear not! We’ve harnessed the power of cutting-edge AI to answer life’s most important question: Am I a child of Elon Müsk?</p>
        <p>And the best part? It’s totally free—because let’s be real, even Elon couldn’t afford to charge you for this much fun.</p>
      </a-card>
      <a-card title="How does this work?" :bordered="false">
        <p>It’s as simple as 1, 2, 3:</p>
        <p>1. Answer a couple of totally normal, definitely relevant questions (it’ll take less than a minute, promise).</p>
        <p>2. Upload a picture of your beautiful face.</p>
        <p>3. Let our highly advanced (and mildly ridiculous) AI work its magic to reveal your possibly billionaire heritage.</p>
        <p>P.S. Don’t worry about your data—we couldn’t store it even if we wanted to. We’re broke, remember?</p>
      </a-card>
      <a-card title="Questionnaire" :bordered="false">
        <p>Which color gets your billionaire vibes going?</p>
        <a-radio-group v-model:value="colour">
          <a-radio value="0">Blue (like the Tesla car you wish you had)</a-radio>
          <a-radio value="1">Red (like Mars—Elon’s dream home)</a-radio>
        </a-radio-group>
        <p>Which animal feels like your spirit guide?</p>
        <a-radio-group v-model:value="animal">
          <a-radio value="0">Donkey</a-radio>
          <a-radio value="1">Elephant</a-radio>
        </a-radio-group>
        <a-flex align="center" gap="middle">
          <p>What does this character inspire in you?</p>
          <a-avatar :size="64" :src="putin" />
        </a-flex>
        <a-radio-group v-model:value="dictator">
          <a-radio value="1">I don’t know who this is, and I’m slightly concerned.</a-radio>
          <a-radio value="0">Nope. Not a fan.</a-radio>
          <a-radio value="2">I like him and think he is an example of leadership.</a-radio>
        </a-radio-group>
      </a-card>
      <a-card title="Upload you picture" :bordered="false">
        <p>And now, the moment of truth! Snap a selfie or upload your best Elon-esque photo. Based on your answers and our AI’s totally serious calculations, we’ll deliver your fate:</p>
        <a-flex align="center" gap="middle">
          <a-space direction="horizontal">
            <a-avatar v-if="!response.value || response.value.prediction === 'MUSK'" :size="64" :src="musk" />
            <a-avatar v-else :size="64" :src="trump" />
            <div>→</div>
            <a-avatar v-if="imageUrl" :size="64" :src="imageUrl" />
            <a-upload
              v-else
              v-model:file-list="fileList"
              :action="AppAPI.Facecheck.constants.UPLOAD"
              :before-upload="beforeUpload"
              :headers="headers.value"
              :show-upload-list="false"
              @change="handleChange"
              accept="image/jpeg,image/png"
              class="face-uploader"
              name="face"
              list-type="picture-card"
            >
              <div>
                <loading-outlined v-if="loading"></loading-outlined>
                <plus-outlined v-else></plus-outlined>
                <div class="ant-upload-text">Upload</div>
              </div>
            </a-upload>
            <div>=</div>
            <a-card v-if="response.value">
              <div><p>{{ AppAPI.Facecheck.interpret(response.value) }}</p></div>
              <div><button @click="reload()">Try again!</button></div>
            </a-card>
          </a-space>
        </a-flex>
      </a-card>
    </a-space>
  </div>
</template>
