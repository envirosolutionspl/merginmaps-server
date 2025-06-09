<template>
  <admin-layout>
    <app-container>
      <app-section ground>
        <template #header>
          <h1 class="headline-h3">{{ Translation_AccountDetails }}</h1>
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
                value: Translation_EmailVerificationStatus
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
              <dt class="paragraph-p6 opacity-80 mb-2">{{ Translation_FullName }}</dt>
              <dd class="font-semibold" data-cy="profile-name">
                {{ profile?.name || '-' }}
              </dd>
            </div>
            <div class="col-6 flex flex-column align-items-end">
              <dt class="paragraph-p6 opacity-80 mb-2">{{ Translation_Registered }}</dt>
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
        <template #title>{{ Translation_Advanced }}</template>

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
                      ? Translation_GrantAdminAccess
                      : Translation_RevokeAdminAccess
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
                  user?.active ? Translation_DeactivateAccount : Translation_ActivateAccount
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
                :label="Translation_DeleteAccount"
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

const Translation_AccountDetails = returnTranslation(lang, 'adminlib_admin_AccountDetailView_AccountDetails');
const Translation_EmailVerificationStatus = returnTranslation(lang, 'adminlib_admin_AccountDetailView_EmailVerificationStatus');
const Translation_FullName = returnTranslation(lang, 'adminlib_admin_AccountDetailView_FullName');
const Translation_Registered = returnTranslation(lang, 'adminlib_admin_AccountDetailView_Registered');
const Translation_Advanced = returnTranslation(lang, 'adminlib_admin_AccountDetailView_Advanced');
const Translation_GrantAdminAccess = returnTranslation(lang, 'adminlib_admin_AccountDetailView_GrantAdminAccess');
const Translation_RevokeAdminAccess = returnTranslation(lang, 'adminlib_admin_AccountDetailView_RevokeAdminAccess');
const Translation_DeactivateAccount = returnTranslation(lang, 'adminlib_admin_AccountDetailView_DeactivateAccount');
const Translation_ActivateAccount = returnTranslation(lang, 'adminlib_admin_AccountDetailView_ActivateAccount');
const Translation_DeleteAccount = returnTranslation(lang, 'adminlib_admin_AccountDetailView_DeleteAccount');

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
    title: returnTranslation(lang, 'adminlib_admin_AccountDetailView_ReceiveNotifications'),
    description: profile?.value?.receive_notifications
      ? returnTranslation(lang, 'adminlib_admin_AccountDetailView_UserHasEnabledReceivingNotifications')
      : returnTranslation(lang, 'adminlib_admin_AccountDetailView_UserHasDisabledNotifications')
  },
  {
    key: 'adminAccess',
    title: returnTranslation(lang, 'adminlib_admin_AccountDetailView_AccessToAdminPanel'),
    description: user.value?.is_admin
      ? returnTranslation(lang, 'adminlib_admin_AccountDetailView_UserHasAccessToTheAdminPanel')
      : returnTranslation(lang, 'adminlib_admin_AccountDetailView_UserDoesNotHaveAccessToTheAdminPanel')
  },
  {
    key: 'accountActivation',
    title: returnTranslation(lang, 'adminlib_admin_AccountDetailView_AccountActivation'),
    description: user?.value?.active
      ? returnTranslation(lang, 'adminlib_admin_AccountDetailView_TheUsersAccountIsCurrentlyActive')
      : returnTranslation(lang, 'adminlib_admin_AccountDetailView_TheUsersAccountIsCurrentlyInactive')
  },
  {
    key: 'deleteAccount',
    title: returnTranslation(lang, 'adminlib_admin_AccountDetailView_DeleteAccount'),
    description:
      returnTranslation(lang, 'adminlib_admin_AccountDetailView_DeletingThisUserWillRemoveThemAndAllTheirData')
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
        confirmText: returnTranslation(lang, 'adminlib_admin_AccountDetailView_Deactivate'),
        severity: 'warning',
        text: returnTranslation(lang, 'adminlib_admin_AccountDetailView_DoYouReallyWantDeactivateThisAccount'),
        description:
          returnTranslation(lang, 'adminlib_admin_AccountDetailView_DeactivatingThisAccountWillLead')
      }
    : {
        text: returnTranslation(lang, 'adminlib_admin_AccountDetailView_DoYouReallyWantActivateThisAccount'),
        confirmText: returnTranslation(lang, 'adminlib_admin_AccountDetailView_Activate')
      }
  const dialog = { header: returnTranslation(lang, 'adminlib_admin_AccountDetailView_UserActivation') }
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
    text: returnTranslation(lang, 'adminlib_admin_AccountDetailView_AreYouSureYouWantToPermanentlyDeleteThisAccount'),
    description: returnTranslation(lang, 'adminlib_admin_AccountDetailView_DeletingThisUserWillRemoveThemAndAllTheirDataConfirm'),
    hint: user.value.username,
    confirmText: returnTranslation(lang, 'adminlib_admin_AccountDetailView_DeletePermanently'),
    confirmField: {
      label: returnTranslation(lang, 'adminlib_admin_AccountDetailView_Username'),
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
    params: { props, listeners, dialog: { header: returnTranslation(lang, 'adminlib_admin_AccountDetailView_DeleteUser') } }
  })
}

const switchAdminAccess = async () => {
  const props: ConfirmDialogProps = !user.value?.is_admin
    ? {
        text: returnTranslation(lang, 'adminlib_admin_AccountDetailView_AreYouSureToGrantAccessToAdminPanelToThisUser'),
        description: returnTranslation(lang, 'adminlib_admin_AccountDetailView_ThisPersonWillHaveFullManagementAccessToAllData'),
        hint: user.value.username,
        confirmText: returnTranslation(lang, 'adminlib_admin_AccountDetailView_GrantAccess'),
        confirmField: {
          label: returnTranslation(lang, 'adminlib_admin_AccountDetailView_Username'),
          expected: user.value.username
        },
        severity: 'warning'
      }
    : {
        text: returnTranslation(lang, 'adminlib_admin_AccountDetailView_AreYouSureYouWantToRevokeAccessToAdminPanel'),
        description: returnTranslation(lang, 'adminlib_admin_AccountDetailView_ThisPersonWillNoLongerHaveAccessToTheAdminPanel'),
        hint: user.value.username,
        confirmText: returnTranslation(lang, 'adminlib_admin_AccountDetailView_RevokeAccess'),
        confirmField: {
          label: returnTranslation(lang, 'adminlib_admin_AccountDetailView_Username'),
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
    params: { props, listeners, dialog: { header: returnTranslation(lang, 'adminlib_admin_AccountDetailView_AdminAccess') } }
  })
}
</script>

<style lang="scss" scoped>
.profile-view-detail-list {
  max-width: 640px;
  width: 100%;
}
</style>
