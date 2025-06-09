<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <div>
    <app-container>
      <app-section ground>
        <template #header>
          <h1 class="headline-h3">{{ Translation_Projects }}</h1>
        </template>
      </app-section>
    </app-container>
    <app-container>
      <app-section ground>
        <span class="p-input-icon-left w-full">
          <i class="ti ti-search paragraph-p3"></i>
          <PInputText
            :placeholder="
              showNamespace
                ? Translation_SearchByWorkspaceNameOrProjectName
                : Translation_SearchProjects
            "
            v-model="search"
            class="w-full"
            @input="onSearch"
          />
        </span>
      </app-section>
    </app-container>
    <app-container>
      <app-section>
        <PDataTable
          :value="projects.items"
          :lazy="true"
          :paginator="true"
          :rows="options.itemsPerPage"
          :rowsPerPageOptions="options.perPageOptions"
          :totalRecords="projects.count"
          :loading="projects.loading"
          :first="(options.page - 1) * options.itemsPerPage"
          :sortField="options.sortBy[0]"
          :sortOrder="options.sortDesc[0] ? -1 : 1"
          removableSort
          reorderable-columns
          @page="onPage"
          @sort="onSort"
          @row-click="rowClick"
          data-cy="projects-table"
          :row-class="(data) => (data.removed_at ? 'opacity-80' : '')"
        >
          <template v-for="header in headers" :key="header.field">
            <PColumn
              v-if="showNamespace && header.field === 'workspace'"
              :field="header.field"
              :header="header.header"
              :sortable="header.sortable"
            >
              <template #body="slotProps">
                {{ slotProps.data.workspace }}
              </template>
            </PColumn>

            <PColumn
              v-else-if="header.field === 'name'"
              :field="header.field"
              :header="header.header"
              :sortable="header.sortable"
            >
              <template #body="slotProps">
                <template v-if="slotProps.data.removed_at">{{
                  slotProps.data.name
                }}</template>
                <router-link
                  v-else
                  :to="{
                    name: 'project',
                    params: {
                      namespace: slotProps.data.workspace,
                      projectName: slotProps.data.name
                    }
                  }"
                  class="font-semibold"
                >
                  {{ slotProps.data.name }}
                </router-link>
              </template>
            </PColumn>

            <PColumn
              v-else-if="header.field === 'updated'"
              :field="header.field"
              :header="header.header"
              :sortable="header.sortable"
            >
              <template #body="slotProps">
                <span :title="$filters.datetime(slotProps.data.updated)">
                  {{ $filters.timediff(slotProps.data.updated) }}
                </span>
              </template>
            </PColumn>

            <PColumn
              v-else-if="header.field === 'disk_usage'"
              :field="header.field"
              :header="header.header"
              :sortable="header.sortable"
            >
              <template #body="slotProps">
                {{ $filters.filesize(slotProps.data.disk_usage, 'MB') }}
              </template>
            </PColumn>

            <PColumn
              v-else-if="header.field === 'removed_at'"
              :field="header.field"
              :header="header.header"
              :sortable="header.sortable"
            >
              <template #body="slotProps">
                <span
                  :title="`${Translation_ScheduledForRemovalAt} ${$filters.datetime(
                    slotProps.data.removed_at
                  )}`"
                >
                  {{ $filters.timediff(slotProps.data.removed_at) }}
                </span>
              </template>
            </PColumn>

            <PColumn v-else-if="header.field === 'buttons'">
              <template #body="slotProps">
                <div
                  class="justify-center px-0"
                  v-if="slotProps.data.removed_at"
                >
                  <div class="flex align-items-center gap-1">
                    <PButton
                      :label="Translation_Restore"
                      severity="secondary"
                      size="small"
                      @click="confirmRestore(slotProps.data)"
                    />
                    <PButton
                      :label="Translation_Delete"
                      severity="danger"
                      size="small"
                      @click="confirmDelete(slotProps.data)"
                    />
                  </div>
                </div>
              </template>
            </PColumn>

            <PColumn
              v-else
              :field="header.field"
              :header="header.header"
              :sortable="header.sortable"
            ></PColumn>
          </template>
          <template #paginatorstart>
            <PButton
              icon="ti ti-refresh"
              plain
              text
              rounded
              size="small"
              @click="onRefresh"
            />
          </template>
          <template #paginatorend />
        </PDataTable>
      </app-section>
    </app-container>
  </div>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_Projects = returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_Projects');
const Translation_SearchByWorkspaceNameOrProjectName = returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_SearchByWorkspaceNameOrProjectName');
const Translation_SearchProjects = returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_SearchProjects');
const Translation_ScheduledForRemovalAt = returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_ScheduledForRemovalAt');
const Translation_Restore = returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_Restore');
const Translation_Delete = returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_Delete');
</script>

<script lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG
import {
  ConfirmDialog,
  useDialogStore,
  useNotificationStore,
  SortingOptions,
  TableDataHeader,
  AppSection,
  AppContainer,
  ConfirmDialogProps
} from '@mergin/lib'
import { mapActions, mapState } from 'pinia'
import {
  DataTablePageEvent,
  DataTableRowClickEvent,
  DataTableSortEvent
} from 'primevue/datatable'
import { PropType, defineComponent } from 'vue'

import { AdminRoutes, useAdminStore } from '@/main'

export default defineComponent({
  name: 'projects-table',
  components: {
    AppContainer,
    AppSection
  },
  props: {
    showNamespace: Boolean,
    initialOptions: {
      type: Object as PropType<SortingOptions>,
      default: () => ({
        sortBy: ['updated'],
        sortDesc: [true],
        itemsPerPage: 20,
        page: 1,
        perPageOptions: [20, 50, 100]
      })
    }
  },
  data() {
    return {
      options: Object.assign({}, this.initialOptions),
      search: ''
    }
  },
  computed: {
    ...mapState(useAdminStore, ['projects']),
    headers(): TableDataHeader[] {
      return [
        ...(this.showNamespace
          ? [
              {
                header: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_Workspace'),
                field: 'workspace',
                sortable: true
              }
            ]
          : []),
        { header: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_Name'), field: 'name', sortable: true },
        { header: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_LastUpdate'), field: 'updated', sortable: true },
        { header: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_Size'), field: 'disk_usage', sortable: true },
        { header: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_ScheduledRemovalAt'), field: 'removed_at', sortable: true },
        { header: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_RemovedBy'), field: 'removed_by', sortable: true },
        { header: '', field: 'buttons', sortable: false }
      ]
    }
  },
  created() {
    this.resetPaging()
    this.fetchProjects()
  },
  methods: {
    ...mapActions(useDialogStore, { showDialog: 'show' }),
    ...mapActions(useNotificationStore, ['error', 'show']),
    ...mapActions(useAdminStore, [
      'getProjects',
      'restoreProject',
      'deleteProject'
    ]),

    paginating(options) {
      this.options = options
      this.fetchProjects()
    },

    async resetPaging() {
      this.options.page = 1
    },

    fetchProjects() {
      this.getProjects({ params: { ...this.options, like: this.search } })
    },

    onSearch() {
      this.resetPaging()
      this.fetchProjects()
    },

    onPage(event: DataTablePageEvent) {
      this.options.page = event.page + 1
      this.options.itemsPerPage = event.rows
      this.fetchProjects()
    },

    onSort(event: DataTableSortEvent) {
      this.options.sortBy[0] = event.sortField?.toString()
      this.options.sortDesc[0] = event.sortOrder < 1
      this.fetchProjects()
    },

    rowClick(event: DataTableRowClickEvent) {
      if (event.data.removed_at) return

      this.$router.push({
        name: AdminRoutes.PROJECT,
        params: {
          namespace: event.data.workspace,
          projectName: event.data.name
        }
      })
    },

    confirmRestore(item) {
      const props: ConfirmDialogProps = {
        text: `${returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_AreYouSureToRestoreProject')} ${item.workspace}/${item.name}?`,
        confirmText: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_Restore')
      }
      const listeners = {
        confirm: async () => {
          await this.restoreProject({ projectId: item.id })
          this.fetchProjects()
        }
      }
      this.showDialog({
        component: ConfirmDialog,
        params: { props, listeners, dialog: { header: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_RestoreProject') } }
      })
    },

    confirmDelete(item) {
      const props: ConfirmDialogProps = {
        text: returnTranslation(lang, 'AreYouSureYouWantToPermanentlyDeleteThisProject'),
        description: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_DeletingThisProjectWillRemoveItAndAllItsData'),
        hint: item.name,
        confirmText: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_DeletePermanently'),
        confirmField: {
          label: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_ProjectName'),
          expected: item.name
        },
        severity: 'danger'
      }
      const listeners = {
        confirm: async () => {
          await this.deleteProject({ projectId: item.id })
          this.fetchProjects()
        }
      }
      this.showDialog({
        component: ConfirmDialog,
        params: { props, listeners, dialog: { header: returnTranslation(lang, 'adminlib_admin_AdminProjectsTable_DeleteProject') } }
      })
    },

    onRefresh() {
      this.fetchProjects()
    }
  }
})
</script>

<style lang="scss" scoped></style>
