<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <access-request-table-template
    :namespace="namespace"
    @accept-access-request-error="onAcceptAccessRequestError"
  />
</template>

<script lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG
import { AxiosError } from 'axios'
import { mapActions } from 'pinia'
import { defineComponent } from 'vue'

import AccessRequestTableTemplate from './AccessRequestTableTemplate.vue'

import { getErrorMessage } from '@/common/error_utils'
import { useNotificationStore } from '@/modules/notification/store'

const FailedToAcceptAccessRequest = returnTranslation(lang, 'FailedToAcceptAccessRequest');

export default defineComponent({
  name: 'AccessRequestTable',
  components: { AccessRequestTableTemplate },
  props: {
    namespace: {
      type: String,
      default: null
    }
  },
  methods: {
    ...mapActions(useNotificationStore, ['error']),

    // TODO: Add more handlers from template, add more emits from template
    async onAcceptAccessRequestError(err: AxiosError) {
      this.error({
        text: getErrorMessage(err, FailedToAcceptAccessRequest)
      })
    }
  }
})
</script>

<style lang="scss" scoped></style>
