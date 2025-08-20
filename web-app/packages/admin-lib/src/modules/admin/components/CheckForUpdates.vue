<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-container v-if="adminStore.displayUpdateAvailable">
    <app-section-banner>
      <template #title>{{ UpdateAvailable }}</template>
      <template #description
        >{{ ANewVersionOfMerginMapsIsAvailableForUsersLetsExploreItsNewFeatures }}</template
      >
      <template #header-actions
        ><PButton
          @click="openUpdateUrl"
          severity="secondary"
          data-cy="check-for-updates-btn"
          :label="Update"
      /></template>
    </app-section-banner>
  </app-container>
</template>

<script lang="ts" setup>
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const UpdateAvailable = returnTranslation(lang, 'UpdateAvailable');
const ANewVersionOfMerginMapsIsAvailableForUsersLetsExploreItsNewFeatures = returnTranslation(lang, 'ANewVersionOfMerginMapsIsAvailableForUsersLetsExploreItsNewFeatures');
const Update = returnTranslation(lang, 'Update');


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
