<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-container v-if="displayBanner">
    <app-section-banner>
      <template #title>{{ ServerIsNotProperlyConfigured }}</template>
      <template #description
        >{{ YourServerIsNotConfiguredProperlyForUseInTheProductionEnvironmentReadMoreInThe }}
        <a :href="docsLinkDocumentation" target="_blank">{{ Documentation }}</a> {{ HowToProperlySetUpTheDeployment }}</template
      >
      <template #header-actions
        ><PButton
          @click="dismiss"
          severity="secondary"
          data-cy="dismiss-server-configured-btn"
          :label="Dismiss"
      /></template>
    </app-section-banner>
  </app-container>
</template>

<script lang="ts" setup>
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const ServerIsNotProperlyConfigured = returnTranslation(lang, 'ServerIsNotProperlyConfigured');
const YourServerIsNotConfiguredProperlyForUseInTheProductionEnvironmentReadMoreInThe = returnTranslation(lang, 'YourServerIsNotConfiguredProperlyForUseInTheProductionEnvironmentReadMoreInThe');
const Documentation = returnTranslation(lang, 'Documentation');
const HowToProperlySetUpTheDeployment = returnTranslation(lang, 'HowToProperlySetUpTheDeployment');
const Dismiss = returnTranslation(lang, 'Dismiss');

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
