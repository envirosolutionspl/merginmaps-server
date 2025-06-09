<template>
  <form @submit.prevent="download" class="flex flex-column pb-4 gap-2">
    <span class="p-input-filled">
      <label id="period-label">{{ Translation_Period }}</label>
      <app-dropdown
        aria-labelledby="period-label"
        v-model="period"
        :options="periodOptions"
      />
    </span>

    <span class="p-input-filled w-full">
      <label for="range">{{ Translation_CustomRange }}</label>
      <PCalendar
        inputId="range"
        v-model="range"
        selectionMode="range"
        :disabled="Number(period) > -1"
        :max-date="maxDate"
        class="w-full"
        :placeholder="Translation_SelectDateRange"
      />
    </span>

    <!-- Footer -->
    <div
      class="w-full flex flex-column lg:flex-row justify-content-between align-items-center mt-4"
    >
      <PButton
        severity="secondary"
        @click="close"
        class="w-12 mb-2 lg:mb-0 lg:mr-2 lg:w-6"
        data-cy="clone-dialog-close-btn"
        :label="Translation_Cancel"
      />
      <PButton
        type="submit"
        class="w-12 lg:w-6"
        :label="Translation_Download"
        :disabled="range.filter(Boolean).length < 2"
      />
    </div>
  </form>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const Translation_Period = returnTranslation(lang, 'adminlib_admin_ReportDownloadDialog_Period');
const Translation_CustomRange = returnTranslation(lang, 'adminlib_admin_ReportDownloadDialog_CustomRange');
const Translation_SelectDateRange = returnTranslation(lang, 'adminlib_admin_ReportDownloadDialog_SelectDateRange');
const Translation_Cancel = returnTranslation(lang, 'adminlib_admin_ReportDownloadDialog_Cancel');
const Translation_Download = returnTranslation(lang, 'adminlib_admin_ReportDownloadDialog_Download');


import { AppDropdown, DropdownOption, useDialogStore } from '@mergin/lib'
import subMonths from 'date-fns/subMonths'
import { ref, watchEffect } from 'vue'

import { useAdminStore } from '@/main'

const dialogStore = useDialogStore()
const adminStore = useAdminStore()

const maxDate = ref<Date>(new Date())
const period = ref<string>('3')
const periodOptions = ref<DropdownOption[]>([
  { label: returnTranslation(lang, 'adminlib_admin_ReportDownloadDialog_Last3Months'), value: '3' },
  { label: returnTranslation(lang, 'adminlib_admin_ReportDownloadDialog_Last6Months'), value: '6' },
  { label: returnTranslation(lang, 'adminlib_admin_ReportDownloadDialog_Last12Months'), value: '12' },
  { label: returnTranslation(lang, 'adminlib_admin_ReportDownloadDialog_CustomRange'), value: '-1' }
])
const range = ref<Array<Date>>([
  subMonths(new Date(), Number(period.value)),
  new Date()
])

watchEffect(() => {
  const periodValue = Number(period.value)
  if (periodValue < 0) {
    range.value = []
    return
  }
  range.value = [subMonths(new Date(), periodValue), new Date()]
})

function close() {
  dialogStore.closeDialog()
}

function download() {
  const [from, to] = range.value
  adminStore.downloadReport({ from, to })
}
</script>
