<template>
  <admin-layout>
    <app-container>
      <app-section ground>
        <template #header>
          <h1 class="headline-h3">{{ AccountDetails }}</h1>
        </template>
      </app-section>
    </app-container>

    <app-container>
      <app-section class="p-4">
        <div class="flex flex-column align-items-center row-gap-3 text-center">
          <PAvatar
            v-if="user"
            :label="$filters.getAvatar(user?.email, user?.username)"
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
            {{ user?.username }}
          </h3>
          <p
            class="m-0 paragraph-p6 overflow-wrap-anywhere"
            data-cy="profile-email"
          >
            <i
              v-if="!user?.verified_email"
              v-tooltip.top="{
                value: EmailVerificationStatus
              }"
              class="ti ti-alert-circle-filled"
              style="color: var(--grape-color)"
            ></i>
            {{ user?.email }}
          </p>
          <dl class="profile-view-detail-list grid grid-nogutter paragraph-p5">
            <div
              class="col-6 flex flex-column align-items-start text-left flex-wrap"
            >
              <dt class="paragraph-p6 opacity-80 mb-2">{{ FullName }}</dt>
              <dd class="font-semibold" data-cy="profile-name">
                {{ profile?.name || '-' }}
              </dd>
            </div>
            <div class="col-6 flex flex-column align-items-end">
              <dt class="paragraph-p6 opacity-80 mb-2">{{ Registered }}</dt>
              <dd class="font-semibold" data-cy="profile-registered">
                {{ $filters.date(user?.registration_date) }}
              </dd>
            </div>
          </dl>
        </div>
      </app-section>
    </app-container>
    <app-container v-if="userStore.loggedUser?.id !== user?.id">
      <app-section>
        <template #title>{{ Advanced }}</template>

        <app-settings :items="settingsItems">
          <template #notifications>
            <div class="flex-shrink-0 paragraph-p1">
              <PInputSwitch
                :model-value="profile?.receive_notifications"
                disabled
              />
            </div>
          </template>
          <template #adminAccess>
            <div class="flex-shrink-0 paragraph-p1">
              <div
                class="flex align-items-center flex-shrink-0"
                data-cy="profile-notification"
              >
                <PButton
                  :severity="user?.is_admin ? 'danger' : 'warning'"
                  :disabled="
                    !instanceStore.configData?.enable_superadmin_assignment
                  "
                  @click="switchAdminAccess"
                  :label="
                    !user?.is_admin
                      ? GrantAdminAccess
                      : RevokeAdminAccess
                  "
                />
              </div>
            </div>
          </template>
          <template #accountActivation>
            <div class="flex-shrink-0">
              <PButton
                @click="changeStatusDialog"
                :severity="user?.active ? 'warning' : 'secondary'"
                :label="
                  user?.active ? DeactivateAccount : ActivateAccount
                "
                class="w-auto mr-1"
              />
            </div>
          </template>
          <template #deleteAccount>
            <div class="flex-shrink-0">
              <PButton
                @click="confirmDeleteUser"
                severity="danger"
                data-cy="profile-close-account-btn"
                :label="DeleteAccount"
              />
            </div>
          </template>
        </app-settings>
      </app-section>
    </app-container>
  </admin-layout>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const AccountDetails = returnTranslation(lang, 'AccountDetails');
const EmailVerificationStatus = returnTranslation(lang, 'EmailVerificationStatus');
const FullName = returnTranslation(lang, 'FullName');
const Registered = returnTranslation(lang, 'Registered');
const Advanced = returnTranslation(lang, 'Advanced');
const GrantAdminAccess = returnTranslation(lang, 'GrantAdminAccess');
const RevokeAdminAccess = returnTranslation(lang, 'RevokeAdminAccess');
const DeactivateAccount = returnTranslation(lang, 'DeactivateAccount');
const ActivateAccount = returnTranslation(lang, 'ActivateAccount');
const DeleteAccount = returnTranslation(lang, 'DeleteAccount');

import {
  ConfirmDialog,
  useDialogStore,
  AppSection,
  AppContainer,
  ConfirmDialogProps,
  AppSettings,
  AppSettingsItemConfig,
  useInstanceStore,
  useUserStore
} from '@mergin/lib'
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'

import AdminLayout from '@/modules/admin/components/AdminLayout.vue'
import { useAdminStore } from '@/modules/admin/store'

const route = useRoute()
const adminStore = useAdminStore()
const dialogStore = useDialogStore()
const instanceStore = useInstanceStore()
const userStore = useUserStore()

