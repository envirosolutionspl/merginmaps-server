<template>
  <app-container>
    <app-section>
      <template #title>{{ Advanced }}</template>
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
              :label="DeleteProject"
            />
          </div>
        </template>
      </app-settings>
    </app-section>
  </app-container>
</template>

<script lang="ts" setup>
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Advanced = returnTranslation(lang, 'Advanced');
const DeleteProject = returnTranslation(lang, 'DeleteProject');

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
    title: returnTranslation(lang, 'PublicProject'),
    description: returnTranslation(lang, 'TheProjectWillBeVisibleToEveryoneIfItIsMarkedAsPublic')
  },
  {
    key: 'deleteProject',
    title: returnTranslation(lang, 'DeleteProject'),
    description: returnTranslation(lang, 'DeletingThisProjectWillRemoveItAndAllItsDataThisActionCannotBeUndone')
  }
])

const confirmDelete = () => {
  const props: ConfirmDialogProps = {
    text: returnTranslation(lang, 'AreYouSureYouWantToPermanentlyDeleteThisProject'),
    description: returnTranslation(lang, 'DeletingThisProjectWillRemoveItAndAllItsDataThisActionCannotBeUndoneTypeInProjectNameToConfirm'),
    hint: project.value.name,
    confirmText: returnTranslation(lang, 'DeletePermanently'),
    confirmField: {
      label: returnTranslation(lang, 'ProjectName'),
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
    params: { props, listeners, dialog: { header: returnTranslation(lang, 'DeleteProject') } }
  })
}
</script>
