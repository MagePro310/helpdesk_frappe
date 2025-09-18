<template>
  <div class="bg-white border rounded-lg shadow-sm">
    <div class="px-4 py-3 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <h3 class="text-sm font-medium text-gray-900">Recent Activity</h3>
        <div class="flex items-center gap-2">
          <button
            @click="refreshActivities"
            class="p-1 text-gray-400 hover:text-gray-600 transition-colors"
            :disabled="activities.loading"
          >
            <LucideRefreshCw
              class="size-4"
              :class="{ 'animate-spin': activities.loading }"
            />
          </button>
          <Dropdown :options="filterOptions" v-model="selectedFilter">
            <template #default>
              <button class="text-sm text-gray-600 hover:text-gray-800 flex items-center gap-1">
                <LucideFilter class="size-4" />
                {{ selectedFilter }}
                <LucideChevronDown class="size-3" />
              </button>
            </template>
          </Dropdown>
        </div>
      </div>
    </div>

    <div class="max-h-96 overflow-y-auto">
      <div v-if="activities.loading && !activities.data?.length" class="p-4">
        <div class="animate-pulse space-y-4">
          <div v-for="i in 5" :key="i" class="flex gap-3">
            <div class="size-8 bg-gray-200 rounded-full"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-200 rounded w-3/4"></div>
              <div class="h-3 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="!activities.data?.length" class="p-8 text-center">
        <LucideActivity class="size-8 text-gray-300 mx-auto mb-2" />
        <p class="text-sm text-gray-500">No recent activities</p>
      </div>

      <div v-else class="divide-y divide-gray-100">
        <div
          v-for="activity in filteredActivities"
          :key="activity.id"
          class="p-4 hover:bg-gray-50 transition-colors"
        >
          <div class="flex gap-3">
            <!-- Activity Icon -->
            <div class="flex-shrink-0">
              <div
                class="size-8 rounded-full flex items-center justify-center"
                :class="getActivityIconClass(activity.type)"
              >
                <component
                  :is="getActivityIcon(activity.type)"
                  class="size-4 text-white"
                />
              </div>
            </div>

            <!-- Activity Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <p class="text-sm font-medium text-gray-900">
                    {{ activity.title }}
                  </p>
                  <p class="text-sm text-gray-600 mt-1">
                    {{ activity.description }}
                  </p>
                  
                  <!-- Activity Details -->
                  <div v-if="activity.details" class="mt-2">
                    <div class="text-xs text-gray-500 space-y-1">
                      <div v-if="activity.details.ticket">
                        Ticket: 
                        <button
                          @click="navigateToTicket(activity.details.ticket)"
                          class="text-blue-600 hover:text-blue-800 font-medium"
                        >
                          {{ activity.details.ticket }}
                        </button>
                      </div>
                      <div v-if="activity.details.priority">
                        Priority: 
                        <span
                          class="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium"
                          :class="getPriorityClass(activity.details.priority)"
                        >
                          {{ activity.details.priority }}
                        </span>
                      </div>
                      <div v-if="activity.details.status">
                        Status: {{ activity.details.status }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Timestamp -->
                <div class="flex flex-col items-end">
                  <span class="text-xs text-gray-500">
                    {{ formatTime(activity.timestamp) }}
                  </span>
                  <div v-if="activity.user" class="flex items-center mt-1">
                    <UserAvatar :name="activity.user" class="size-5 mr-1" />
                    <span class="text-xs text-gray-600">
                      {{ getUserDisplayName(activity.user) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Load More Button -->
    <div v-if="hasMore" class="px-4 py-3 border-t border-gray-200">
      <button
        @click="loadMore"
        class="text-sm text-blue-600 hover:text-blue-800 font-medium w-full text-center"
        :disabled="activities.loading"
      >
        Load more activities
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { createResource, Dropdown } from "frappe-ui";
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import UserAvatar from "@/components/UserAvatar.vue";

const router = useRouter();

const selectedFilter = ref("All");
const hasMore = ref(true);
const currentPage = ref(1);

const filterOptions = [
  { label: "All", value: "All" },
  { label: "Ticket Updates", value: "ticket_update" },
  { label: "Assignments", value: "assignment" },
  { label: "Status Changes", value: "status_change" },
  { label: "Comments", value: "comment" },
  { label: "SLA Events", value: "sla_event" }
];

const activities = createResource({
  url: "helpdesk.api.dashboard.get_recent_activities",
  params: {
    page: currentPage.value,
    filter_type: selectedFilter.value
  },
  auto: true,
});

const filteredActivities = computed(() => {
  if (!activities.data) return [];
  if (selectedFilter.value === "All") return activities.data;
  return activities.data.filter((activity: any) => activity.type === selectedFilter.value);
});

const refreshActivities = () => {
  currentPage.value = 1;
  hasMore.value = true;
  activities.update({
    params: {
      page: currentPage.value,
      filter_type: selectedFilter.value
    }
  });
  activities.reload();
};

const loadMore = () => {
  currentPage.value += 1;
  // In a real implementation, you would append new data
  activities.update({
    params: {
      page: currentPage.value,
      filter_type: selectedFilter.value
    }
  });
  activities.reload();
};

const navigateToTicket = (ticketId: string) => {
  router.push(`/tickets/${ticketId}`);
};

const getActivityIcon = (type: string) => {
  const icons = {
    'ticket_created': 'LucidePlus',
    'ticket_update': 'LucideEdit',
    'assignment': 'LucideUser',
    'status_change': 'LucideArrowRight',
    'comment': 'LucideMessageCircle',
    'sla_event': 'LucideClock',
    'resolution': 'LucideCheckCircle',
    'escalation': 'LucideAlertTriangle',
    'default': 'LucideActivity'
  };
  return icons[type] || icons.default;
};

const getActivityIconClass = (type: string) => {
  const classes = {
    'ticket_created': 'bg-green-500',
    'ticket_update': 'bg-blue-500',
    'assignment': 'bg-purple-500',
    'status_change': 'bg-orange-500',
    'comment': 'bg-indigo-500',
    'sla_event': 'bg-red-500',
    'resolution': 'bg-green-600',
    'escalation': 'bg-red-600',
    'default': 'bg-gray-500'
  };
  return classes[type] || classes.default;
};

const getPriorityClass = (priority: string) => {
  const classes = {
    'High': 'bg-red-100 text-red-800',
    'Medium': 'bg-yellow-100 text-yellow-800',
    'Low': 'bg-green-100 text-green-800',
    'Urgent': 'bg-red-200 text-red-900'
  };
  return classes[priority] || 'bg-gray-100 text-gray-800';
};

const formatTime = (timestamp: string) => {
  const now = new Date();
  const time = new Date(timestamp);
  const diffMs = now.getTime() - time.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return time.toLocaleDateString();
};

const getUserDisplayName = (userId: string) => {
  // In a real implementation, you might want to cache user names
  return userId.split('@')[0] || userId;
};

watch(selectedFilter, () => {
  refreshActivities();
});

// Auto-refresh activities every 60 seconds
let refreshInterval: number;

onMounted(() => {
  refreshInterval = setInterval(() => {
    if (currentPage.value === 1) {
      refreshActivities();
    }
  }, 60000);
});

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval);
  }
});
</script>