const settingsItems = computed<AppSettingsItemConfig[]>(() => [
  {
    key: 'notifications',
    title: returnTranslation(lang, 'ReceiveNotifications'),
    description: profile?.value?.receive_notifications
      ? returnTranslation(lang, 'UserHasEnabledReceivingNotifications')
      : returnTranslation(lang, 'UserHasDisabledNotifications')
  },
  {
    key: 'adminAccess',
    title: returnTranslation(lang, 'AccessToAdminPanel'),
    description: user.value?.is_admin
      ? returnTranslation(lang, 'UserHasAccessToTheAdminPanel')
      : returnTranslation(lang, 'UserDoesNotHaveAccessToTheAdminPanel')
  },
  {
    key: 'accountActivation',
    title: returnTranslation(lang, 'AccountActivation'),
    description: user?.value?.active
      ? returnTranslation(lang, 'TheUsersAccountIsCurrentlyActiveDeactivationWillLeadToATemporaryBanFromMerginMapsUsage')
      : returnTranslation(lang, 'TheUsersAccountIsCurrentlyInactiveActivatingItWillAllowAccessToMerginMaps')
  },
  {
    key: 'deleteAccount',
    title: 'Delete account',
    description: returnTranslation(lang, 'DeletingThisUserWillRemoveThemAndAllTheirDataThisActionCannotBeUndone')
  }
])

const user = computed(() => adminStore.user)
const profile = computed(() => adminStore.user?.profile)
const routeUsername = computed(() => route?.params?.username)

const fetchProfile = (username: string) => {
  adminStore.user = null
  adminStore.fetchUserByName({ username })
}

watch(
  routeUsername,
  (username) => {
    if (username) {
      fetchProfile(username as string)
    }
  },
  { immediate: true }
)

const changeStatusDialog = () => {
  const props: ConfirmDialogProps = user.value.active
    ? {
        confirmText: returnTranslation(lang, 'Deactivate'),
        severity: 'warning',
        text: returnTranslation(lang, 'DoYouReallyWantDeactivateThisAccount'),
        description: returnTranslation(lang, 'DeactivatingThisAccountWillLeadToATemporaryBanFromMerginMapsUsage')
      }
    : {
        text: returnTranslation(lang, 'DoYouReallyWantActivateThisAccount'),
        confirmText: returnTranslation(lang, 'Activate')
      }
  const dialog = { header: returnTranslation(lang, 'UserActivation') }
  const listeners = {
    confirm: async () => {
      await adminStore.updateUser({
        username: user.value.username,
        data: {
          active: !user.value.active
        }
      })
    }
  }
  dialogStore.show({
    component: ConfirmDialog,
    params: {
      props,
      listeners,
      dialog
    }
  })
}

const confirmDeleteUser = () => {
  const props: ConfirmDialogProps = {
    text: returnTranslation(lang, 'AreYouSureYouWantToPermanentlyDeleteThisAccount'),
    description: returnTranslation(lang, 'DeletingThisUserWillRemoveThemAndAllTheirDataThisActionCannotBeUndoneTypeInUsernameToConfirm'),
    hint: user.value.username,
    confirmText: returnTranslation(lang, 'DeletePermanently'),
    confirmField: {
      label: returnTranslation(lang, 'Username'),
      expected: user.value.username
    },
    severity: 'danger'
  }
  const listeners = {
    confirm: async () =>
      await adminStore.deleteUser({ username: user.value.username })
  }
  dialogStore.show({
    component: ConfirmDialog,
    params: { props, listeners, dialog: { header: returnTranslation(lang, 'DeleteUser') } }
  })
}

const switchAdminAccess = async () => {
  const props: ConfirmDialogProps = !user.value?.is_admin
    ? {
        text: returnTranslation(lang, 'AreYouSureToGrantAccessToAdminPanelToThisUser'),
        description: returnTranslation(lang, 'ThisPersonWillHaveFullManagementAccessToAllDataOnTheServerTheyWillSeeAllUsersAndProjectsAndCanUpdateOrRemoveThem'),
        hint: user.value.username,
        confirmText: returnTranslation(lang, 'GrantAccess'),
        confirmField: {
          label: returnTranslation(lang, 'Username'),
          expected: user.value.username
        },
        severity: 'warning'
      }
    : {
        text: returnTranslation(lang, 'AreYouSureYouWantToRevokeAccessToAdminPanelToThisUser'),
        description: returnTranslation(lang, 'ThisPersonWillNoLongerHaveAccessToTheAdminPanel'),
        hint: user.value.username,
        confirmText: returnTranslation(lang, 'RevokeAccess'),
        confirmField: {
          label: returnTranslation(lang, 'Username'),
          expected: user.value.username
        },
        severity: 'danger'
      }
  const listeners = {
    confirm: async () =>
      await adminStore.updateUser({
        username: user.value.username,
        data: {
          is_admin: !user.value.is_admin
        }
      })
  }
  dialogStore.show({
    component: ConfirmDialog,
    params: { props, listeners, dialog: { header: returnTranslation(lang, 'AdminAccess') } }
  })
}
</script>

<style lang="scss" scoped>
.profile-view-detail-list {
  max-width: 640px;
  width: 100%;
}
</style>
