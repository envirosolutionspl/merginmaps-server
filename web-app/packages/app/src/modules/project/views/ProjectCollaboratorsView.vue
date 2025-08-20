<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <project-collaborators-view-template
    v-if="isProjectOwner"
    @share="openShareDialog"
    :allow-share="instanceStore.currentGlobalRole === undefined"
    :show-access-requests="userStore.isGlobalWorkspaceAdmin"
  >
    <project-members-table
      :allow-remove="instanceStore.currentGlobalRole === undefined"
    />
  </project-collaborators-view-template>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

import {
  ProjectShareDialog,
  ProjectCollaboratorsViewTemplate,
  useDialogStore,
  useProjectStore,
  useUserStore,
  useInstanceStore,
  useNotificationStore,
  errorUtils,
  ProjectMembersTable
} from '@mergin/lib'
import { computed } from 'vue'

const projectStore = useProjectStore()
const dialogStore = useDialogStore()
const userStore = useUserStore()
const instanceStore = useInstanceStore()
const notificationStore = useNotificationStore()

const isProjectOwner = computed(() => projectStore.isProjectOwner)

function openShareDialog() {
  const lang = import.meta.env.VITE_LANG
  const FailedToSaveProjectSettings = returnTranslation(lang, 'FailedToSaveProjectSettings');
  const ShareProject = returnTranslation(lang, 'ShareProject');
  const dialog = {
    maxWidth: 600,
    header: `${ShareProject} ${projectStore.project?.name}`
  }
  dialogStore.show({
    component: ProjectShareDialog,
    params: {
      dialog,
      listeners: {
        onShareError: (err) => {
          notificationStore.error({
            text: errorUtils.getErrorMessage(
              err,
              FailedToSaveProjectSettings
            )
          })
        }
      }
    }
  })
}
</script>
