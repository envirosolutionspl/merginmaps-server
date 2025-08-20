<template>
  <app-container>
    <app-section>
      <template #title>Advanced</template>
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
              label="Delete project"
            />
          </div>
        </template>
      </app-settings>
    </app-section>
  </app-container>
</template>

<script lang="ts" setup>
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
    title: returnTranslation(import.meta.env.VITE_LANG, 'PublicProject'),
    description: returnTranslation(import.meta.env.VITE_LANG, 'TheProjectWillBeVisibleToEveryoneIfItIsMarkedAsPublic')
  },
  {
    key: 'deleteProject',
    title: returnTranslation(import.meta.env.VITE_LANG, 'DeleteProject'),
    description: returnTranslation(import.meta.env.VITE_LANG, 'DeletingThisProjectWillRemoveItAndAllItsDataThisActionCannotBeUndone')
  }
])

const confirmDelete = () => {
  const lang = import.meta.env.VITE_LANG
  const props: ConfirmDialogProps = {
    text: `Are you sure you want to permanently delete this project?`,
    description: `Deleting this project will remove it
      and all its data. This action cannot be undone. Type in project name to confirm:`,
    hint: project.value.name,
    confirmText: 'Delete permanently',
    confirmField: {
      label: 'Project name',
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
    params: { props, listeners, dialog: { header: returnTranslation(import.meta.env.VITE_LANG, 'DeleteProject') } }
  })
}
</script>
