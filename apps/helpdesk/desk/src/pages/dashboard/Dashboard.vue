<template>
  <div class="flex flex-col">
    <LayoutHeader>
      <template #left-header>
        <div class="text-lg font-medium text-gray-900">Dashboard</div>
      </template>
      <template #right-header>
        <div class="flex items-center gap-2">
          <!-- Export Button -->
          <Dropdown :options="exportOptions">
            <template #default>
              <Button variant="outline" size="sm">
                <template #prefix>
                  <LucideDownload class="size-4" />
                </template>
                Export
              </Button>
            </template>
          </Dropdown>

          <!-- Dashboard Settings -->
          <Button variant="ghost" size="sm" @click="openDashboardSettings">
            <template #prefix>
              <LucideSettings class="size-4" />
            </template>
          </Button>
        </div>
      </template>
    </LayoutHeader>

    <div class="p-5 w-full overflow-y-scroll">
      <!-- Filters -->
      <div class="mb-4 flex items-center gap-4 overflow-x-auto">
        <Dropdown
          v-if="!showDatePicker"
          :options="options"
          class="!form-control !w-48"
          v-model="preset"
          placeholder="Select Range"
          @change="filters.period = preset"
        >
          <template #default>
            <div
              class="flex justify-between !w-48 items-center border border-outline-gray-2 rounded text-ink-gray-8 px-2 py-1.5 hover:border-outline-gray-3 hover:shadow-sm focus:border-outline-gray-4 focus:shadow-sm focus:ring-0 focus-visible:ring-0 transition-colors h-7 cursor-pointer"
            >
              <div class="flex items-center">
                <LucideCalendar class="size-4 text-ink-gray-5 mr-2" />
                <span class="text-base">{{ preset }}</span>
              </div>
              <LucideChevronDown class="size-4 text-ink-gray-5" />
            </div>
          </template>
        </Dropdown>
        <DateRangePicker
          v-else
          class="!w-48"
          ref="datePickerRef"
          v-model="filters.period"
          variant="outline"
          placeholder="Period"
          @update:model-value="
            (e:string) => {
              showDatePicker = false;
              preset = formatter(e);
            }
          "
          :formatter="formatRange"
        >
          <template #prefix>
            <LucideCalendar class="size-4 text-ink-gray-5 mr-2" />
          </template>
        </DateRangePicker>
        <Link
          v-if="isManager"
          class="form-control w-48"
          doctype="HD Team"
          placeholder="Team"
          v-model="filters.team"
          :page-length="5"
          :hide-me="true"
        >
          <template #prefix>
            <LucideUsers class="size-4 text-ink-gray-5 mr-2" />
          </template>
        </Link>
        <Link
          v-if="isManager"
          class="form-control w-48"
          doctype="HD Agent"
          placeholder="Agent"
          v-model="filters.agent"
          :page-length="5"
          :filters="agentFilter"
          :hide-me="true"
        >
          <template #prefix>
            <LucideUser class="size-4 text-ink-gray-5 mr-2" />
          </template>
        </Link>
      </div>
      <!-- Charts -->
      <div v-if="!loading" class="transition-all animate-fade-in duration-300 space-y-6">
        <!-- Enhanced Dashboard Layout -->
        <div
          v-if="preferences.showHighlights"
          class="grid grid-cols-1 lg:grid-cols-4 gap-6"
        >
          <!-- Quick Actions Widget -->
          <div class="lg:col-span-1">
            <QuickActionsWidget />
          </div>

          <!-- Real-time Notifications -->
          <div class="lg:col-span-1">
            <NotificationsPanel />
          </div>

          <!-- Recent Activity Timeline -->
          <div class="lg:col-span-2">
            <RecentActivityTimeline />
          </div>
        </div>

        <!-- Number Cards -->
        <div
          v-if="preferences.showNumberCards && !numberCards.loading"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4"
        >
          <Tooltip
            v-for="(config, index) in numberCards.data"
            :text="config.tooltip"
          >
            <NumberChart
              :key="index"
              class="border rounded-xl bg-white/60 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow"
              :config="config"
            />
          </Tooltip>
        </div>

        <!-- Performance Analytics Section -->
        <div v-if="preferences.showPerformance">
          <PerformanceAnalytics :filters="filters" />
        </div>

        <!-- Trend Charts -->
        <div
          v-if="preferences.showTrends && !trendData.loading"
          class="grid grid-cols-1 lg:grid-cols-2 gap-4"
        >
          <div
            class="border rounded-xl bg-white/70 backdrop-blur-sm min-h-80 p-2 shadow-sm"
            v-for="(chart, index) in trendData.data"
            :key="index"
          >
            <component :is="getChartType(chart)" />
          </div>
        </div>
        <!-- Master Data Charts -->
        <div
          v-if="preferences.showSegments && !masterData.loading"
          class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full"
        >
          <div
            class="border rounded-xl bg-white/70 backdrop-blur-sm p-2 shadow-sm"
            v-for="(chart, index) in masterData.data"
            :key="index"
          >
            <component :is="getChartType(chart)" />
          </div>
        </div>
      </div>
      <!-- Loading State -->
      <div
        v-else
        class="flex items-center justify-center h-[240px] gap-2 rounded transition-all animate-fade-in"
      >
        <Button :loading="true" size="2xl" variant="ghost" />
      </div>
    </div>

    <Dialog v-model="showScheduleDialog" :options="scheduleDialogOptions">
      <template #body-content>
        <div class="space-y-4">
          <FormControl
            type="textarea"
            label="Recipients"
            placeholder="agent@example.com, manager@example.com"
            v-model="scheduleForm.recipients"
            helper-text="Comma separated list of email addresses"
          />
          <FormControl
            type="select"
            label="Frequency"
            v-model="scheduleForm.frequency"
            :options="scheduleFrequencyOptions"
          />
          <div class="grid grid-cols-2 gap-4">
            <FormControl
              type="select"
              label="Delivery Time"
              v-model="scheduleForm.deliveryTime"
              :options="scheduleTimeOptions"
            />
            <FormControl
              type="select"
              label="Format"
              v-model="scheduleForm.format"
              :options="scheduleFormatOptions"
            />
          </div>
          <FormControl
            type="checkbox"
            :label="'Include detailed charts'"
            v-model="scheduleForm.includeCharts"
          />
        </div>
      </template>
      <template #actions>
        <Button
          variant="solid"
          class="w-full"
          :loading="scheduleSubmitting"
          @click="confirmScheduleReport"
        >
          Schedule Report
        </Button>
      </template>
    </Dialog>

    <Dialog v-model="showSettingsDialog" :options="settingsDialogOptions">
      <template #body-content>
        <div class="space-y-4">
          <p class="text-sm text-gray-500">
            Toggle the sections you want to see on your dashboard. Changes are saved automatically for your browser.
          </p>
          <div class="grid grid-cols-1 gap-3">
            <FormControl
              v-for="section in settingsSections"
              :key="section.key"
              type="checkbox"
              :label="section.label"
              v-model="preferences[section.key]"
            />
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="outline" class="w-full" @click="resetPreferences">
          Reset to defaults
        </Button>
      </template>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { Link } from "@/components";
