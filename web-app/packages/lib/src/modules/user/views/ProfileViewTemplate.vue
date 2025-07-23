<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <article class="profile-view">
    <app-container
      ><section
        class="flex flex-column lg:flex-row lg:align-items-center row-gap-3"
      >
        <!-- Title with buttons -->
        <h1 class="headline-h3 text-color font-semibold">{{ AccountDetails }}</h1>
        <div class="flex flex-grow-1 align-items-center lg:justify-content-end">
          <PButton
            @click="editProfileDialog"
            icon="ti ti-pencil"
            :label="EditAccount"
            class="w-auto mr-1"
            data-cy="profile-edit-btn"
          />
          <PButton
            @click="changePasswordDialog"
            severity="secondary"
            data-cy="profile-change-password-btn"
            class="w-auto"
            icon="ti ti-lock"
            :label="ChangePassword"
          />
        </div></section
    ></app-container>
    <app-container v-if="$slots.additionalBeforeContent"
      ><slot name="additionalBeforeContent"></slot
    ></app-container>
    <app-container v-if="!loggedUser?.verified_email">
      <app-section-banner>
        <template #header-image
          ><img width="50" height="50" src="@/assets/warning.svg"
        /></template>
        <template #title>{{ PleaseVerifyYourEmail }}</template>
        <template #description
          >{{ WeSentYouAVerificationEmailToTheAccountYouProvidedDuringSignup }}</template
        >
        <template #header-actions
          ><PButton
            @click="resendConfirmationEmail"
            severity="secondary"
            data-cy="profile-send-email-btn"
            :label="SendConfirmationEmail"
        /></template>
      </app-section-banner>
    </app-container>
    <app-container>
      <app-section class="p-4">
        <div class="flex flex-column align-items-center row-gap-3 text-center">
          <PAvatar
            :label="$filters.getAvatar(loggedUser.email, loggedUser.name)"
            shape="circle"
            :pt="{
              root: {
                class: 'text-5xl font-semibold text-color-forest',
                style: {
                  width: '120px',
                  height: '120px'
                }
              }
            }"
          />
          <h3 class="headline-h2" data-cy="profile-username">
            {{ loggedUser?.username }}
          </h3>
          <p
            class="m-0 paragraph-p6 overflow-wrap-anywhere"
            data-cy="profile-email"
          >
            <i
              v-if="!loggedUser?.verified_email"
              v-tooltip.top="{
                value: 'Email verification status'
              }"
              class="ti ti-alert-circle-filled"
              data-cy="project-form-missing-project"
              style="color: var(--grape-color)"
            ></i
            >&nbsp;{{ loggedUser?.email }}
          </p>
          <dl class="profile-view-detail-list grid grid-nogutter paragraph-p5">
            <div
              class="col-6 flex flex-column align-items-start text-left flex-wrap"
            >
              <dt class="paragraph-p6 opacity-80 mb-2">{{ FullName }}</dt>
              <dd class="font-semibold" data-cy="profile-name">
                {{ loggedUser?.name || '-' }}
              </dd>
            </div>
            <div class="col-6 flex flex-column align-items-end">
              <dt class="paragraph-p6 opacity-80 mb-2">{{ Registered }}</dt>
              <dd class="font-semibold" data-cy="profile-registered">
                {{ $filters.date(loggedUser?.registration_date) }}
              </dd>
            </div>
          </dl>
        </div>
      </app-section>
    </app-container>
    <app-container>
      <app-section>
        <template #title>{{ Advanced }}</template>
        <div class="flex flex-column row-gap-3 paragraph-p5 px-4 pb-4">
          <div
            :class="[
              'flex flex-column align-items-start',
              'row-gap-2',
              'md:align-items-center md:flex-row'
            ]"
          >
            <div class="flex-grow-1">
              <p class="title-t3">{{ ReceiveNotifications }}</p>
              <span class="paragraph-p6 opacity-80"
                >{{ WeWillSendYouInformationAboutWorkspaceActivity }}</span
              >
            </div>
            <div
              class="flex align-items-center flex-shrink-0"
              data-cy="profile-notification"
            >
              <PInputSwitch
                :modelValue="loggedUser?.receive_notifications"
                @change="receiveNotificationsChange"
              />
            </div>
          </div>
          <div
            :class="[
              'flex flex-column align-items-start',
              'row-gap-2',
              'md:align-items-center md:flex-row'
            ]"
          >
            <div class="flex-grow-1">
              <p class="title-t3">{{ CloseAccount }}</p>
              <span class="paragraph-p6 opacity-80"
                >{{ YourAccountWillBeClosedInCaseYouAreAnOwnerOfAWorkspaceYouMightNeedToTransferTheOwnershipFirstOrCloseTheWorkspace }}</span
              >
            </div>
            <div class="flex-shrink-0">
              <PButton
                @click="confirmDeleteUser"
                severity="danger"
                data-cy="profile-close-account-btn"
                :label="CloseAccount"
              />
            </div>
          </div>
        </div>
      </app-section>
    </app-container>
    <app-container><slot name="additionalContent"></slot></app-container>
  </article>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const AccountDetails = returnTranslation(lang, 'AccountDetails');
