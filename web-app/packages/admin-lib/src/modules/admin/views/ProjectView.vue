<template>
  <admin-layout v-if="project">
    <app-container>
      <app-section ground>
        <template #header>
          <h1 class="headline-h3">{{ Translation_ProjectDetails }}</h1>
        </template>
        <template #headerActions>
          <PButton
            severity="secondary"
            @click="downloadArchive"
            data-cy="project-download-btn"
            icon="ti ti-download"
            class="mr-2"
            :label="Translation_Download"
            :disabled="projectStore.projectDownloading"
          />
          <PButton
            severity="secondary"
            @click="openDashboard"
            data-cy="project-dashboard"
            icon="ti ti-external-link"
            :label="Translation_OpenInDashboard"
          />
        </template>
      </app-section>
    </app-container>

    <app-container>
      <app-section class="p-4">
        <div class="flex flex-column row-gap-3">
          <h2 class="headline-h2" data-cy="project-name">
            <template v-if="showWorkspaceName"
              ><router-link
                :to="{
                  name: 'adminWorkspace',
                  params: { id: project?.workspace_id }
                }"
              >
                {{ project?.namespace }}
              </router-link>
              / </template
            >{{ project?.name }}
          </h2>
          <dl
            class="project-view-detail-list paragraph-p5 flex flex-column gap-3"
          >
            <div>
              <dt class="paragraph-p6 opacity-80">{{ Translation_Created }}</dt>
              <dd class="font-semibold" data-cy="project-owner">
                {{ $filters.datetime(project?.created) }}
              </dd>
            </div>
            <div>
              <dt class="paragraph-p6 opacity-80">{{ Translation_Updated }}</dt>
              <dd class="font-semibold" data-cy="project-created">
                {{ $filters.datetime(project?.updated) }}
              </dd>
            </div>
            <div>
              <dt class="paragraph-p6 opacity-80">{{ Translation_DiskUsage }}</dt>
              <dd class="font-semibold" data-cy="project-created">
                {{ $filters.filesize(project?.disk_usage, 'MB') }}
              </dd>
            </div>
          </dl>
        </div>
      </app-section>
    </app-container>

    <app-container>
      <PTabView
        :active-index="activeTabIndex"
        @tab-click="(e) => tabClick(e.index)"
        data-cy="project-tab-nav"
        :pt="{
          root: {
            class: 'relative z-auto'
          },
          nav: {
            style: {
              backgroundColor: 'transparent',
              maxWidth: '1120px'
            },
            class: 'mx-auto px-3 lg:px-0 border-transparent'
          },
          panelContainer: {
            style: {
              backgroundColor: 'transparent'
            },
            class: 'py-0 px-3'
          }
        }"
      >
        <PTabPanel
          v-for="tab in tabs"
          :header="tab.header"
          :key="tab.route"
        ></PTabPanel>
      </PTabView>
      <router-view />
    </app-container>
    <download-progress />
    <download-file-large />
  </admin-layout>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_ProjectDetails = returnTranslation(lang, 'adminlib_admin_ProjectView_ProjectDetails');
const Translation_Download = returnTranslation(lang, 'adminlib_admin_ProjectView_Download');
const Translation_OpenInDashboard = returnTranslation(lang, 'adminlib_admin_ProjectView_OpenInDashboard');
const Translation_Created = returnTranslation(lang, 'adminlib_admin_ProjectView_Created');
const Translation_Updated = returnTranslation(lang, 'adminlib_admin_ProjectView_Updated');
const Translation_DiskUsage = returnTranslation(lang, 'adminlib_admin_ProjectView_DiskUsage');


import {
  AppSection,
  AppContainer,
  useProjectStore,
  ProjectApi,
  DownloadProgress,
  DownloadFileLarge
} from '@mergin/lib'
import { computed, watch, defineProps } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import { AdminRoutes } from '@/modules'
import AdminLayout from '@/modules/admin/components/AdminLayout.vue'

interface TabItem {
  route: string
  header?: string
}

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()

defineProps<{
  projectName: string
  namespace: string
}>()

const tabs = computed(() => {
  const tabs: TabItem[] = [
    {
      route: AdminRoutes.ProjectTree,
      header: returnTranslation(lang, 'adminlib_admin_ProjectView_Files')
    },
    {
      route: AdminRoutes.ProjectHistory,
      header: returnTranslation(lang, 'adminlib_admin_ProjectView_History')
    },
    {
      route: AdminRoutes.ProjectSettings,
      header: returnTranslation(lang, 'adminlib_admin_ProjectView_Settings')
    }
  ]
  return tabs
})

const project = computed(() => projectStore.project)
const routeProjectName = computed(() => route?.params?.projectName as string)
const routeWorkspaceName = computed(() => route?.params?.namespace as string)
const activeTabIndex = computed((): number => {
  const index = tabs.value.findIndex((item) =>
    route.matched.some((m) => m.name === item.route)
  )
  return index >= 0 ? index : 0
})
// TODO: prevent hardcoded route names from hasRoute checks
const showWorkspaceName = computed(
  () => router.hasRoute('adminWorkspace') && project.value?.workspace_id
)

const fetchProject = (projectName: string, workspaceName: string) => {
  projectStore.project = null
  projectStore.fetchProject({
    namespace: workspaceName,
    projectName
  })
}

watch(
  [routeProjectName, routeWorkspaceName],
  ([projectName, workspaceName]) => {
    if (projectName && workspaceName) {
      fetchProject(projectName, workspaceName)
    }
  },
  { immediate: true }
)

/**
 * Handles clicking on a tab by index.
 *
 * @param index - The index of the clicked tab.
 */
function tabClick(index: number) {
  router.push({
    name: tabs.value?.[index]?.route,
    params: {
      projectName: routeProjectName.value,
      namespace: routeWorkspaceName.value
    }
  })
}

function downloadArchive() {
  const url = ProjectApi.constructDownloadProjectUrl(project.value?.id)
  projectStore.downloadArchive({ url })
}

function openDashboard() {
  window.open(
    `/projects/${project.value?.namespace}/${project.value?.name}`,
    '_blank'
  )
}
</script>

<style lang="scss" scoped>
.project-view-detail-list {
  max-width: 640px;
  width: 100%;
}
</style>
