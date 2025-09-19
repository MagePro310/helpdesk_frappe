<template>
  <div class="space-y-4">
    <!-- Performance Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-white border rounded-lg p-4 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Avg Response Time</p>
            <p class="text-2xl font-bold text-gray-900">
              {{ displayValue(performanceData.data?.avg_response_time) }}
              <span class="text-sm font-normal text-gray-500">hrs</span>
            </p>
          </div>
          <div class="p-2 bg-blue-100 rounded-lg">
            <LucideClock class="size-6 text-blue-600" />
          </div>
        </div>
        <div class="mt-2 flex items-center">
          <span
            class="text-sm font-medium"
            :class="getPerformanceClass(performanceData.data?.response_time_trend)"
          >
            {{ formatTrend(performanceData.data?.response_time_trend) }}
          </span>
          <span class="text-sm text-gray-500 ml-1">vs last period</span>
        </div>
      </div>

      <div class="bg-white border rounded-lg p-4 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Resolution Rate</p>
            <p class="text-2xl font-bold text-gray-900">
              {{ displayValue(performanceData.data?.resolution_rate) }}
              <span class="text-sm font-normal text-gray-500">%</span>
            </p>
          </div>
          <div class="p-2 bg-green-100 rounded-lg">
            <LucideCheckCircle class="size-6 text-green-600" />
          </div>
        </div>
        <div class="mt-2 flex items-center">
          <span
            class="text-sm font-medium"
            :class="getPerformanceClass(performanceData.data?.resolution_rate_trend)"
          >
            {{ formatTrend(performanceData.data?.resolution_rate_trend) }}
          </span>
          <span class="text-sm text-gray-500 ml-1">vs last period</span>
        </div>
      </div>

      <div class="bg-white border rounded-lg p-4 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Customer Satisfaction</p>
            <p class="text-2xl font-bold text-gray-900">
              {{ displayValue(performanceData.data?.csat_score) }}
              <span class="text-sm font-normal text-gray-500">/5</span>
            </p>
          </div>
          <div class="p-2 bg-yellow-100 rounded-lg">
            <LucideStar class="size-6 text-yellow-600" />
          </div>
        </div>
        <div class="mt-2 flex items-center">
          <span
            class="text-sm font-medium"
            :class="getPerformanceClass(performanceData.data?.csat_trend)"
          >
            {{ formatTrend(performanceData.data?.csat_trend) }}
          </span>
          <span class="text-sm text-gray-500 ml-1">vs last period</span>
        </div>
      </div>
    </div>

    <!-- Agent Performance Chart -->
    <div class="bg-white/80 border rounded-xl shadow-sm backdrop-blur-sm">
      <div class="px-4 py-3 border-b border-gray-200">
        <h3 class="text-sm font-medium text-gray-900">Agent Performance</h3>
      </div>
      <div class="p-4">
        <div v-if="agentPerformance.loading" class="h-80 flex items-center justify-center">
          <div class="animate-pulse">
            <div class="h-4 bg-gray-200 rounded w-48 mb-4"></div>
            <div class="h-32 bg-gray-200 rounded w-full"></div>
          </div>
        </div>
        <div
          v-else-if="!Array.isArray(agentPerformance.data?.data) || !agentPerformance.data?.data?.length"
          class="h-80 flex items-center justify-center text-sm text-gray-500"
        >
          No agent performance data for this period.
        </div>
        <div v-else class="h-80">
          <component
            :is="getChartType(agentPerformance.data)"
            :config="agentPerformance.data"
          />
        </div>
      </div>
    </div>

    <!-- Ticket Velocity Chart -->
    <div class="bg-white/80 border rounded-xl shadow-sm backdrop-blur-sm">
      <div class="px-4 py-3 border-b border-gray-200">
        <h3 class="text-sm font-medium text-gray-900">Ticket Velocity</h3>
      </div>
      <div class="p-4">
        <div v-if="ticketVelocity.loading" class="h-80 flex items-center justify-center">
          <div class="animate-pulse">
            <div class="h-4 bg-gray-200 rounded w-48 mb-4"></div>
            <div class="h-32 bg-gray-200 rounded w-full"></div>
          </div>
        </div>
        <div
          v-else-if="!Array.isArray(ticketVelocity.data?.data) || !ticketVelocity.data?.data?.length"
          class="h-80 flex items-center justify-center text-sm text-gray-500"
        >
          No ticket velocity data for this period.
        </div>
        <div v-else class="h-80">
          <component
            :is="getChartType(ticketVelocity.data)"
            :config="ticketVelocity.data"
          />
        </div>
      </div>
    </div>

    <!-- Team Performance Table -->
    <div v-if="isManager" class="bg-white/80 border rounded-xl shadow-sm backdrop-blur-sm">
      <div class="px-4 py-3 border-b border-gray-200">
        <h3 class="text-sm font-medium text-gray-900">Team Performance</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Agent
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Tickets Resolved
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Avg Response Time
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                CSAT Score
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                SLA Compliance
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <template v-if="hasTeamData">
              <tr v-for="agent in teamPerformance.data" :key="agent.agent">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <UserAvatar :name="agent.agent" class="size-8 mr-3" />
                    <div class="text-sm font-medium text-gray-900">
                      {{ agent.full_name || agent.agent }}
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ agent.tickets_resolved || 0 }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ displayValue(agent.avg_response_time) }} hrs
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <span class="text-sm text-gray-900 mr-2">
                      {{ displayValue(agent.csat_score) }}
                    </span>
                    <div class="flex">
                      <LucideStar
                        v-for="i in 5"
                        :key="i"
                        class="size-4"
                        :class="i <= (agent.csat_score || 0) ? 'text-yellow-400 fill-current' : 'text-gray-300'"
                      />
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getSLAComplianceClass(agent.sla_compliance)"
                  >
                  {{ displayValue(agent.sla_compliance, 0) }}%
                </span>
              </td>
              </tr>
            </template>
            <tr v-else>
              <td class="px-6 py-8 text-center text-sm text-gray-500" colspan="5">
                No team performance data for the selected filters.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { createResource, AxisChart, DonutChart } from "frappe-ui";
