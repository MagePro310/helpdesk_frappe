<template>
  <div class="bg-white/80 backdrop-blur-sm border rounded-xl shadow-sm">
    <div class="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
      <h3 class="text-sm font-semibold text-gray-900">Quick Actions</h3>
      <span v-if="lastUpdated" class="text-[11px] text-gray-400">
        Updated {{ lastUpdated }}
      </span>
    </div>

    <div class="p-4">
      <div v-if="isLoading" class="grid grid-cols-2 gap-3">
        <div
          v-for="placeholder in 6"
          :key="placeholder"
          class="h-[92px] rounded-lg bg-gray-100 animate-pulse"
        ></div>
      </div>
      <div v-else class="grid grid-cols-2 gap-3">
        <!-- Create New Ticket -->
        <button
          @click="createNewTicket"
          class="flex flex-col items-center justify-center p-3 border border-gray-200 rounded-lg bg-gradient-to-br from-white via-white to-gray-50 hover:shadow-md hover:-translate-y-[1px] transition-all group"
        >
          <LucidePlus class="size-6 text-blue-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">New Ticket</span>
          <span class="text-xs text-gray-500">Create ticket</span>
        </button>

        <!-- Bulk Actions -->
        <button
          @click="openBulkActions"
          class="flex flex-col items-center justify-center p-3 border border-gray-200 rounded-lg bg-gradient-to-br from-white via-white to-gray-50 hover:shadow-md hover:-translate-y-[1px] transition-all group"
        >
          <LucideList class="size-6 text-green-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">Bulk Actions</span>
          <span class="text-xs text-gray-500">Update multiple</span>
        </button>

        <!-- My Tickets -->
        <button
          @click="viewMyTickets"
          class="flex flex-col items-center justify-center p-3 border border-gray-200 rounded-lg bg-gradient-to-br from-white via-white to-gray-50 hover:shadow-md hover:-translate-y-[1px] transition-all group"
        >
          <LucideUser class="size-6 text-purple-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">My Tickets</span>
          <span class="text-xs text-gray-500">{{ myTicketsCount }} open</span>
        </button>

        <!-- Team Tickets -->
        <button
          v-if="isManager"
          @click="viewTeamTickets"
          class="flex flex-col items-center justify-center p-3 border border-gray-200 rounded-lg bg-gradient-to-br from-white via-white to-gray-50 hover:shadow-md hover:-translate-y-[1px] transition-all group"
        >
          <LucideUsers class="size-6 text-orange-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">Team Tickets</span>
          <span class="text-xs text-gray-500">{{ teamTicketsCount }} open</span>
        </button>

        <!-- Reports -->
        <button
          @click="viewReports"
          class="flex flex-col items-center justify-center p-3 border border-gray-200 rounded-lg bg-gradient-to-br from-white via-white to-gray-50 hover:shadow-md hover:-translate-y-[1px] transition-all group"
        >
          <LucideBarChart class="size-6 text-indigo-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">Reports</span>
          <span class="text-xs text-gray-500">Analytics</span>
        </button>

        <!-- Settings -->
        <button
          v-if="isManager"
          @click="openSettings"
          class="flex flex-col items-center justify-center p-3 border border-gray-200 rounded-lg bg-gradient-to-br from-white via-white to-gray-50 hover:shadow-md hover:-translate-y-[1px] transition-all group"
        >
          <LucideSettings class="size-6 text-gray-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">Settings</span>
          <span class="text-xs text-gray-500">Configure</span>
        </button>
      </div>

      <!-- Quick Filters -->
      <div class="mt-4 pt-4 border-t border-gray-200">
        <h4 class="text-xs font-medium text-gray-700 uppercase tracking-wide mb-3">
          Quick Filters
        </h4>
        <div v-if="isLoading" class="flex flex-wrap gap-2">
          <div
            v-for="placeholder in 4"
            :key="`filter-${placeholder}`"
            class="h-6 w-28 bg-gray-100 rounded-full animate-pulse"
          ></div>
        </div>
        <div v-else class="flex flex-wrap gap-2">
          <button
            v-for="filter in quickFilters"
            :key="filter.name"
            @click="applyQuickFilter(filter)"
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 hover:bg-gray-200 transition-colors"
          >
            <span
              class="size-2 rounded-full mr-1"
              :class="filter.color"
            ></span>
            {{ filter.label }}
            <span class="ml-1 text-gray-600">({{ filter.count || 0 }})</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { createResource } from "frappe-ui";
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useTimeAgo } from "@vueuse/core";

const router = useRouter();
const { isManager, userId } = useAuthStore();

const ticketCounts = createResource({
  url: "helpdesk.api.dashboard.get_quick_action_counts",
  auto: true,
});

const isLoading = computed(() => ticketCounts.loading && !ticketCounts.data);
const myTicketsCount = computed(() => ticketCounts.data?.my_tickets || 0);
const teamTicketsCount = computed(() => ticketCounts.data?.team_tickets || 0);
const lastRefresh = ref<string | null>(null);
const lastUpdatedDisplay = useTimeAgo(lastRefresh);
const lastUpdated = computed(() =>
  lastRefresh.value ? lastUpdatedDisplay.value : null
);

const quickFilters = computed(() => [
  {
    name: "high_priority",
    label: "High Priority",
    color: "bg-red-500",
    count: ticketCounts.data?.high_priority || 0,
    filters: { priority: "High" }
  },
  {
    name: "overdue",
    label: "Overdue",
    color: "bg-orange-500",
    count: ticketCounts.data?.overdue || 0,
    filters: { is_overdue: true }
  },
  {
    name: "unassigned",
    label: "Unassigned",
    color: "bg-yellow-500",
    count: ticketCounts.data?.unassigned || 0,
    filters: { _assign: ["is", "not set"] }
  },
  {
    name: "pending_feedback",
    label: "Pending Feedback",
    color: "bg-blue-500",
    count: ticketCounts.data?.pending_feedback || 0,
    filters: { status: "Waiting for Customer" }
  }
]);

const createNewTicket = () => {
  router.push("/tickets/new");
};

const openBulkActions = () => {
  router.push("/tickets?bulk=true");
};

const viewMyTickets = () => {
  router.push({
    path: "/tickets",
    query: { _assign: userId }
  });
};

const viewTeamTickets = () => {
  router.push("/tickets?view=team");
};

const viewReports = () => {
  router.push("/reports");
};

const openSettings = () => {
  router.push("/settings");
};

const applyQuickFilter = (filter: any) => {
  router.push({
    path: "/tickets",
    query: filter.filters
  });
};

let refreshHandle: number | null = null;

onMounted(() => {
  refreshHandle = window.setInterval(async () => {
    await ticketCounts.reload();
  }, 120000);
});

onUnmounted(() => {
  if (refreshHandle) {
    clearInterval(refreshHandle);
  }
});

ticketCounts.onSuccess = () => {
  lastRefresh.value = new Date().toISOString();
};
</script>
