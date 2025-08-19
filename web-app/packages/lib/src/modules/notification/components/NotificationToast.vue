<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <PToast position="top-center" :pt="{ content: 'align-items-center' }"
    >>
    <template #message="{ message }">
      <i :class="['p-toast-message-icon', icon(message.severity)]" />
      <div class="p-toast-message-text" data-pc-section="text">
        <span class="p-toast-summary" data-pc-section="summary">{{

          message.summary === 'Account with given email does not exist' ? AccountWithGivenEmailDoesNotExist :
          message.summary === 'Unknown error in input fields' ? UnknownErrorInInputFields :
          message.summary === 'Workspace not found' ? WorkspaceNotFound :
          message.summary === 'You do not have permissions to search within workspace' ? YouDoNotHavePermissionsToSearchWithinWorkspace :
          message.summary === 'You do not have permissions' ? YouDoNotHavePermissions :
          message.summary === 'Version mismatch' ? VersionMismatch :
          message.summary === 'Project with the same name already exists' ? ProjectWithTheSameNameAlreadyExists :
          message.summary.includes("is not a 'email' - 'email'") ? message.summary.replace("is not a 'email' - 'email'", IsNotAEmailEmail) :
          message.summary === 'Invalid username or password' ? InvalidUsernameOrPassword : message.summary

        }}</span>
        <div
          v-if="message.detail"
          class="p-toast-detail text-color"
          data-pc-section="detail"
        >
          {{

          message.detail

          }}
        </div>
      </div>
    </template>
  </PToast>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const AccountWithGivenEmailDoesNotExist = returnTranslation(lang, 'AccountWithGivenEmailDoesNotExist');
const InvalidUsernameOrPassword = returnTranslation(lang, 'InvalidUsernameOrPassword');
const UnknownErrorInInputFields = returnTranslation(lang, 'UnknownErrorInInputFields');
const WorkspaceNotFound = returnTranslation(lang, 'WorkspaceNotFound');
const YouDoNotHavePermissionsToSearchWithinWorkspace = returnTranslation(lang, 'YouDoNotHavePermissionsToSearchWithinWorkspace');
const YouDoNotHavePermissions = returnTranslation(lang, 'YouDoNotHavePermissions');
const IsNotAEmailEmail = returnTranslation(lang, 'IsNotAEmailEmail');
const VersionMismatch = returnTranslation(lang, 'VersionMismatch');
const ProjectWithTheSameNameAlreadyExists = returnTranslation(lang, 'ProjectWithTheSameNameAlreadyExists');

import { ToastMessageOptions } from 'primevue/toast'

const icon = (severity: ToastMessageOptions['severity']) => {
  const mapper: Record<ToastMessageOptions['severity'], string> = {
    success: 'ti ti-circle-check-filled',
    info: 'ti ti-info-circle-filled',
    warn: 'ti ti-alert-triangle-filled',
    error: 'ti ti-alert-circle-filled'
  }

  return mapper[severity] || 'ti ti-alert-circle-filled'
}
</script>