const EditAccount = returnTranslation(lang, 'EditAccount');
const ChangePassword = returnTranslation(lang, 'ChangePassword');
const PleaseVerifyYourEmail = returnTranslation(lang, 'PleaseVerifyYourEmail');
const WeSentYouAVerificationEmailToTheAccountYouProvidedDuringSignup = returnTranslation(lang, 'WeSentYouAVerificationEmailToTheAccountYouProvidedDuringSignup');
const SendConfirmationEmail = returnTranslation(lang, 'SendConfirmationEmail');
const FullName = returnTranslation(lang, 'FullName');
const Registered = returnTranslation(lang, 'Registered');
const Advanced = returnTranslation(lang, 'Advanced');
const ReceiveNotifications = returnTranslation(lang, 'ReceiveNotifications');
const WeWillSendYouInformationAboutWorkspaceActivity = returnTranslation(lang, 'WeWillSendYouInformationAboutWorkspaceActivity');
const CloseAccount = returnTranslation(lang, 'CloseAccount');
const YourAccountWillBeClosedInCaseYouAreAnOwnerOfAWorkspaceYouMightNeedToTransferTheOwnershipFirstOrCloseTheWorkspace = returnTranslation(lang, 'YourAccountWillBeClosedInCaseYouAreAnOwnerOfAWorkspaceYouMightNeedToTransferTheOwnershipFirstOrCloseTheWorkspace');

</script>

<script lang="ts">
import { mapState, mapActions } from 'pinia'
import { defineComponent } from 'vue'

import DeleteAccountDialog from '../components/DeleteAccountConfirm.vue'

import AppContainer from '@/common/components/AppContainer.vue'
import AppSection from '@/common/components/AppSection.vue'
import AppSectionBanner from '@/common/components/AppSectionBanner.vue'
import { DeleteAccountConfirmProps, useDialogStore } from '@/modules'
import { useLayoutStore } from '@/modules/layout/store'
import ChangePasswordForm from '@/modules/user/components/ChangePasswordForm.vue'
import EditProfileForm from '@/modules/user/components/EditProfileForm.vue'
import { useUserStore } from '@/modules/user/store'

export default defineComponent({
  name: 'ProfileViewTemplate',
  props: {
    name: String
  },
  components: { AppContainer, AppSection, AppSectionBanner },
  data() {
    return {
      dialog: false
    }
  },
  computed: {
    ...mapState(useLayoutStore, ['drawer']),
    ...mapState(useUserStore, ['loggedUser'])
  },
  created() {
    this.fetchUserProfile()
  },
  methods: {
    ...mapActions(useDialogStore, ['show']),
    ...mapActions(useUserStore, {
      fetchUserProfile: 'fetchUserProfile',
      resendConfirmationEmailToUser: 'resendConfirmationEmail',
      closeUserProfile: 'closeUserProfile',
      editUserProfile: 'editUserProfile'
    }),

    resendConfirmationEmail() {
      this.resendConfirmationEmailToUser({ email: this.loggedUser?.email })
    },
    confirmDeleteUser() {
      const props: DeleteAccountConfirmProps = {
        username: this.loggedUser?.username
      }
      const listeners = {
        confirm: async () => await this.closeUserProfile()
      }
      this.show({
        component: DeleteAccountDialog,
        params: {
          props,
          listeners,
          dialog: { header: returnTranslation(lang, 'CloseAccount') }
        }
      })
    },
    changePasswordDialog() {
      const dialog = { persistent: true, header: returnTranslation(lang, 'ChangePassword') }
      this.show({
        component: ChangePasswordForm,
        params: {
          dialog
        }
      })
    },
    editProfileDialog() {
      const props = { profile: this.loggedUser }
      const dialog = { header: returnTranslation(lang, 'EditAccount') }
      this.show({
        component: EditProfileForm,
        params: {
          props,
          dialog
        }
      })
    },
    receiveNotificationsChange() {
      this.editUserProfile({
        editedUser: {
          ...this.loggedUser,
          receive_notifications: !this.loggedUser?.receive_notifications
        },
        componentId: this.merginComponentUuid
      })
    }
  }
})
</script>

<style lang="scss" scoped>
.profile-view {
  &-detail-list {
    max-width: 640px;
    width: 100%;
  }
}
</style>
