<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <div>
    <app-container>
      <app-section class="pt-4">
        <app-settings>
          <app-settings-item>
            <template #title>
              <template v-if="project.access.public"
                >{{ Translation_ThisIsPublicProject }}</template
              >
              <template v-else>{{ Translation_ThisIsPrivateProject }}</template>
            </template>

            <template #description>
              <template v-if="project.access.public">
                {{ Translation_HideThisProjectFromEveryone }}
              </template>
              <template v-else>{{ Translation_MakeThisProjectVisibleToAnyone }}</template>
            </template>

            <template #action>
              <div class="flex-shrink-0">
                <PButton
                  @click="confirmPublicPrivate()"
                  severity="secondary"
                  data-cy="settings-public-btn"
                  :label="
                    project.access.public ? Translation_MakePrivate : Translation_MakePublic
                  "
                />
              </div>
            </template>
          </app-settings-item>
          <slot name="operations"></slot>
          <app-settings-item>
            <template #title>{{ Translation_DeleteProject }}</template>
            <template #description>{{ Translation_AllDataWillBeLost }}</template>
            <template #action
              ><div class="flex-shrink-0">
                <PButton
                  @click="confirmDelete"
                  severity="danger"
                  data-cy="settings-delete-btn"
                  :label="Translation_DeleteProject"
                /></div
            ></template>
          </app-settings-item>
        </app-settings>
      </app-section>
    </app-container>
  </div>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_ThisIsPublicProject = returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_ThisIsPublicProject');
const Translation_ThisIsPrivateProject = returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_ThisIsPrivateProject');
const Translation_HideThisProjectFromEveryone = returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_HideThisProjectFromEveryone');
const Translation_MakeThisProjectVisibleToAnyone = returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_MakeThisProjectVisibleToAnyone');
const Translation_MakePrivate = returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_MakePrivate');
const Translation_MakePublic = returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_MakePublic');
const Translation_DeleteProject = returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_DeleteProject');
const Translation_AllDataWillBeLost = returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_AllDataWillBeLost');


</script>

<script lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

import { mapActions, mapState } from 'pinia'
import { PropType, defineComponent } from 'vue'

import AppSettings from '@/common/components/app-settings/AppSettings.vue'
import AppSettingsItem from '@/common/components/app-settings/AppSettingsItem.vue'
import AppContainer from '@/common/components/AppContainer.vue'
import AppSection from '@/common/components/AppSection.vue'
import { ConfirmDialogProps } from '@/modules'
import ConfirmDialog from '@/modules/dialog/components/ConfirmDialog.vue'
import { useDialogStore } from '@/modules/dialog/store'
import { useProjectStore } from '@/modules/project/store'

export default defineComponent({
  name: 'ProjectSettingsViewTemplate',
  components: {
    AppContainer,
    AppSection,
    AppSettings,
    AppSettingsItem
  },
  props: {
    projectName: String,
    showSettings: Boolean,
    showAccessRequests: {
      type: Boolean as PropType<boolean>,
      default: false
    }
  },
  computed: {
    ...mapState(useProjectStore, ['project', 'accessRequestsCount'])
  },
  created() {
    if (!this.showSettings) {
      this.$router.push('/projects')
    }
  },
  methods: {
    ...mapActions(useProjectStore, ['deleteProject', 'updatePublicFlag']),
    ...mapActions(useDialogStore, { showDialog: 'show' }),
    togglePublicPrivate() {
      this.updatePublicFlag({
        projectId: this.project.id,
        data: {
          public: !this.project.access.public
        }
      })
    },
    confirmDelete() {
      const props: ConfirmDialogProps = {
        text: returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_AreYouSureToDeleteProject'),
        description: returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_AllFilesWillBeLost'),
        hint: `${this.projectName}`,
        severity: 'danger',
        confirmText: returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_Delete'),
        confirmField: {
          label: returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_ProjectName'),
          expected: this.projectName,
          placeholder: returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_TypeInProjectNameToConfirmDeletion')
        }
      }
      const listeners = {
        confirm: () => this.onDeleteProject()
      }
      this.showDialog({
        component: ConfirmDialog,
        params: {
          props,
          listeners,
          dialog: { header: returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_ConfirmDeleteProject') }
        }
      })
    },
    confirmPublicPrivate() {
      const props: ConfirmDialogProps = {
        text: `${returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_DoYouReallyWantToMakeThisProject')} ${
          this.project?.access.public ? returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_Private') : returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_Public')
        }?`,
        confirmText: returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_Yes'),
        cancelText: returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_No'),
        description: this.project?.access.public
          ? returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_OnceYouMakeYourProjectPrivate')
          : returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_OnceYouMakeYourProjectPublic')
      }
      const listeners = {
        confirm: () => this.togglePublicPrivate()
      }
      this.showDialog({
        component: ConfirmDialog,
        params: {
          props,
          listeners,
          dialog: {
            header: this.project?.access.public
              ? returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_PrivateProject')
              : returnTranslation(lang, 'lib_project_ProjectSettingsViewTemplate_PublicProject')
          }
        }
      })
    },
    onDeleteProject() {
      this.deleteProject({
        projectId: this.project.id
      })
    }
  }
})
</script>

<style lang="scss" scoped></style>
