<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <ConfirmDialog
    :text="DoYouReallyWishToCloseYourAccount"
    :description="ThisActionWillDeleteYourMerginMapsAccountIfYouAreAWorkspaceOwnerYouNeedToTransferTheOwnershipToSomebodyElseOrCloseTheWorkspace"
    :cancelText="No"
    :confirmText="Yes"
    :hint="username"
    :confirmField="{
      label: Username,
      expected: username
    }"
    severity="danger"
    @confirm="confirm"
  >
    <TipMessage>
      <template #image
        ><img wdth="50" height="50" src="@/assets/exclamation.svg"
      /></template>
      <template #title>{{ PleaseNote }}</template>
      <template #description
        >{{ InOrderToDeleteYourAccountEnterYourUsernameInTheFieldAboveAndClickYes }}</template
      >
    </TipMessage>
  </ConfirmDialog>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const DoYouReallyWishToCloseYourAccount = returnTranslation(lang, 'DoYouReallyWishToCloseYourAccount');
const ThisActionWillDeleteYourMerginMapsAccountIfYouAreAWorkspaceOwnerYouNeedToTransferTheOwnershipToSomebodyElseOrCloseTheWorkspace = returnTranslation(lang, 'ThisActionWillDeleteYourMerginMapsAccountIfYouAreAWorkspaceOwnerYouNeedToTransferTheOwnershipToSomebodyElseOrCloseTheWorkspace');
const No = returnTranslation(lang, 'No');
const Yes = returnTranslation(lang, 'Yes');
const Username = returnTranslation(lang, 'Username');
const PleaseNote = returnTranslation(lang, 'PleaseNote');
const InOrderToDeleteYourAccountEnterYourUsernameInTheFieldAboveAndClickYes = returnTranslation(lang, 'InOrderToDeleteYourAccountEnterYourUsernameInTheFieldAboveAndClickYes');

import TipMessage from '@/common/components/TipMessage.vue'
import { DeleteAccountConfirmProps } from '@/modules'
import ConfirmDialog from '@/modules/dialog/components/ConfirmDialog.vue'

defineProps<DeleteAccountConfirmProps>()
const emit = defineEmits(['confirm'])

function confirm() {
  emit('confirm')
}
</script>