import { useAuthStore } from "@/stores/auth";
import NotificationsPanel from "@/components/dashboard/NotificationsPanel.vue";
import QuickActionsWidget from "@/components/dashboard/QuickActionsWidget.vue";
import PerformanceAnalytics from "@/components/dashboard/PerformanceAnalytics.vue";
import RecentActivityTimeline from "@/components/dashboard/RecentActivityTimeline.vue";
import {
  AxisChart,
  createResource,
  DateRangePicker,
  dayjs,
  DonutChart,
  Dropdown,
  NumberChart,
  Tooltip,
  usePageMeta,
  Button,
  call,
  Dialog,
  FormControl,
  toast,
} from "frappe-ui";
import { computed, h, onMounted, reactive, ref, watch } from "vue";
import { useStorage } from "@vueuse/core";

const { isManager, userId } = useAuthStore();

const filters = reactive({
  period: getLastXDays(),
  agent: null,
  team: null,
});

const defaultPreferences = {
  showHighlights: true,
  showNumberCards: true,
  showPerformance: true,
  showTrends: true,
  showSegments: true,
};

const preferences = useStorage("helpdesk_dashboard_preferences", {
  ...defaultPreferences,
});

const colors = [
  "#318AD8",
  "#F683AE",
  "#48BB74",
  "#F56B6B",
  "#FACF7A",
  "#44427B",
  "#5FD8C4",
  "#F8814F",
  "#15CCEF",
  "#A6B1B9",
];

const numberCards = createResource({
  url: "helpdesk.api.dashboard.get_dashboard_data",
  cache: ["Analytics", "NumberCards"],
  params: {
    dashboard_type: "number_card",
    filters,
  },
});

const masterData = createResource({
  url: "helpdesk.api.dashboard.get_dashboard_data",
  cache: ["Analytics", "MasterCharts"],
  params: {
    dashboard_type: "master",
    filters,
  },
});

const trendData = createResource({
  url: "helpdesk.api.dashboard.get_dashboard_data",
  cache: ["Analytics", "TrendCharts"],
  params: {
    dashboard_type: "trend",
    filters,
  },
});

