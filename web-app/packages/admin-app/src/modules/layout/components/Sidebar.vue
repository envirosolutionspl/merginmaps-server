<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: LicenseRef-MerginMaps-Commercial
-->

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const admin = returnTranslation(lang, 'AdminPanel')

import { AdminRoutes, SidebarFooter } from '@mergin/admin-lib'
import { SideBarItemModel, SideBarTemplate } from '@mergin/lib'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const sidebarItems = computed<SideBarItemModel[]>(() => [
  {
    title: returnTranslation(import.meta.env.VITE_LANG, 'Overview'),
    to: '/overview',
    icon: 'ti ti-layout-dashboard',
    active: route.matched.some((item) => item.name === AdminRoutes.OVERVIEW)
  },
  {
    title: returnTranslation(import.meta.env.VITE_LANG, 'Accounts'),
    to: '/accounts',
    icon: 'ti ti-user-circle',
    active: route.matched.some((item) => item.name === AdminRoutes.ACCOUNTS)
  },
  {
    title: returnTranslation(import.meta.env.VITE_LANG, 'Projects'),
    to: '/projects',
    icon: 'ti ti-article',
    active: route.matched.some((item) => item.name === AdminRoutes.PROJECTS)
  },
  {
    title: returnTranslation(import.meta.env.VITE_LANG, 'Settings'),
    to: '/settings',
    icon: 'ti ti-settings',
    active: route.matched.some((item) => item.name === AdminRoutes.SETTINGS)
  }
])
</script>

<template>
  <side-bar-template :sidebarItems="sidebarItems">
    <template #subtitle>{{ admin }}</template>
    <template #footer>
      <sidebar-footer />
    </template>
  </side-bar-template>
</template>

<style lang="scss" scoped></style>
