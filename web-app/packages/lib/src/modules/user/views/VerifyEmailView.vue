<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-onboarding-page>
    <template #header>
      <h1 class="headline-h1">{{ Translation_EmailConfirmation }}</h1>
    </template>
    <div class="flex flex-column gap-4 align-items-center">
      <template v-if="verified"
        ><img src="@/assets/neutral.svg" alt="MerginMaps neutral" /><span
          class="opacity-80 paragraph-p5"
          >{{ Translation_YourEmailAddressHasBeenVerified }}</span
        ></template
      >
      <template v-else
        ><img src="@/assets/negative.svg" alt="MerginMaps negative" />{{ Translation_InvalidToken }}</template
      >
      <PButton
        data-cy="verify-email-btn"
        @click="$router.push({ name: 'home' })"
        class="w-full"
        :label="Translation_Continue"
      />
    </div>
  </app-onboarding-page>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_EmailConfirmation = returnTranslation(lang, 'lib_user_VerifyEmailView_EmailConfirmation');
const Translation_YourEmailAddressHasBeenVerified = returnTranslation(lang, 'lib_user_VerifyEmailView_YourEmailAddressHasBeenVerified');
const Translation_InvalidToken = returnTranslation(lang, 'lib_user_VerifyEmailView_InvalidToken');
const Translation_Continue = returnTranslation(lang, 'lib_user_VerifyEmailView_Continue');

</script>

<script lang="ts">
import { defineComponent } from 'vue'

import AppOnboardingPage from '@/common/components/AppOnboardingPage.vue'
import { UserApi } from '@/modules/user/userApi'

export default defineComponent({
  name: 'VerifyEmailView',
  data() {
    return {
      verified: false
    }
  },
  computed: {
    token() {
      return this.$route.params.token as string
    }
  },
  async created() {
    try {
      await UserApi.confirmEmail(this.token)
      this.verified = true
    } catch (e) {
      this.verified = false
    }
  },
  components: { AppOnboardingPage }
})
</script>

<style scoped lang="scss"></style>
