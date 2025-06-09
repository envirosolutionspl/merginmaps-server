<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <admin-layout>
    <app-container>
      <app-section ground>
        <template #header><h1 class="headline-h3">{{ Translation_Settings }}</h1></template>
      </app-section>
    </app-container>

    <app-container>
      <app-section>
        <template #title>{{ Translation_Advanced }}</template>
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
              :label="Translation_Download"
          /></template>
        </app-settings>
      </app-section>
    </app-container>
  </admin-layout>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_Settings = returnTranslation(lang, 'adminlib_admin_SettingsViewTemplate_Settings')
const Translation_Advanced = returnTranslation(lang, 'adminlib_admin_SettingsViewTemplate_Advanced')
const Translation_Download = returnTranslation(lang, 'adminlib_admin_SettingsViewTemplate_Download')

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
  settingsItems: () => {
    const lang = import.meta.env.VITE_LANG
    return [
      {
        title: returnTranslation(lang, 'adminlib_admin_SettingsViewTemplate_CheckForUpdates'),
        description: returnTranslation(lang, 'adminlib_admin_SettingsViewTemplate_LetMerginMapsAutomaticallyCheckForNewUpdates'),
        key: 'checkForUpdates'
      },
      {
        title: returnTranslation(lang, 'adminlib_admin_SettingsViewTemplate_ServerUsageReport'),
        description: returnTranslation(lang, 'adminlib_admin_SettingsViewTemplate_DownloadUsageStatisticsForYourServerDeployment'),
        key: 'downloadReport'
      }
    ]
  }
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
      dialog: { header: returnTranslation(lang, 'adminlib_admin_SettingsViewTemplate_DownloadReport') }
    }
  })
}
</script>

<style lang="scss" scoped></style>
