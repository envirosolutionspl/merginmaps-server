<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <div class="py-4">
    <div class="mb-4">
      <span class="flex p-float-label w-full p-input-filled">
        <PInputText
          autofocus
          id="name"
          v-model="name"
          type="text"
          :class="{ 'p-invalid': errors.detail }"
          aria-describedby="text-error"
          data-cy="project-form-name"
          class="flex-grow-1"
        />
        <label for="name">{{ Translation_ProjectName }}</label>
        <small class="p-error" id="text-error">{{
          errors.detail || '&nbsp;'
        }}</small>
      </span>
    </div>

    <tip-message class="mb-6">
      ><template #description
        >{{ Translation_AGoodCandidateForAProjectName }}</template
      ></tip-message
    >

    <div
      class="flex flex-column lg:flex-row justify-content-between align-items-center"
    >
      <PButton
        severity="secondary"
        @click="close"
        class="flex w-12 mb-2 lg:mb-0 lg:mr-2 lg:w-6 justify-content-center"
        >{{ Translation_Cancel }}</PButton
      >

      <PButton
        id="create-project-btn"
        :disabled="!name"
        @click="create"
        data-cy="project-form-create-btn"
        class="flex w-12 lg:w-6 justify-content-center"
      >
        {{ Translation_CreateProject }}
      </PButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_ProjectName = returnTranslation(lang, 'lib_project_ProjectForm_ProjectName');
const Translation_AGoodCandidateForAProjectName = returnTranslation(lang, 'lib_project_ProjectForm_AGoodCandidateForAProjectName');
const Translation_Cancel = returnTranslation(lang, 'lib_project_ProjectForm_Cancel');
const Translation_CreateProject = returnTranslation(lang, 'lib_project_ProjectForm_CreateProject');
</script>

<script lang="ts">
import { mapActions, mapState } from 'pinia'
import { defineComponent } from 'vue'

import { TipMessage } from '@/common/components'
import { useUserStore } from '@/main'
import { useDialogStore } from '@/modules/dialog/store'
import { useFormStore } from '@/modules/form/store'
import { useProjectStore } from '@/modules/project/store'

export default defineComponent({
  name: 'new-project-form',
  components: {
    TipMessage
  },
  data() {
    return {
      name: ''
    }
  },
  computed: {
    ...mapState(useUserStore, ['currentWorkspace']),
    ...mapState(useFormStore, ['getErrorByComponentId']),
    errors() {
      return this.getErrorByComponentId(this.merginComponentUuid) ?? {}
    }
  },
  beforeUnmount() {
    this.clearErrors({
      componentId: this.merginComponentUuid,
      keepNotification: true
    })
  },
  methods: {
    ...mapActions(useDialogStore, ['close']),
    ...mapActions(useFormStore, ['clearErrors']),
    ...mapActions(useProjectStore, ['createProject']),

    async create() {
      // TODO: add types
      const dialogData = { componentId: this.merginComponentUuid }
      await this.clearErrors(dialogData)
      try {
        const data = {
          name: this.name.trim(),
          public: false
        }
        await this.createProject({
          data,
          namespace: this.currentWorkspace?.name
        })
        await this.close()
        this.$emit('success')
      } catch (err) {
        this.$emit('error', err, dialogData)
      }
    },
    beforeUnmount() {
      this.clearErrors({
        componentId: this.merginComponentUuid,
        keepNotification: true
      })
    }
  }
})
</script>
