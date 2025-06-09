<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <ConfirmDialog
    :text="Translation_DoYouReallyWishToCloseYourAccount"
    :description="Translation_ThisActionWillDeleteYourMerginMapsAccount"
    :cancelText="Translation_No"
    :confirmText="Translation_Yes"
    :hint="username"
    :confirmField="{
      label: Translation_Username,
      expected: username,
      placeholder: Translation_TypeInYourUsernameToConfirmDeletion
    }"
    severity="danger"
    @confirm="confirm"
  />
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_DoYouReallyWishToCloseYourAccount = returnTranslation(lang, 'lib_user_DeleteAccountConfirm_DoYouReallyWishToCloseYourAccount');
const Translation_ThisActionWillDeleteYourMerginMapsAccount = returnTranslation(lang, 'lib_user_DeleteAccountConfirm_ThisActionWillDeleteYourMerginMapsAccount');
const Translation_No = returnTranslation(lang, 'lib_user_DeleteAccountConfirm_No');
const Translation_Yes = returnTranslation(lang, 'lib_user_DeleteAccountConfirm_Yes');
const Translation_Username = returnTranslation(lang, 'lib_user_DeleteAccountConfirm_Username');
const Translation_TypeInYourUsernameToConfirmDeletion = returnTranslation(lang, 'lib_user_DeleteAccountConfirm_TypeInYourUsernameToConfirmDeletion');

import { DeleteAccountConfirmProps } from '@/modules'
import ConfirmDialog from '@/modules/dialog/components/ConfirmDialog.vue'

defineProps<DeleteAccountConfirmProps>()
const emit = defineEmits(['confirm'])

function confirm() {
  emit('confirm')
}
</script>