const agentFilter = ref(null);
const teamMembers = createResource({
  url: "helpdesk.helpdesk.doctype.hd_team.hd_team.get_team_members",
  cache: ["Analytics", "TeamMembers"],
  params: {
    team: filters.team,
  },
  onSuccess: (data) => {
    // Set Agent Filters
    agentFilter.value = { name: ["in", data] };
  },
});

// Export options
const exportOptions = computed(() => [
  {
    label: "Export as PDF",
    onClick: () => exportDashboard("pdf"),
  },
  {
    label: "Export as Excel",
    onClick: () => exportDashboard("excel"),
  },
  {
    label: "Schedule Report",
    onClick: () => scheduleReport(),
  },
]);

// Dashboard functions
const exportDashboard = async (format: string) => {
  try {
    const response = await call({
      method: "helpdesk.api.dashboard.export_dashboard_data",
      args: {
        format: format,
        filters: {
          from_date: filters.period?.split(",")[0] || null,
          to_date: filters.period?.split(",")[1] || null,
          agent: filters.agent || null,
          team: filters.team || null,
        },
      },
    });
    
    if (response.file_url) {
      // Download the file
      const link = document.createElement("a");
      link.href = response.file_url;
      link.download = response.filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  } catch (error) {
    console.error("Export failed:", error);
  }
};

const showScheduleDialog = ref(false);
const showSettingsDialog = ref(false);
const scheduleSubmitting = ref(false);

const scheduleForm = reactive({
  recipients: "",
  frequency: "Daily",
  deliveryTime: "09:00",
  format: "pdf",
  includeCharts: true,
});

const scheduleFrequencyOptions = [
  { label: "Daily", value: "Daily" },
  { label: "Weekly", value: "Weekly" },
  { label: "Monthly", value: "Monthly" },
];

const scheduleFormatOptions = [
  { label: "PDF", value: "pdf" },
  { label: "Excel", value: "excel" },
];

const scheduleTimeOptions = Array.from({ length: 24 }, (_, hour) => {
  const formatted = `${hour.toString().padStart(2, "0")}:00`;
  return { label: formatted, value: formatted };
});

const scheduleDialogOptions = {
  title: "Schedule Dashboard Report",
  size: "lg" as const,
};

const settingsDialogOptions = {
  title: "Dashboard Sections",
  size: "md" as const,
};

const settingsSections = [
  { key: "showHighlights", label: "Highlights (Quick actions, notifications, activity)" },
  { key: "showNumberCards", label: "KPI number cards" },
  { key: "showPerformance", label: "Performance analytics" },
  { key: "showTrends", label: "Trend charts" },
  { key: "showSegments", label: "Segment breakdown charts" },
];

const scheduleReport = () => {
  showScheduleDialog.value = true;
};

const openDashboardSettings = () => {
  showSettingsDialog.value = true;
};

const resetPreferences = () => {
  Object.assign(preferences.value, defaultPreferences);
  toast.success("Dashboard sections reset");
};

const confirmScheduleReport = async () => {
  if (!scheduleForm.recipients.trim()) {
    toast.error("Please add at least one recipient");
    return;
  }
  scheduleSubmitting.value = true;
  try {
    await call({
      method: "helpdesk.api.dashboard.schedule_dashboard_report",
      args: {
        schedule: {
          ...scheduleForm,
          filters: {
            from_date: filters.period?.split(",")[0] || null,
            to_date: filters.period?.split(",")[1] || null,
            agent: filters.agent || null,
            team: filters.team || null,
          },
        },
      },
    });
    toast.success("Report schedule saved");
    showScheduleDialog.value = false;
  } catch (error) {
    console.error(error);
    toast.error("Could not save schedule");
  } finally {
    scheduleSubmitting.value = false;
  }
};

const loadExistingSchedule = async () => {
  try {
    const response = await call({
      method: "helpdesk.api.dashboard.get_dashboard_schedule",
    });
    if (response?.schedule) {
      const {
        recipients,
        frequency,
        deliveryTime,
        format,
        includeCharts,
      } = response.schedule;
      scheduleForm.recipients = recipients || "";
      scheduleForm.frequency = frequency || "Daily";
      scheduleForm.deliveryTime = deliveryTime || "09:00";
      scheduleForm.format = format || "pdf";
      scheduleForm.includeCharts = includeCharts ?? true;
    }
  } catch (error) {
    console.warn("Unable to load saved schedule", error);
  }
};

watch(
  () => filters.team,
  (newVal) => {
    filters.agent = null; // Reset agent when team is selected
    if (newVal) {
      teamMembers.update({
        params: {
          team: newVal,
        },
      });
      teamMembers.reload();
    }
    if (!newVal) {
      agentFilter.value = null; // Reset agent filter if no team is selected
    }
  }
);

const loading = computed(() => {
  return numberCards.loading || masterData.loading || trendData.loading;
});

function getChartType(chart: any) {
  chart.colors = colors;
  if (chart["type"] === "axis") {
    return h(AxisChart, {
      config: chart,
    });
  }
  if (chart["type"] === "pie") {
    return h(DonutChart, {
      config: chart,
    });
  }
}

function getLastXDays(range: number = 30): string {
  const today = new Date();
  const lastXDate = new Date(today);
  lastXDate.setDate(today.getDate() - range);

  return `${dayjs(lastXDate).format("YYYY-MM-DD")},${dayjs(today).format(
    "YYYY-MM-DD"
  )}`;
}

const showDatePicker = ref(false);
const datePickerRef = ref(null);
const preset = ref("Last 30 Days");

const options = computed(() => [
  {
    group: "Presets",
    hideLabel: true,
    items: [
      {
        label: "Today",
        onClick: () => {
          preset.value = "Today";
          filters.period = getLastXDays(0);
        },
      },
      {
        label: "Last 7 Days",
        onClick: () => {
          preset.value = "Last 7 Days";
          filters.period = getLastXDays(7);
        },
      },
      {
        label: "Last 30 Days",
        onClick: () => {
          preset.value = "Last 30 Days";
          filters.period = getLastXDays(30);
        },
      },
      {
        label: "Last 60 Days",
        onClick: () => {
          preset.value = "Last 60 Days";
          filters.period = getLastXDays(60);
        },
      },
      {
        label: "Last 90 Days",
        onClick: () => {
          preset.value = "Last 90 Days";
          filters.period = getLastXDays(90);
        },
      },
    ],
  },
  {
    label: "Custom Range",
    onClick: () => {
      showDatePicker.value = true;
      setTimeout(() => {
        datePickerRef.value?.open();
      }, 0);
      preset.value = "Custom Range";
      filters.period = null; // Reset period to allow custom date selection
    },
  },
]);

function formatter(range: string) {
  if (!range) {
    filters.period = getLastXDays();
    preset.value = "Last 30 Days";
    return preset.value;
  }
  let [from, to] = range.split(",");
  return `${formatRange(from)} to ${formatRange(to)}`;
}

function formatRange(date: string) {
  const dateObj = new Date(date);
  return dateObj.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year:
      dateObj.getFullYear() === new Date().getFullYear()
        ? undefined
        : "numeric",
  });
}

