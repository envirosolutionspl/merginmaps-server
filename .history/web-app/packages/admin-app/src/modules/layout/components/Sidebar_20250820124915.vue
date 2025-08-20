<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: LicenseRef-MerginMaps-Commercial
-->

<script setup lang="ts">
import { AdminRoutes, SidebarFooter } from '@mergin/admin-lib'
import { SideBarItemModel, SideBarTemplate } from '@mergin/lib'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const sidebarItems = computed<SideBarItemModel[]>(() => [
  {
<<<<<<< HEAD
    title: returnTranslation(import.meta.env.VITE_LANG, 'Overview'),
=======
    title: 'Overview',
>>>>>>> parent of 781c0e7 (new translations modules)
    to: '/overview',
    icon: 'ti ti-layout-dashboard',
    active: route.matched.some((item) => item.name === AdminRoutes.OVERVIEW)
  },
  {
<<<<<<< HEAD
    title: returnTranslation(import.meta.env.VITE_LANG, 'Accounts'),
=======
    title: 'Accounts',
>>>>>>> parent of 781c0e7 (new translations modules)
    to: '/accounts',
    icon: 'ti ti-user-circle',
    active: route.matched.some((item) => item.name === AdminRoutes.ACCOUNTS)
  },
  {
<<<<<<< HEAD
    title: returnTranslation(import.meta.env.VITE_LANG, 'Projects'),
=======
    title: 'Projects',
>>>>>>> parent of 781c0e7 (new translations modules)
    to: '/projects',
    icon: 'ti ti-article',
    active: route.matched.some((item) => item.name === AdminRoutes.PROJECTS)
  },
  {
<<<<<<< HEAD
    title: returnTranslation(import.meta.env.VITE_LANG, 'Settings'),
=======
    title: 'Settings',
>>>>>>> parent of 781c0e7 (new translations modules)
    to: '/settings',
    icon: 'ti ti-settings',
    active: route.matched.some((item) => item.name === AdminRoutes.SETTINGS)
  }
])
</script>

<template>
  <side-bar-template :sidebarItems="sidebarItems">
    <template #subtitle>Admin panel</template>
    <template #footer>
      <sidebar-footer />
    </template>
  </side-bar-template>
</template>

<style lang="scss" scoped></style>
