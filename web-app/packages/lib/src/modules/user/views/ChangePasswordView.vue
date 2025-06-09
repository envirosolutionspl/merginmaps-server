<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <app-onboarding-page>
    <template #header><h1 class="headline-h1">{{ Translation_ChangePassword }}</h1></template>

    <form
      v-if="!success"
      @submit.prevent="changePasswordWithToken"
      class="flex flex-column"
    >
      <span>
        <app-password-tooltip for="newPassword"
          ><template #label>{{ Translation_NewPassword }}</template>
        </app-password-tooltip>
        <PPassword
          id="newPassword"
          v-model="password"
          data-cy="change-password"
          :class="['w-full', errors.old_password ? 'p-invalid' : '']"
          toggleMask
          :feedback="false"
          aria-describedby="password-error"
          :placeholder="Translation_PleaseEnterYourPassword"
        />
        <span class="p-error paragraph-p6" id="password-error">{{
          errors.password?.[0]
            ? errors.password?.[0].startsWith('Password')
              ? Translation_PasswordMustBeAtLeast
              : errors.password[0]
            : '&nbsp;'
        }}</span>
      </span>

      <span>
        <app-password-tooltip for="confirm">
          <template #label>{{ Translation_ConfirmPassword }}</template>
        </app-password-tooltip>

        <PPassword
          id="confirm"
          v-model="confirm"
          :class="['w-full', errors.confirm ? 'p-invalid' : '']"
          data-cy="change-password-confirm"
          aria-describedby="confirm-password-error"
          toggleMask
          :feedback="false"
          :placeholder="Translation_PleaseEnterYourNewPassword"
        />

        <span class="p-error paragraph-p6" id="confirm-password-error">{{
          errors.confirm?.[0] || '&nbsp;'
        }}</span>
      </span>

      <PButton
        type="submit"
        class="mt-6"
        data-cy="change-password-btn"
        :disabled="!password || !confirm"
        :label="Translation_Change"
      />
    </form>

    <div v-else class="flex flex-column align-items-center">
      <span
        >{{ Translation_YourPasswordWasChanged }}
        <router-link
          class="text-color-forest title-t3 align-self-center"
          :to="{ name: 'login' }"
          >{{ lib_user_ChangePasswordView_SignIn }}</router-link
        ></span
      >
    </div>
  </app-onboarding-page>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_ChangePassword = returnTranslation(lang, 'lib_user_ChangePasswordView_YourAccountWillBeClosed');
const Translation_NewPassword = returnTranslation(lang, 'lib_user_ChangePasswordView_NewPassword');
const Translation_PleaseEnterYourPassword = returnTranslation(lang, 'lib_user_ChangePasswordView_PleaseEnterYourPassword');
const Translation_PasswordMustBeAtLeast = returnTranslation(lang, 'lib_user_ChangePasswordView_PasswordMustBeAtLeast');
const Translation_ConfirmPassword = returnTranslation(lang, 'lib_user_ChangePasswordView_ConfirmPassword');
const Translation_PleaseEnterYourNewPassword = returnTranslation(lang, 'lib_user_ChangePasswordView_PleaseEnterYourNewPassword');
const Translation_Change = returnTranslation(lang, 'lib_user_ChangePasswordView_Change');
const Translation_YourPasswordWasChanged = returnTranslation(lang, 'lib_user_ChangePasswordView_YourPasswordWasChanged');
const lib_user_ChangePasswordView_SignIn = returnTranslation(lang, 'lib_user_ChangePasswordView_SignIn');

</script>


<script lang="ts">
import { mapActions, mapState } from 'pinia'
import { defineComponent } from 'vue'

import AppOnboardingPage from '@/common/components/AppOnboardingPage.vue'
import AppPasswordTooltip from '@/common/components/AppPasswordTooltip.vue'
import { useFormStore } from '@/modules/form/store'
import { useUserStore } from '@/modules/user/store'

export default defineComponent({
  name: 'ChangePasswordView',
  components: { AppPasswordTooltip, AppOnboardingPage },
  data() {
    return {
      on: '',
      success: false,
      password: '',
      confirm: '',
      passwordVisible: false
    }
  },
  computed: {
    ...mapState(useFormStore, ['getErrorByComponentId']),
    errors() {
      return this.getErrorByComponentId(this.merginComponentUuid) ?? {}
    },
    token() {
      return this.$route.params.token as string
    }
  },

  beforeUnmount() {
    this.clearErrors({
      componentId: this.merginComponentUuid,
      keepNotification: true
    })
  },

  methods: {
    ...mapActions(useUserStore, {
      changePasswordWithTokenAction: 'changePasswordWithToken'
    }),
    ...mapActions(useFormStore, ['clearErrors', 'handleError']),
    responseCallback(value) {
      this.success = value
    },
    changePasswordWithToken() {
      this.clearErrors({ componentId: this.merginComponentUuid })
      const data = {
        password: this.password,
        confirm: this.confirm
      }

      this.changePasswordWithTokenAction({
        data,
        token: this.token,
        callback: this.responseCallback,
        componentId: this.merginComponentUuid
      })
    }
  }
})
</script>

<style lang="scss" scoped></style>