watch(
  () => filters,
  (newVal) => {
    if (showDatePicker.value) {
      return;
    }
    const filters = {
      from_date: newVal.period?.split(",")[0] || null,
      to_date: newVal.period?.split(",")[1] || null,
      agent: newVal.agent || null,
      team: newVal.team || null,
    };

    numberCards.update({
      params: {
        dashboard_type: "number_card",
        filters: filters,
      },
    });
    numberCards.reload();

    masterData.update({
      params: {
        dashboard_type: "master",
        filters: filters,
      },
    });
    masterData.reload();

    trendData.update({
      params: {
        dashboard_type: "trend",
        filters: filters,
      },
    });
    trendData.reload();
  },
  { deep: true }
);

onMounted(() => {
  loadExistingSchedule();
  if (!isManager) {
    // when filters are updated, resources are reloaded coz of the watcher
    filters.agent = userId;
    return;
  }
  // If not managers call the resources
  numberCards.reload();
  masterData.reload();
  trendData.reload();
});

usePageMeta(() => {
  return {
    title: "Dashboard",
  };
});

watch(
  () => preferences.value,
  (val) => {
    // ensure keys exist if user removed local storage manually
    for (const key of Object.keys(defaultPreferences)) {
      if (typeof val[key] === "undefined") {
        val[key] = defaultPreferences[key as keyof typeof defaultPreferences];
      }
    }
  },
  { deep: true, immediate: true }
);
</script>

<style scoped>
:deep(.form-control button) {
  @apply text-base rounded h-7 py-1.5 border border-outline-gray-2 bg-surface-white placeholder-ink-gray-4 hover:border-outline-gray-3 hover:shadow-sm focus:bg-surface-white focus:border-outline-gray-4 focus:shadow-sm focus:ring-0 focus-visible:ring-0 text-ink-gray-8 transition-colors w-full dark:[color-scheme:dark];
}
:deep(.form-control button > div) {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:deep(.form-control div) {
  width: 100%;
  display: flex;
}

.animate-fade-in {
  animation: fade-in 0.4s ease;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
