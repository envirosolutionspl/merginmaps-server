<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <projects-list-view-template
    :namespace="namespace"
    :can-create-project="canCreateProject"
    @new-project-error="onNewProjectError"
  >
    <template #projects="{ onlyPublic }">
      <projects-table-data-loader
        :key="namespace + $route.name.toString()"
        :show-namespace="false"
        :namespace="namespace"
        :only-public="onlyPublic"
        :can-create-project="canCreateProject"
        @new-project-error="onNewProjectError"
      />
    </template>
  </projects-list-view-template>
</template>

<script lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG
import {
  ProjectsListViewTemplate,
  ProjectsTableDataLoader,
  useFormStore,
  useUserStore
} from '@mergin/lib'
import { computed, defineComponent } from 'vue'

export default defineComponent({
  name: 'ProjectsListView',
  components: {
    ProjectsListViewTemplate,
    ProjectsTableDataLoader
  },
  props: {
    namespace: String
  },
  setup() {
    const userStore = useUserStore()
    const formStore = useFormStore()

    const canCreateProject = computed(() => userStore.isGlobalWorkspaceAdmin)

    /**
     * Error handler for create new project from $emit in Template
     * */
    function onNewProjectError(err, data) {
      const lang = import.meta.env.VITE_LANG
      formStore.handleError({
        componentId: data.componentId,
        error: err,
        generalMessage: returnTranslation(lang, 'FailedToCreateProject')
      })
    }

    return {
      canCreateProject,
      onNewProjectError
    }
  }
})
</script>
