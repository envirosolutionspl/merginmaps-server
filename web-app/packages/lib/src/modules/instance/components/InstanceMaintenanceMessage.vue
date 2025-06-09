<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-container class="relative z-5">
    <PMessage severity="warn" :closable="false" class="m-0">
      <template #messageicon="slotProps">
        <i :class="[slotProps.class, 'ti ti-alert-triangle-filled']" />
      </template>
      <p>
        {{ Translation_TheServiceIsCurrentlyIn }}
      </p></PMessage
    >
  </app-container>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_TheServiceIsCurrentlyIn = returnTranslation(lang, 'lib_instance_InstanceMaintenanceMessage_TheServiceIsCurrentlyIn');

import { AppContainer } from '@/common/components'
</script>

<style scoped></style>
