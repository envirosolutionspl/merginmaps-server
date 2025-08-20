<!--
Copyright (C) Lutra Consulting Limited

SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
-->

<template>
  <PDataView
    :value="accessRequests"
    :lazy="true"
    :paginator="accessRequestsCount > 10"
    :loading="loading"
    :rows="options.itemsPerPage"
    :totalRecords="accessRequestsCount"
    :data-key="'id'"
    :paginator-template="FirstPageLinkPrevPageLinkPageLinksNextPageLinkLastPageLink"
    size="small"
    @page="onPage"
  >
    <template #header>
      <h3 class="font-semibold paragraph-p6 text-color">{{ AccessRequests }}</h3>
    </template>
    <template #list="slotProps">
      <template v-for="item in slotProps.items" :key="item.id">
        <!-- Row -->
        <div
          class="flex flex-column lg:flex-row align-items-center justify-content-between px-4 py-2 mt-0 border-bottom-1 border-gray-200 gap-2"
        >
          <p
            v-if="loggedUser.username === item.requested_by"
            class="w-12 lg:w-6 paragraph-p6"
          >
            {{ YouRequestedAnAccessToProject }}
            <span class="font-semibold">{{ item.project_name }}</span> {{ InWorkspace }}<span class="font-semibold">{{ item.namespace }}</span
            >.
          </p>
          <p v-else class="w-12 lg:w-6 paragraph-p6">
            {{ User }}
            <span class="font-semibold">{{ item.requested_by }}</span>
            {{ RequestedAnAccessToYourProject }}
            <span class="font-semibold">{{ item.project_name }}.</span>
          </p>
          <div
            class="flex w-12 lg:w-4 align-items-center flex-wrap lg:flex-nowrap row-gap-2"
          >
            <p class="opacity-80 paragraph-p6 w-12">
              <span v-tooltip.right="{ value: $filters.datetime(item.expire) }">
                <template
                  v-if="$filters.remainingtime(item.expire) === 'expired'"
                  >{{ Expired }}</template
                >
                <template v-else
                  >{{ ExpiringIn }}
                  {{ $filters.remainingtime(item.expire) }}</template
                >
              </span>
            </p>
            <AppDropdown
              v-if="showAccept"
              :options="availablePermissions"
              v-model="permissions[item.id]"
              @change="(e) => permissionsChange(e, item)"
              :disabled="expired(item.expire)"
              class="w-6 lg:w-5 lg:mr-2"
            />
            <div class="flex justify-content-end w-6 lg:w-4">
              <PButton
                icon="ti ti-x"
                rounded
                :aria-label="Disallow"
                severity="danger"
                class="mr-2"
                @click="cancelRequest(item)"
              />
              <PButton
                v-if="showAccept"
                icon="ti ti-check"
                rounded
                :aria-label="Accept"
                severity="success"
                :disabled="expired(item.expire)"
                @click="acceptRequest(item)"
              />
            </div>
          </div>
        </div>
      </template>
    </template>
    <template #empty>
      <p>{{ NoAccessRequestsFound }}</p>
    </template>
  </PDataView>
</template>

<script setup lang="ts">
import returnTranslation from '@/../../lang/translate';
const lang = import.meta.env.VITE_LANG

const FirstPageLinkPrevPageLinkPageLinksNextPageLinkLastPageLink = returnTranslation(lang, 'FirstPageLinkPrevPageLinkPageLinksNextPageLinkLastPageLink');
const AccessRequests = returnTranslation(lang, 'AccessRequests');
const InWorkspace = returnTranslation(lang, 'InWorkspace');
const User = returnTranslation(lang, 'User');
const RequestedAnAccessToYourProject = returnTranslation(lang, 'RequestedAnAccessToYourProject');
const YouRequestedAnAccessToProject = returnTranslation(lang, 'YouRequestedAnAccessToProject');
const Expired = returnTranslation(lang, 'Expired');
const ExpiringIn = returnTranslation(lang, 'ExpiringIn');
const Disallow = returnTranslation(lang, 'Disallow');
const Accept = returnTranslation(lang, 'Accept');
const NoAccessRequestsFound = returnTranslation(lang, 'NoAccessRequestsFound');
</script>

<script lang="ts">
import { mapActions, mapState } from 'pinia'
import { DataViewPageEvent } from 'primevue/dataview'
import { DropdownChangeEvent } from 'primevue/dropdown'
import { defineComponent } from 'vue'

import AppDropdown from '@/common/components/AppDropdown.vue'
import { ProjectPermissionName } from '@/common/permission_utils'
import { useUserStore } from '@/main'
import { useNotificationStore } from '@/modules/notification/store'
import { useProjectStore } from '@/modules/project/store'
import {
  GetAccessRequestsPayload,
  AccessRequest
} from '@/modules/project/types'

export default defineComponent({
  name: 'AccessRequestTableTemplate',
  components: { AppDropdown },
  props: {
    namespace: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      loading: false,
      options: {
        // Default is order_params=expire ASC
        sortBy: 'expire',
        sortDesc: false,
        itemsPerPage: 10,
        page: 1
      },
      selectedPermissions: {}
    }
  },
  computed: {
    ...mapState(useProjectStore, [
      'accessRequests',
      'accessRequestsCount',
      'availablePermissions'
    ]),
    ...mapState(useUserStore, ['loggedUser']),
    showAccept() {
      return this.namespace != null
    },
    permissions(): Record<number, ProjectPermissionName> {
      return {
        ...this.accessRequests.reduce(
          (acc, curr) => ({
            ...acc,
            [curr.id]: 'read'
          }),
          {}
        ),
        ...this.selectedPermissions
      }
    }
  },
  methods: {
    ...mapActions(useProjectStore, [
      'cancelProjectAccessRequest',
      'acceptProjectAccessRequest',
      'getAccessRequests'
    ]),
    ...mapActions(useNotificationStore, ['error']),

    onPage(e: DataViewPageEvent) {
      this.options.page = e.page + 1
      this.options.itemsPerPage = e.rows
      this.fetchItems()
    },
    permissionsChange(e: DropdownChangeEvent, item: AccessRequest) {
      const { value } = e
      const { id } = item
      this.selectedPermissions[id] = value
    },
    /** Update pagination in case of last accepting / canceling feature */
    async updatePaginationOrFetch() {
      if (this.accessRequests.length === 1 && this.options.page > 1) {
        this.options.page -= 1
      }
      await this.fetchItems()
    },
    async acceptRequest(request) {
      try {
        const data = {
          permissions: this.permissions[request.id]
        }
        await this.acceptProjectAccessRequest({
          data,
          itemId: request.id,
          workspace: this.namespace
        })
        await this.updatePaginationOrFetch()
      } catch (err) {
        this.$emit('accept-access-request-error', err)
      }
    },
    expired(expire) {
      return Date.parse(expire) < Date.now()
    },
    async cancelRequest(request) {
      await this.cancelProjectAccessRequest({
        itemId: request.id,
        workspace: this.namespace
      })
      await this.updatePaginationOrFetch()
    },
    async fetchItems() {
      this.loading = true
      try {
        const payload: GetAccessRequestsPayload = {
          namespace: this.namespace,
          params: {
            page: this.options.page,
            per_page: this.options.itemsPerPage,
            order_params:
              this.options.sortBy &&
              `${this.options.sortBy} ${this.options.sortDesc ? 'DESC' : 'ASC'}`
          }
        }
        await this.getAccessRequests(payload)
      } finally {
        this.loading = false
      }
    }
  }
})
</script>

<style lang="scss" scoped></style>
