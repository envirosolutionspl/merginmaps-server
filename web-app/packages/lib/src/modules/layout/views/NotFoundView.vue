<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <article
    class="relative not-found-view flex align-items-center justify-content-center h-full"
  >
    <aside class="absolute top-0 left-0 m-4">
      <img src="@/assets/mm-logo.svg" />
    </aside>
    <div
      class="not-found-view-container flex flex-column align-items-center text-center row-gap-4 p-4 lg:p-0"
    >
      <header>
        <h1 class="headline-h1">{{ Translation_OoopsItSeemsTheGPSHasLostItsWay }}</h1>
      </header>
      <img src="@/assets/map-circle.svg" alt="Not found" />
      {{ Translation_ThisPageDoesNotExist }}
      <PButton
        v-if="displayBackButton"
        data-cy="login-form-btn-back-dashboard"
        @click="$router.push({ name: 'dashboard' })"
        >{{ Translation_BackToDashboard }}
      </PButton>
    </div>
  </article>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_OoopsItSeemsTheGPSHasLostItsWay = returnTranslation(lang, 'lib_layout_NotFoundView_OoopsItSeemsTheGPSHasLostItsWay');
const Translation_ThisPageDoesNotExist = returnTranslation(lang, 'lib_layout_NotFoundView_ThisPageDoesNotExist');
const Translation_BackToDashboard = returnTranslation(lang, 'lib_layout_NotFoundView_BackToDashboard');

</script>

<script lang="ts">
import { mapState } from 'pinia'
import { defineComponent } from 'vue'

import { useUserStore } from '@/modules/user/store'

export default defineComponent({
  name: 'NotFoundView',
  computed: {
    ...mapState(useUserStore, ['loggedUser']),
    displayBackButton() {
      return this.loggedUser
    }
  }
})
</script>

<style scoped lang="scss">
.not-found-view {
  &-container {
    max-width: 480px;
    width: 100%;
  }
}
</style>
