import LucideBookOpen from "~icons/lucide/book-open";
import LucideCloudLightning from "~icons/lucide/cloud-lightning";
import LucideContact2 from "~icons/lucide/contact-2";
import LucideTicket from "~icons/lucide/ticket";
import LucideGraduationCap from "~icons/lucide/graduation-cap";
import LucideUserCog from "~icons/lucide/user-cog";
import { OrganizationsIcon } from "../icons";
import PhoneIcon from "../icons/PhoneIcon.vue";

export const agentPortalSidebarOptions = [
  {
    label: "Tickets",
    icon: LucideTicket,
    to: "TicketsAgent",
  },
  {
    label: "Knowledge Base",
    icon: LucideBookOpen,
    to: "AgentKnowledgeBase",
  },
  {
    label: "Canned responses",
    icon: LucideCloudLightning,
    to: "CannedResponses",
  },
  {
    label: "Customers",
    icon: OrganizationsIcon,
    to: "CustomerList",
  },
  {
    label: "Contacts",
    icon: LucideContact2,
    to: "ContactList",
  },
  {
    label: "Call Logs",
    icon: PhoneIcon,
    to: "CallLogs",
  },
  {
    label: "Admin Tutorial",
    icon: LucideUserCog,
    to: "AdminTutorial",
  },
];

export const customerPortalSidebarOptions = [
  {
    label: "Tickets",
    icon: LucideTicket,
    to: "TicketsCustomer",
  },
  {
    label: "Knowledge Base",
    icon: LucideBookOpen,
    to: "CustomerKnowledgeBase",
  },
  {
    label: "User Tutorial",
    icon: LucideGraduationCap,
    to: "UserTutorial",
  },
];
