<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <PToast group="download-large-error" position="top-center">
    <template #message>
      <p>
        {{ Translation_TheProjectIsTooLargeToDownload }}
        <a
          href="https://merginmaps.com/blog/support-tip-downloading-a-previous-version-of-your-project"
          target="_blank"
          class="font-semibold"
          >{{ Translation_ReadOurBlogForMoreDetails }}</a
        >.
      </p>
    </template>
  </PToast>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_TheProjectIsTooLargeToDownload = returnTranslation(lang, 'lib_project_DownloadFileLarge_TheProjectIsTooLargeToDownload');
const Translation_ReadOurBlogForMoreDetails = returnTranslation(lang, 'lib_project_DownloadFileLarge_ReadOurBlogForMoreDetails');

</script>

<script lang="ts">
import { defineComponent } from 'vue'

// we need to use options api here , because useToast is not properly handled multiple toast services
export default defineComponent({
  name: 'DownloadFileLarge'
})
</script>

<style lang="scss" scoped></style>
