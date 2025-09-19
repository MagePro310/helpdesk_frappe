<template>
  <div class="bg-white/80 backdrop-blur-sm border rounded-xl shadow-sm">
    <div class="px-4 py-3 border-b border-gray-100">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-sm font-semibold text-gray-900">Real-time Notifications</h3>
          <p class="text-xs text-gray-500" v-if="lastUpdated">
            Updated {{ lastUpdated }}
          </p>
        </div>
        <div class="flex items-center gap-2">
          <button
            @click="refreshNotifications"
            class="p-1 text-gray-400 hover:text-gray-600 transition-colors"
            :disabled="notifications.loading"
          >
            <LucideRefreshCw
              class="size-4"
              :class="{ 'animate-spin': notifications.loading }"
            />
          </button>
          <span
            v-if="unreadCount > 0"
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800"
          >
            {{ unreadCount }}
          </span>
        </div>
      </div>
    </div>

    <div class="max-h-80 overflow-y-auto">
      <div v-if="notifications.loading && !notifications.data?.length" class="p-4">
        <div class="animate-pulse space-y-3">
          <div class="h-4 bg-gray-200 rounded w-3/4"></div>
          <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          <div class="h-4 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>

      <div v-else-if="!notifications.data?.length" class="p-4 text-center">
        <LucideBell class="size-8 text-gray-300 mx-auto mb-2" />
        <p class="text-sm text-gray-500">No new notifications</p>
      </div>

      <div v-else>
        <div
          v-for="notification in notifications.data"
          :key="notification.name"
          class="px-4 py-3 border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer"
          :class="{
            'bg-blue-50 border-blue-100': !notification.read,
            'opacity-70': notification.read
          }"
          @click="markAsRead(notification)"
        >
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0">
              <div
                class="size-2 rounded-full mt-2"
                :class="getNotificationColor(notification.type)"
              ></div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between">
                <p class="text-sm font-semibold text-gray-900 truncate">
                  {{ notification.title }}
                </p>
                <span class="text-xs text-gray-500">
                  {{ formatTime(notification.creation) }}
                </span>
              </div>
              <div class="mt-1">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium uppercase tracking-wide"
                  :class="getNotificationBadge(notification.type)"
                >
                  {{ getNotificationLabel(notification.type) }}
                </span>
              </div>
              <p class="text-sm text-gray-600 mt-1">
                {{ notification.message }}
              </p>
              <div v-if="notification.action_url" class="mt-2">
                <button
                  class="text-xs text-blue-600 hover:text-blue-800 font-medium"
                  @click.stop="navigateToTicket(notification.action_url)"
                >
                  View Ticket →
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="notifications.data?.length > 0" class="px-4 py-3 border-t border-gray-200">
      <button
        @click="markAllAsRead"
        class="text-sm text-blue-600 hover:text-blue-800 font-medium w-full text-center"
        :disabled="unreadCount === 0 || notifications.loading || markingAll"
      >
        Mark all as read
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { createResource, call, toast } from "frappe-ui";
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useTimeAgo } from "@vueuse/core";

const router = useRouter();

const notifications = createResource({
  url: "helpdesk.api.dashboard.get_dashboard_notifications",
  cache: ["Dashboard", "Notifications"],
  auto: true,
  onSuccess: (data: any[]) => {
    if (!Array.isArray(data)) return;
    data.forEach((item) => {
      if (typeof item.read === "undefined") {
        item.read = false;
      }
    });
    lastRefresh.value = new Date().toISOString();
  },
});

const unreadCount = computed(() => {
  return notifications.data?.filter((n: any) => !n.read)?.length || 0;
});

const markingAll = ref(false);
const lastRefresh = ref<string | null>(null);
const lastUpdatedDisplay = useTimeAgo(lastRefresh);
const lastUpdated = computed(() =>
  lastRefresh.value ? lastUpdatedDisplay.value : null
);

const refreshNotifications = () => {
  notifications.reload();
};

const markAsRead = async (notification: any) => {
  if (!notification.read) {
    try {
      await call({
        method: "helpdesk.api.dashboard.mark_notification_read",
        args: { notification_id: notification.name },
      });
      notification.read = true;
    } catch (error) {
      toast.error("Could not update notification");
    }
  }
};

const markAllAsRead = async () => {
  if (unreadCount.value === 0) {
    return;
  }
  markingAll.value = true;
  try {
    await call({
      method: "helpdesk.api.dashboard.mark_all_notifications_read",
    });
    await notifications.reload();
    toast.success("All notifications cleared");
  } catch (error) {
    toast.error("Unable to mark notifications as read");
  } finally {
    markingAll.value = false;
  }
};

const navigateToTicket = (url: string) => {
  if (url) {
    router.push(url);
  }
};

const getNotificationColor = (type: string) => {
  const colors = {
    'ticket_assigned': 'bg-blue-500',
    'ticket_updated': 'bg-green-500',
    'sla_breach': 'bg-red-500',
    'feedback_received': 'bg-yellow-500',
    'ticket_resolved': 'bg-green-500',
    'default': 'bg-gray-500'
  };
  return colors[type] || colors.default;
};

const getNotificationBadge = (type: string) => {
  const styles = {
    'ticket_assigned': 'bg-blue-100 text-blue-700 border border-blue-200',
    'ticket_updated': 'bg-emerald-100 text-emerald-700 border border-emerald-200',
    'sla_breach': 'bg-red-100 text-red-700 border border-red-200',
    'feedback_received': 'bg-amber-100 text-amber-700 border border-amber-200',
    'ticket_resolved': 'bg-green-100 text-green-700 border border-green-200',
    'default': 'bg-gray-100 text-gray-700 border border-gray-200'
  };
  return styles[type] || styles.default;
};

const getNotificationLabel = (type: string) => {
  const labels: Record<string, string> = {
    ticket_assigned: 'Assignment',
    ticket_updated: 'Update',
    sla_breach: 'SLA',
    feedback_received: 'Feedback',
    ticket_resolved: 'Resolved',
  };
  return labels[type] || 'Alert';
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

// Auto-refresh notifications every 30 seconds
let refreshInterval: number;

onMounted(() => {
  refreshInterval = setInterval(() => {
    refreshNotifications();
  }, 30000);
});

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval);
  }
});
</script>
