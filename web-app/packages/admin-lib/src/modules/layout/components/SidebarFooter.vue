<template>
  <PDivider class="m-0" />
  <a
    href="/"
    target="__blank"
    class="flex justify-content-between align-items-center title-t5 no-underline cursor-pointer"
    >{{ Translation_Dashboard }} <i class="title-t1 ti ti-external-link"
  /></a>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_Dashboard = returnTranslation(lang, 'adminlib_admin_SidebarFooter_Dashboard')
</script>
