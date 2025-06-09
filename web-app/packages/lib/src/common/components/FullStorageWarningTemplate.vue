<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-container v-if="open">
    <slot :usage="usage">
      <PMessage severity="warn" @close="open = false" class="m-0">
        <template #messageicon="slotProps">
          <i :class="[slotProps.class, 'ti ti-alert-triangle-filled']" />
        </template>
        <p>
          <span class="font-semibold"
            >{{ Translation_YourStorageIsAlmostFull }} ({{ usage }}%).</span
          >
          {{ Translation_SoonYouWillNotBeAbleToSyncYourProjects }}
        </p></PMessage
      >
    </slot>
  </app-container>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_YourStorageIsAlmostFull = returnTranslation(lang, 'lib_components_FullStorageWarningTemplate_YourStorageIsAlmostFull');
const Translation_SoonYouWillNotBeAbleToSyncYourProjects = returnTranslation(lang, 'lib_components_FullStorageWarningTemplate_SoonYouWillNotBeAbleToSyncYourProjects');

import { computed, ref } from 'vue'

import { AppContainer } from '@/common/components'
import { useUserStore } from '@/main'

const userStore = useUserStore()

const usage = computed(() =>
  userStore.currentWorkspace?.disk_usage > userStore.currentWorkspace?.storage
    ? 0
    : Math.floor(
        (userStore.currentWorkspace?.disk_usage /
          userStore.currentWorkspace?.storage) *
          100
      )
)

/** Handle open state with connection to message close button */
const isOver = computed({
  get() {
    return usage.value > 90
  },
  set(value) {
    open.value = value
  }
})
const open = ref(isOver)
</script>

<style scoped></style>
