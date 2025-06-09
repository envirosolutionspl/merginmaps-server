<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-container v-if="displayBanner">
    <app-section-banner>
      <template #title>{{ Translation_ServerIsNotProperlyConfigured }}</template>
      <template #description
        >{{ Translation_YourServerIsNotConfiguredProperlyForUse }}
        <a :href="docsLinkDocumentation" target="_blank">{{ Translation_Documentation }}</a>
        {{ Translation_HowToProperlySetUpTheDeployment }}.</template
      >
      <template #header-actions
        ><PButton
          @click="dismiss"
          severity="secondary"
          data-cy="dismiss-server-configured-btn"
          :label="Translation_Dismiss"
      /></template>
    </app-section-banner>
  </app-container>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_ServerIsNotProperlyConfigured = returnTranslation(lang, 'adminlib_admin_ServerNotConfigured_ServerIsNotProperlyConfigured');
const Translation_YourServerIsNotConfiguredProperlyForUse = returnTranslation(lang, 'adminlib_admin_ServerNotConfigured_YourServerIsNotConfiguredProperlyForUse');
const Translation_Documentation = returnTranslation(lang, 'adminlib_admin_ServerNotConfigured_Documentation');
const Translation_HowToProperlySetUpTheDeployment = returnTranslation(lang, 'adminlib_admin_ServerNotConfigured_HowToProperlySetUpTheDeployment');
const Translation_Dismiss = returnTranslation(lang, 'adminlib_admin_ServerNotConfigured_Dismiss');

import { useInstanceStore, AppSectionBanner, AppContainer } from '@mergin/lib'
import { computed } from 'vue'

import { useAdminStore } from '@/modules/admin/store'

const adminStore = useAdminStore()
const instanceStore = useInstanceStore()

const docsLinkDocumentation = computed(
  () => `${instanceStore.configData?.docs_url ?? ''}/dev/mergince`
)
const displayBanner = computed(
  () =>
    !instanceStore.configData?.server_configured &&
    !adminStore.isServerConfigHidden
)

function dismiss() {
  adminStore.setServerConfiguredCookies()
}

adminStore.getServerConfiguredCookies()
</script>

<style lang="scss" scoped></style>