import { computed, h, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import UserAvatar from "@/components/UserAvatar.vue";

const { isManager } = useAuthStore();

const props = defineProps<{
  filters: any;
}>();

const performanceData = createResource({
  url: "helpdesk.api.dashboard.get_performance_overview",
  params: {},
  auto: false,
});

const agentPerformance = createResource({
  url: "helpdesk.api.dashboard.get_agent_performance_chart",
  params: {},
  auto: false,
});

const ticketVelocity = createResource({
  url: "helpdesk.api.dashboard.get_ticket_velocity_chart",
  params: {},
  auto: false,
});

const teamPerformance = createResource({
  url: "helpdesk.api.dashboard.get_team_performance",
  params: {},
  auto: false,
});

const resolvedFilters = computed(() => {
  const payload: Record<string, any> = {};
  const source = props.filters || {};

  if (source.period) {
    const [from, to] = source.period.split(",");
    if (from) payload.from_date = from;
    if (to) payload.to_date = to;
  }

  if (source.agent) {
    payload.agent = source.agent;
  }

  if (source.team) {
    payload.team = source.team;
  }

  return payload;
});

const loadAnalytics = async (filters: Record<string, any>) => {
  const params = { filters };

  performanceData.update({ params });
  agentPerformance.update({ params });
  ticketVelocity.update({ params });

  const requests: Promise<unknown>[] = [
    performanceData.reload(),
    agentPerformance.reload(),
    ticketVelocity.reload(),
  ];

  if (isManager) {
    teamPerformance.update({ params });
    requests.push(teamPerformance.reload());
  }

  await Promise.allSettled(requests);
};

watch(
  resolvedFilters,
  (filters) => {
    loadAnalytics(filters);
  },
  { immediate: true, deep: true }
);

const hasTeamData = computed(() =>
  Array.isArray(teamPerformance.data) && teamPerformance.data.length > 0
);

const displayValue = (value: number | null | undefined, fallback = "--") => {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return fallback;
  }
  return value;
};

const getChartType = (chart: any) => {
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

  chart.colors = colors;
  
  if (chart.type === "axis") {
    return h(AxisChart, { config: chart });
  }
  if (chart.type === "pie") {
    return h(DonutChart, { config: chart });
  }
  return h(AxisChart, { config: chart });
};

const getPerformanceClass = (trend: number) => {
  if (trend > 0) return "text-green-600";
  if (trend < 0) return "text-red-600";
  return "text-gray-600";
};

const formatTrend = (trend: number) => {
  if (!trend) return "No change";
  const prefix = trend > 0 ? "+" : "";
  return `${prefix}${trend.toFixed(1)}%`;
};

const getSLAComplianceClass = (compliance: number) => {
  if (compliance >= 90) return "bg-green-100 text-green-800";
  if (compliance >= 70) return "bg-yellow-100 text-yellow-800";
  return "bg-red-100 text-red-800";
};
</script>
