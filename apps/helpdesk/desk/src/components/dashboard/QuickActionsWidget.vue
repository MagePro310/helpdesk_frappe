<template>
  <div class="bg-white border rounded-lg shadow-sm">
    <div class="px-4 py-3 border-b border-gray-200">
      <h3 class="text-sm font-medium text-gray-900">Quick Actions</h3>
    </div>

    <div class="p-4">
      <div class="grid grid-cols-2 gap-3">
        <!-- Create New Ticket -->
        <button
          @click="createNewTicket"
          class="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-colors group"
        >
          <LucidePlus class="size-6 text-blue-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">New Ticket</span>
          <span class="text-xs text-gray-500">Create ticket</span>
        </button>

        <!-- Bulk Actions -->
        <button
          @click="openBulkActions"
          class="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-colors group"
        >
          <LucideList class="size-6 text-green-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">Bulk Actions</span>
          <span class="text-xs text-gray-500">Update multiple</span>
        </button>

        <!-- My Tickets -->
        <button
          @click="viewMyTickets"
          class="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-colors group"
        >
          <LucideUser class="size-6 text-purple-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">My Tickets</span>
          <span class="text-xs text-gray-500">{{ myTicketsCount }} open</span>
        </button>

        <!-- Team Tickets -->
        <button
          v-if="isManager"
          @click="viewTeamTickets"
          class="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-colors group"
        >
          <LucideUsers class="size-6 text-orange-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">Team Tickets</span>
          <span class="text-xs text-gray-500">{{ teamTicketsCount }} open</span>
        </button>

        <!-- Reports -->
        <button
          @click="viewReports"
          class="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-colors group"
        >
          <LucideBarChart class="size-6 text-indigo-600 mb-2 group-hover:scale-110 transition-transform" />
          <span class="text-sm font-medium text-gray-900">Reports</span>
          <span class="text-xs text-gray-500">Analytics</span>
        </button>

        <!-- Settings -->
        <button
          v-if="isManager"
          @click="openSettings"
          class="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-colors group"
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
        <div class="flex flex-wrap gap-2">
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
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const { isManager, userId } = useAuthStore();

const ticketCounts = createResource({
  url: "helpdesk.api.dashboard.get_quick_action_counts",
  auto: true,
});

const myTicketsCount = computed(() => ticketCounts.data?.my_tickets || 0);
const teamTicketsCount = computed(() => ticketCounts.data?.team_tickets || 0);

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

onMounted(() => {
  // Refresh counts every 2 minutes
  setInterval(() => {
    ticketCounts.reload();
  }, 120000);
});
</script>