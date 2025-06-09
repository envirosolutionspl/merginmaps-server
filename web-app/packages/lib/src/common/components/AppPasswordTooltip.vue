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

<script lang="ts" setup>
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG
defineProps<{ for: string }>()
const tooltip = `
  <ul>
    <li>${returnTranslation(lang, 'lib_components_AppPasswordTooltip_PasswordMustBeAtLeast')}</li>
    <li>${returnTranslation(lang, 'lib_components_AppPasswordTooltip_PasswordMustContain')}</li>
      <ul>
        <li>${returnTranslation(lang, 'lib_components_AppPasswordTooltip_Lowercase')}</li>
        <li>${returnTranslation(lang, 'lib_components_AppPasswordTooltip_Uppercase')}</li>
        <li>${returnTranslation(lang, 'lib_components_AppPasswordTooltip_Digits')}</li>
        <li>${returnTranslation(lang, 'lib_components_AppPasswordTooltip_Special')}</li>
      </ul>
  </ul>
`
</script>

<!-- const tooltip = `
  <ul>
    <li>${Translation_PasswordMustBeAtLeast}</li>
    <li>${Translation_PasswordMustContain}</li>
      <ul>
        <li>${Translation_Lowercase}</li>
        <li>${Translation_Uppercase}</li>
        <li>${Translation_Digits}</li>
        <li>${Translation_Special}</li>
      </ul>
  </ul>
` -->