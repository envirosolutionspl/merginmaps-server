<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-onboarding-page>
    <template #header>
      <h1 class="headline-h1">{{ EmailConfirmation }}</h1>
    </template>
    <div class="flex flex-column gap-4 align-items-center">
      <template v-if="verified"
        ><img src="@/assets/neutral.svg" alt="MerginMaps neutral" /><span
          class="opacity-80 paragraph-p5"
          >{{ YourEmailAddressHasBeenVerified }}</span
        ></template
      >
      <template v-else
        ><img src="@/assets/negative.svg" alt="MerginMaps negative" />{{ InvalidToken }}</template
      >
      <PButton
        data-cy="verify-email-btn"
        @click="$router.push({ name: 'home' })"
        class="w-full"
        :label="Continue"
      />
    </div>
  </app-onboarding-page>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const EmailConfirmation = returnTranslation(lang, 'EmailConfirmation');
const YourEmailAddressHasBeenVerified = returnTranslation(lang, 'YourEmailAddressHasBeenVerified');
const InvalidToken = returnTranslation(lang, 'InvalidToken');
const Continue = returnTranslation(lang, 'Continue');

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
