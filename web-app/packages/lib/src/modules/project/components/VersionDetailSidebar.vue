<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <div v-if="version">
    <app-sidebar-right v-model="sidebarVisible" data-cy="app-right-sidebar">
      <template #title>{{ queryId }}</template>
      <template #headerButtons
        ><PButton
          type="button"
          @click="downloadVersion"
          icon="ti ti-download"
          text
          rounded
          plain
          class="p-1 text-2xl"
          data-cy="file-detail-download-btn"
        ></PButton
      ></template>
      <dl class="grid grid-nogutter row-gap-4">
        <div class="col-12">
          <dt class="paragraph-p6 opacity-80">{{ Translation_Version }}</dt>
          <dd>
            <h3 class="headline-h3 mt-0">
              {{ version.name }}
            </h3>
          </dd>
        </div>
        <PDivider class="m-0" />
        <div class="col-6">
          <dt class="paragraph-p6 opacity-80">{{ Translation_Author }}</dt>
          <dd class="font-semibold paragraph-p5">
            {{ version.author }}
          </dd>
        </div>
        <div class="col-6 flex flex-column align-items-end">
          <dt class="paragraph-p6 opacity-80">{{ Translation_ProjectSize }}</dt>
          <dd class="font-semibold paragraph-p5">
            {{ $filters.filesize(version.project_size) }}
          </dd>
        </div>
        <div class="col-12">
          <dt class="paragraph-p6 opacity-80">{{ Translation_Created }}</dt>
          <dd class="font-semibold paragraph-p5">
            {{ $filters.datetime(version.created) }}
          </dd>
        </div>
        <div class="col-12">
          <dt class="paragraph-p6 opacity-80">{{ Translation_UserAgent }}</dt>
          <dd class="font-semibold paragraph-p5">
            {{ version.user_agent }}
          </dd>
        </div>
      </dl>
      <project-version-changes v-if="version" :version="version" />
    </app-sidebar-right>
  </div>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_Version = returnTranslation(lang, 'lib_project_VersionDetailSidebar_Version');
const Translation_Author = returnTranslation(lang, 'lib_project_VersionDetailSidebar_Author');
const Translation_ProjectSize = returnTranslation(lang, 'lib_project_VersionDetailSidebar_ProjectSize');
const Translation_Created = returnTranslation(lang, 'lib_project_VersionDetailSidebar_Created');
const Translation_UserAgent = returnTranslation(lang, 'lib_project_VersionDetailSidebar_UserAgent');

</script>

<script lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG
import { mapActions, mapState } from 'pinia'
import { defineComponent } from 'vue'

import ProjectVersionChanges from './ProjectVersionChanges.vue'

import AppSidebarRight from '@/common/components/AppSidebarRight.vue'
import { getErrorMessage } from '@/common/error_utils'
import { ProjectVersion } from '@/modules'
import { useNotificationStore } from '@/modules/notification/store'
import { ProjectApi } from '@/modules/project/projectApi'
import { useProjectStore } from '@/modules/project/store'

export default defineComponent({
  name: 'VersionDetailSidebar',
  components: { AppSidebarRight, ProjectVersionChanges },
  data() {
    return {
      version: null as ProjectVersion
    }
  },
  computed: {
    ...mapState(useProjectStore, ['project', 'versions']),
    queryId(): string {
      return this.$route.query.version_id as string
    },
    sidebarVisible: {
      get() {
        return !!this.queryId
      },
      set(visible: boolean) {
        if (visible) {
          this.sidebarVisible = visible
        } else {
          this.$router.replace({ query: undefined })
        }
      }
    }
  },
  watch: {
    queryId: {
      immediate: true,
      handler() {
        if (this.queryId) {
          this.getVersion()
          return
        }
        this.sidebarVisible = false
      }
    }
  },
  methods: {
    ...mapActions(useNotificationStore, ['error']),
    ...mapActions(useProjectStore, ['downloadArchive']),
    async getVersion() {
      try {
        const response = await ProjectApi.getProjectVersion(
          this.project.id,
          this.queryId
        )
        this.version = response.data
      } catch (err) {
        this.error({
          text: getErrorMessage(err, returnTranslation(lang, 'lib_project_VersionDetailSidebar_FailedToFetchProjectVersion'))
        })
      }
    },
    downloadVersion() {
      const url = ProjectApi.constructDownloadProjectVersionUrl(
        this.project.id,
        this.queryId
      )
      this.downloadArchive({ url, versionId: this.queryId })
    }
  }
})
</script>

<style lang="scss" scoped></style>
