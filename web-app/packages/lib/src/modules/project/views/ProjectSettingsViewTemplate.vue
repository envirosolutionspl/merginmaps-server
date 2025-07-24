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
                >{{ ThisIsPublicProject }}</template
              >
              <template v-else>{{ ThisIsPrivateProject }}</template>
            </template>

            <template #description>
              <template v-if="project.access.public">
                {{ HideThisProjectFromEveryone }}
              </template>
              <template v-else>{{ MakeThisProjectVisibleToAnyone }}</template>
            </template>

            <template #action>
              <div class="flex-shrink-0">
                <PButton
                  @click="confirmPublicPrivate()"
                  severity="secondary"
                  data-cy="settings-public-btn"
                  :label="
                    project.access.public ? MakePrivate : MakePublic
                  "
                />
              </div>
            </template>
          </app-settings-item>
          <slot name="operations"></slot>
          <app-settings-item>
            <template #title>{{ DeleteProject }}</template>
            <template #description>{{ AllDataWillBeLost }}</template>
            <template #action
              ><div class="flex-shrink-0">
                <PButton
                  @click="confirmDelete"
                  severity="danger"
                  data-cy="settings-delete-btn"
                  :label="DeleteProject"
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

const ThisIsPublicProject = returnTranslation(lang, 'ThisIsPublicProject');
const ThisIsPrivateProject = returnTranslation(lang, 'ThisIsPrivateProject');
const HideThisProjectFromEveryone = returnTranslation(lang, 'HideThisProjectFromEveryone');
const MakePrivate = returnTranslation(lang, 'MakePrivate');
const MakePublic = returnTranslation(lang, 'MakePublic');
const DeleteProject = returnTranslation(lang, 'DeleteProject');
const AllDataWillBeLost = returnTranslation(lang, 'AllDataWillBeLost');

</script>

<script lang="ts">
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
    confirmDelete() { // returnTranslation(lang, 'AllDataWillBeLost')
      const lang = import.meta.env.VITE_LANG
      const props: ConfirmDialogProps = {
        text: returnTranslation(lang, 'AreYouSureToDeleteProject'),
        description: returnTranslation(lang, 'AllFilesWillBeLostTypeInProjectNameToConfirm'),
        hint: `${this.projectName}`,
        severity: 'danger',
        confirmText: returnTranslation(lang, 'Delete'),
        confirmField: {
          label: returnTranslation(lang, 'ProjectName'),
          expected: this.projectName
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
          dialog: { header: returnTranslation(lang, 'ConfirmDeleteProject') }
        }
      })
    },
    confirmPublicPrivate() {
      const lang = import.meta.env.VITE_LANG
      const DoYouReallyWantToMakeThisProject = returnTranslation(lang, 'DoYouReallyWantToMakeThisProject')
      const props: ConfirmDialogProps = {
        text: `${DoYouReallyWantToMakeThisProject} ${
          this.project?.access.public ? returnTranslation(lang, 'Private') : returnTranslation(lang, 'Public')
        }?`,
        confirmText: returnTranslation(lang, 'Yes'),
        cancelText: returnTranslation(lang, 'No'),
        description: this.project?.access.public
          ? returnTranslation(lang, 'OnceYouMakeYourProjectPrivateItCanNotBeAccessedByTheCommunity')
          : returnTranslation(lang, 'OnceYouMakeYourProjectPublicItCanBeAccessedByTheCommunity')
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
              ? returnTranslation(lang, 'PrivateProject')
              : returnTranslation(lang, 'PublicProject')
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
