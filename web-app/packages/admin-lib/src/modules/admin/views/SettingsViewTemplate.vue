<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <admin-layout>
    <app-container>
      <app-section ground>
        <template #header><h1 class="headline-h3">{{ Settings }}</h1></template>
      </app-section>
    </app-container>

    <app-container>
      <app-section>
        <template #title>{{ Advanced }}</template>
        <app-settings :items="settingsItems">
          <template #items-start><slot /></template>

          <template #checkForUpdates
            ><PInputSwitch
              :modelValue="adminStore.checkForUpdates"
              @change="switchCheckForUpdates"
          /></template>
          <template #downloadReport
            ><PButton
              severity="secondary"
              @click="downloadReport"
              :label="Download"
          /></template>
        </app-settings>
      </app-section>
    </app-container>
  </admin-layout>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG
const Settings = returnTranslation(lang, 'Settings');
const Advanced = returnTranslation(lang, 'Advanced');
const Download = returnTranslation(lang, 'Download');

import {
  AppContainer,
  AppSection,
  AppSettings,
  AppSettingsItemConfig,
  useDialogStore
} from '@mergin/lib'

import ReportDownloadDialog from '../components/ReportDownloadDialog.vue'
import { useAdminStore } from '../store'

import AdminLayout from '@/modules/admin/components/AdminLayout.vue'

withDefaults(defineProps<{ settingsItems?: AppSettingsItemConfig[] }>(), {
  settingsItems: () => [
    {
      title: returnTranslation(import.meta.env.VITE_LANG, 'CheckForUpdates'),
      description: returnTranslation(import.meta.env.VITE_LANG, 'LetMerginMapsAutomaticallyCheckForNewUpdates'),
      key: 'checkForUpdates'
    },
    {
      title: returnTranslation(import.meta.env.VITE_LANG, 'ServerUsageReport'),
      description: returnTranslation(import.meta.env.VITE_LANG, 'DownloadUsageStatisticsForYourServerDeployment'),
      key: 'downloadReport'
    }
  ]
})

const adminStore = useAdminStore()
const dialogStore = useDialogStore()

function switchCheckForUpdates() {
  const value = !adminStore.checkForUpdates
  adminStore.setCheckUpdatesToCookies({ value })
}

function downloadReport() {
  dialogStore.show({
    component: ReportDownloadDialog,
    params: {
      dialog: { header: returnTranslation(lang, 'DownloadReport') }
    }
  })
}
</script>

<style lang="scss" scoped></style>
