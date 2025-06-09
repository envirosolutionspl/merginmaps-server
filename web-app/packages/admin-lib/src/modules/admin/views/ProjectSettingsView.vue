<template>
  <app-container>
    <app-section>
      <template #title>{{ Translation_Advanced }}</template>
      <app-settings :items="settingsItems">
        <template #publicProject>
          <div class="flex-shrink-0 paragraph-p1">
            <PInputSwitch :model-value="project?.access?.public" disabled />
          </div>
        </template>
        <template #deleteProject>
          <div class="flex-shrink-0">
            <PButton
              @click="confirmDelete"
              severity="danger"
              data-cy="project-delete-btn"
              :label="Translation_DeleteProject"
            />
          </div>
        </template>
      </app-settings>
    </app-section>
  </app-container>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_Advanced = returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_Advanced');
const Translation_DeleteProject = returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_DeleteProject');

import {
  AppContainer,
  AppSection,
  AppSettings,
  AppSettingsItemConfig,
  ConfirmDialog,
  ConfirmDialogProps,
  useDialogStore,
  useProjectStore
} from '@mergin/lib'
import { computed } from 'vue'

import { useAdminStore } from '@/modules/admin/store'

const projectStore = useProjectStore()
const dialogStore = useDialogStore()
const adminStore = useAdminStore()

const project = computed(() => projectStore.project)

const settingsItems = computed<AppSettingsItemConfig[]>(() => [
  {
    key: 'publicProject',
    title: returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_PublicProject'),
    description:
      returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_TheProjectWillBeVisibleToEveryone')
  },
  {
    key: 'deleteProject',
    title: returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_DeleteProject'),
    description:
      returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_DeletingThisProjectWillRemove')
  }
])

const confirmDelete = () => {
  const props: ConfirmDialogProps = {
    text: returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_AreYouSureYouWantToPermanentlyDelete'),
    description: returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_DeletingThisProjectWillRemoveIt'),
    hint: project.value.name,
    confirmText: returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_DeletePermanently'),
    confirmField: {
      label: returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_ProjectName'),
      expected: project.value.name
    },
    severity: 'danger'
  }
  const listeners = {
    confirm: async () =>
      await adminStore.deleteProject({ projectId: project.value.id })
  }
  dialogStore.show({
    component: ConfirmDialog,
    params: { props, listeners, dialog: { header: returnTranslation(lang, 'adminlib_admin_ProjectSettingsView_DeleteProject') } }
  })
}
</script>
