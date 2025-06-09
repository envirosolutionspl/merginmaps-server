<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-container v-if="adminStore.displayUpdateAvailable">
    <app-section-banner>
      <template #title>{{ Translation_UpdateAvailable }}</template>
      <template #description
        >{{ Translation_ANewVersionOfMerginMapsIsAvailableForUsers }}</template
      >
      <template #header-actions
        ><PButton
          @click="openUpdateUrl"
          severity="secondary"
          data-cy="check-for-updates-btn"
          :label="Translation_Update"
      /></template>
    </app-section-banner>
  </app-container>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_UpdateAvailable = returnTranslation(lang, 'adminlib_admin_CheckForUpdates_UpdateAvailable');
const Translation_ANewVersionOfMerginMapsIsAvailableForUsers = returnTranslation(lang, 'adminlib_admin_CheckForUpdates_ANewVersionOfMerginMapsIsAvailableForUsers');
const Translation_Update = returnTranslation(lang, 'adminlib_admin_CheckForUpdates_Update');


import { AppSectionBanner, AppContainer } from '@mergin/lib'
import { onMounted } from 'vue'

import { useAdminStore } from '@/modules/admin/store'

const adminStore = useAdminStore()

onMounted(async () => {
  await adminStore.checkVersions()
})

function openUpdateUrl() {
  window.open(adminStore.latestServerVersion?.info_url, '_blank')
}
</script>

<style scoped></style>
