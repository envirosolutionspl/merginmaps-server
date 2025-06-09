<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <settings-view-template>
    <app-settings-item v-for="item in settingsItems" :key="item.key">
      <template #title>{{ item.title }}</template>
      <template #description
        >{{ item.description
        }}<template v-if="item.key === 'usageInformation'">
          {{ Translation_Click }}
          <a
            class="font-semibold text-color-forest"
            :href="instanceStore.configData?.docs_url"
            target="_blank"
            >{{ Translation_Here }}</a
          >
          {{ Translation_ForMoreInformation }}</template
        ></template
      >
      <template #action>
        <div class="flex-shrink-0 paragraph-p1">
          <PInputSwitch
            :model-value="Boolean(instanceStore.configData?.collect_statistics)"
            disabled
          />
        </div>
      </template>
    </app-settings-item>
  </settings-view-template>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_Click = returnTranslation(lang, 'adminlib_admin_SettingsView_Click');
const Translation_Here = returnTranslation(lang, 'adminlib_admin_SettingsView_Here');
const Translation_ForMoreInformation = returnTranslation(lang, 'adminlib_admin_SettingsView_ForMoreInformation');

import {
  AppSettingsItemConfig,
  useInstanceStore,
  AppSettingsItem
} from '@mergin/lib'
import { ref } from 'vue'

import SettingsViewTemplate from '@/modules/admin/views/SettingsViewTemplate.vue'

const instanceStore = useInstanceStore()

const settingsItems = ref<AppSettingsItemConfig[]>([
  {
    title: returnTranslation(lang, 'adminlib_admin_SettingsView_CollectStatistics'),
    description: returnTranslation(lang, 'adminlib_admin_SettingsView_HelpUsImproveMerginMaps'),
    key: 'usageInformation'
  }
])
</script>

<style scoped></style>
