<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-container>
    <app-section-banner>
      <template #header-image>
        <img width="50" height="50" src="@/assets/globe.svg" />
      </template>
      <template #header-actions
        ><PButton
          :label="BrowseCommunityProjects"
          @click.stop="click"
          data-cy="community-project-btn"
      /></template>
      <template #title>{{ CommunityProjects }}</template>
      <template #description
        >{{ ExploreVariousTemplateProjectsWithinOurCommunity }}</template
      >
    </app-section-banner>
  </app-container>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const BrowseCommunityProjects = returnTranslation(lang, 'BrowseCommunityProjects');
const CommunityProjects = returnTranslation(lang, 'CommunityProjects');
const ExploreVariousTemplateProjectsWithinOurCommunity = returnTranslation(lang, 'ExploreVariousTemplateProjectsWithinOurCommunity');

import { useRouter } from 'vue-router'

import { ProjectRouteName } from '../routes'

import AppContainer from '@/common/components/AppContainer.vue'
import AppSectionBanner from '@/common/components/AppSectionBanner.vue'

const router = useRouter()

function click() {
  router.push({ name: ProjectRouteName.ProjectsExplore })
}
</script>
