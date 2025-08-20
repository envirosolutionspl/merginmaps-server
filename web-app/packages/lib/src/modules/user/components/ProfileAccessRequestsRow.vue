<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-section v-if="accessRequests && accessRequestsCount > 0">
    <template #title>{{ YouRequestedAccessToTheseProjects }}</template>
    <access-request-table />
  </app-section>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const YouRequestedAccessToTheseProjects = returnTranslation(lang, 'YouRequestedAccessToTheseProjects');

</script>

<script lang="ts">
import { mapActions, mapState } from 'pinia'
import { defineComponent } from 'vue'

import AppSection from '@/common/components/AppSection.vue'
import AccessRequestTable from '@/modules/project/components/AccessRequestTable.vue'
import { useProjectStore } from '@/modules/project/store'

export default defineComponent({
  name: 'ProfileAccessRequestsRow',
  components: { AccessRequestTable, AppSection },
  computed: {
    ...mapState(useProjectStore, ['accessRequests', 'accessRequestsCount'])
  },
  async created() {
    await this.initUserAccessRequests()
  },
  methods: {
    ...mapActions(useProjectStore, ['initUserAccessRequests'])
  }
})
</script>

<style scoped lang="scss"></style>
