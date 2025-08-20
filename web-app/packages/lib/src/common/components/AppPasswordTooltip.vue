<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <label class="flex align-items-center" :for="'for'"
    ><slot name="label"></slot>&nbsp;
    <i
      class="ti ti-info-circle-filled cursor-pointer text-color-medium-green hover:text-color paragraph-p4"
      :style="{ color: 'var(--medium-green-color)' }"
      v-tooltip="{
        value: tooltip,
        escape: false
      }"
  /></label>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

defineProps<{ for: string }>()
const tooltip = returnTranslation(lang, 'PassTooltipComponent')
</script>
