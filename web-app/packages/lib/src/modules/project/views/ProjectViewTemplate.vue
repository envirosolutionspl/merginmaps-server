<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <div>
    <template v-if="project">
      <app-container
        class="project-view-actions flex justify-content-start lg:justify-content-end"
      >
        <!-- Z indexes based on minus margin, its not possible to add additional buttons to tab view -->
        <div class="relative z-1">
          <PButton
            severity="secondary"
            @click="downloadArchive({ url: downloadUrl })"
            data-cy="project-download-btn"
            icon="ti ti-download"
            class="mr-2"
            :label="Download"
          />
          <PButton
            severity="secondary"
            @click="cloneDialog"
            v-if="canCloneProject"
            data-cy="project-clone-btn"
            icon="ti ti-copy"
            :label="Clone"
            class="mr-2"
          />
          <PButton
            severity="secondary"
            @click="leaveDialog"
            data-cy="project-leave-btn"
            icon="ti ti-logout"
            :label="LeaveProject"
            v-if="canLeaveProject"
          />
        </div>
      </app-container>

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
        <PTabPanel :header="tabs[0].header"></PTabPanel>
        <slot name="map.tab" />
        <!-- Render other tabs with header -->
        <PTabPanel
          v-for="tab in tabs.slice(1).filter((item) => item.header)"
          :header="tab.header"
          :key="tab.route"
        ></PTabPanel>
      </PTabView>
      <router-view />
    </template>
    <app-container v-else-if="fetchProjectsResponseStatus">
      <app-section v-if="fetchProjectsResponseStatus === 403">
        <div class="flex flex-column align-items-center p-4 text-center gap-4">
          <img src="@/assets/map-circle.svg" alt="No project" />
          <p class="font-semibold">{{ ThisIsAPrivateProject }}</p>
          <p class="paragraph-p5 opacity-80 mt-2 mb-4">
            {{ YouDontHavePermissionsToAccessThisProject }}
          </p>
          <PButton id="request-access-btn" @click="createAccessRequest"
            >{{ RequestAccess }}</PButton
          >
        </div>
      </app-section>
      <app-section v-else-if="fetchProjectsResponseStatus === 404">
        <div class="flex flex-column align-items-center p-4 text-center gap-4">
          <img src="@/assets/map-circle.svg" alt="No project" />
          <p class="font-semibold">{{ ProjectNotFound }}</p>
          <p class="paragraph-p5 opacity-80 mt-2 mb-4">
            {{ PleaseCheckFfAddressIsWrittenCorrectly }}
          </p>
        </div>
      </app-section>
      <app-section v-else-if="fetchProjectsResponseStatus === 409">
        <div class="flex flex-column align-items-center p-4 text-center gap-4">
          <img src="@/assets/map-circle.svg" alt="No project" />
          <p class="font-semibold">
            {{ YouDontHavePermissionsToAccessThisProject }}
          </p>
          <p class="paragraph-p5 opacity-80 mt-2 mb-4">
            {{ YouAlreadyRequestedAccess }}
          </p>
        </div>
      </app-section>
    </app-container>
    <slot name="right">
      <upload-dialog v-if="upload" :namespace="namespace" />
    </slot>
  </div>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Download = returnTranslation(lang, 'Download');
const Clone = returnTranslation(lang, 'Clone');
const LeaveProject = returnTranslation(lang, 'LeaveProject');
const ThisIsAPrivateProject = returnTranslation(lang, 'ThisIsAPrivateProject');
const YouDontHavePermissionsToAccessThisProject = returnTranslation(lang, 'YouDontHavePermissionsToAccessThisProject');
const RequestAccess = returnTranslation(lang, 'RequestAccess');
const ProjectNotFound = returnTranslation(lang, 'ProjectNotFound');
const PleaseCheckFfAddressIsWrittenCorrectly = returnTranslation(lang, 'PleaseCheckFfAddressIsWrittenCorrectly');
const YouAlreadyRequestedAccess = returnTranslation(lang, 'YouAlreadyRequestedAccess');

</script>

<script lang="ts">
import { mapActions, mapState } from 'pinia'
import { defineComponent, PropType } from 'vue'

import { AppContainer, AppSection } from '@/common'
import { waitCursor } from '@/common/html_utils'
import {
  USER_ROLE_NAME_BY_ROLE,
  WorkspaceRole
} from '@/common/permission_utils'
import { ConfirmDialogProps, ProjectRouteName } from '@/modules'
import ConfirmDialog from '@/modules/dialog/components/ConfirmDialog.vue'
import { useDialogStore } from '@/modules/dialog/store'
import { useLayoutStore } from '@/modules/layout/store'
import { useNotificationStore } from '@/modules/notification/store'
import UploadDialog from '@/modules/project/components/UploadDialog.vue'
import { ProjectApi } from '@/modules/project/projectApi'
import { useProjectStore } from '@/modules/project/store'
import { useUserStore } from '@/modules/user/store'

interface TabItem {
  route: string
  header?: string
}

export default defineComponent({
  name: 'ProjectViewTemplate',
  components: {
    UploadDialog,
    AppContainer,
    AppSection
  },
  props: {
    namespace: String,
    projectName: String,
    showSettings: Boolean as PropType<boolean>,
    showHistory: { type: Boolean as PropType<boolean>, default: true },
    hideCloneButton: {
      type: Boolean,
      default: false
    },
    mapRoute: String
  },
  data() {
    return {
      fetchProjectsResponseStatus: null,
      tab: null,
      value: 'read'
    }
  },
  computed: {
    ...mapState(useLayoutStore, ['drawer']),
    ...mapState(useProjectStore, ['project', 'uploads']),
    ...mapState(useUserStore, ['loggedUser']),
    ...mapState(useProjectStore, ['isProjectOwner']),
    ...mapState(useUserStore, ['currentWorkspace', 'isLoggedIn']),

    tabs(): TabItem[] {
      const tabs: TabItem[] = [
        {
          route: ProjectRouteName.ProjectTree,
          header: returnTranslation(lang, 'Files')
        }
      ]

      if (this.loggedUser) {
        // If map in slots, add route to map tab
        if (this.$slots['map.tab']) {
          tabs.push({
            route: this.mapRoute
          })
        }
        if (this.showHistory) {
          tabs.push({
            route: ProjectRouteName.ProjectHistory,
            header: returnTranslation(lang, 'History')
          })
        }
        if (this.showSettings) {
          tabs.push({
            route: ProjectRouteName.ProjectCollaborators,
            header: returnTranslation(lang, 'Collaborators')
          })
          tabs.push({
            route: ProjectRouteName.ProjectSettings,
            header: returnTranslation(lang, 'Settings')
          })
        }
      }
      return tabs
    },

    activeTabIndex(): number {
      return this.tabs.findIndex((item) =>
        this.$route.matched.some((m) => m.name === item.route)
      )
    },

    canCloneProject() {
      return this.isLoggedIn && !this.hideCloneButton
    },

    canShareProject() {
      return (
        this.project?.workspace_id === this.currentWorkspace?.id &&
        this.isProjectOwner
      )
    },

    canLeaveProject() {
      return (
        this.project?.workspace_id === this.currentWorkspace?.id &&
        this.currentWorkspace?.role ===
          USER_ROLE_NAME_BY_ROLE[WorkspaceRole.guest]
      )
    },

    upload() {
      return this.project && this.uploads[this.project.path]
    },
    downloadUrl() {
      if (this.$route.name === 'project-versions-detail') {
        return ProjectApi.constructDownloadProjectVersionUrl(
          this.namespace,
          this.projectName,
          this.$route.params.version_id as string
        )
      } else {
        return this.constructDownloadProjectUrl({
          namespace: this.namespace,
          projectName: this.projectName
        })
      }
    }
  },
  async created() {
    if (
      !this.project ||
      this.project.name !== this.projectName ||
      this.project.namespace !== this.namespace
    ) {
      this.setProject({ project: null })
      await this.getProject()
    }
  },
  watch: {
    project() {
      if (
        !this.project ||
        this.project.name !== this.projectName ||
        this.project.namespace !== this.namespace
      ) {
        this.setProject({ project: null })
        this.getProject()
      }
    }
  },
  methods: {
    ...mapActions(useProjectStore, [
      'downloadArchive',
      'fetchProjectDetail',
      'unsubscribeProject',
      'constructDownloadProjectUrl'
    ]),
    ...mapActions(useProjectStore, ['setProject']),
    ...mapActions(useDialogStore, { showDialog: 'show' }),
    ...mapActions(useNotificationStore, ['error', 'show']),

    setFetchProjectResponseStatus(status) {
      this.fetchProjectsResponseStatus = status
    },
    async getProject() {
      this.fetchProjectDetail({
        callbackStatus: this.setFetchProjectResponseStatus,
        projectName: this.projectName,
        namespace: this.namespace,
        isLoggedUser: !!this.loggedUser
      })
    },
    cloneDialog() {
      this.$emit('open-clone-dialog')
    },
    createAccessRequest() {
      waitCursor(true)
      ProjectApi.createProjectAccessRequest(
        this.namespace,
        this.projectName,
        true
      )
        .then(() => {
          waitCursor(false)
          this.show({
            text: returnTranslation(lang, 'AccessHasBeenRequested')
          })
          this.$router.push({
            name: 'projects'
          })
        })
        .catch(() => {
          this.error({
            text: returnTranslation(lang, 'FailedToRequest')
          })
          waitCursor(false)
        })
    },
    leaveDialog() {

      const AreYouSureToLeaveTheProject = returnTranslation(lang, 'AreYouSureToLeaveTheProject');
      const YouWillNotHaveAccessToItAnymore = returnTranslation(lang, 'YouWillNotHaveAccessToItAnymore');
      const Yes = returnTranslation(lang, 'Yes');
      const No = returnTranslation(lang, 'No');

      const props: ConfirmDialogProps = {
        text: `${AreYouSureToLeaveTheProject} ${this.projectName}?`,
        description: YouWillNotHaveAccessToItAnymore,
        severity: 'danger',
        confirmText: Yes,
        cancelText: No
      }
      const listeners = {
        confirm: async () => {
          await this.unsubscribeProject({ id: this.project.id })
          if (!this.project) {
            await this.$router.push('/dashboard')
          }
        }
      }
      const LeaveProject = returnTranslation(lang, 'LeaveProject');
      this.showDialog({
        component: ConfirmDialog,
        params: {
          props,
          listeners,
          dialog: { header: LeaveProject }
        }
      })
    },

    /**
     * Handles clicking on a tab by index.
     *
     * @param index - The index of the clicked tab.
     */
    tabClick(index: number) {
      this.$router.push({
        name: this.tabs[index].route,
        query: {}
      })
    }
  }
})
</script>

<style lang="scss" scoped>
.project-view-actions {
  margin-bottom: -2.75rem;
}

@media screen and (max-width: $lg) {
  .project-view-actions {
    margin-bottom: 0px;
  }
}
</style>
