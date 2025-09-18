<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" class="-ml-0.5" />
      </template>
    </LayoutHeader>
    <div class="px-4 sm:px-6 lg:px-8 py-8 max-w-7xl mx-auto">
      <!-- Hero Header Section -->
      <div class="text-center mb-12">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full mb-6 shadow-lg">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
          </svg>
        </div>
        <h1 class="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-indigo-600 bg-clip-text text-transparent mb-4">
          Admin Management Center
        </h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
          Master your helpdesk system with comprehensive administrative tools and best practices
        </p>
        <div class="flex flex-wrap justify-center gap-3 mt-6">
          <span class="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
            </svg>
            User Management
          </span>
          <span class="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
            </svg>
            Email Integration
          </span>
          <span class="inline-flex items-center px-4 py-2 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
            </svg>
            Automation
          </span>
        </div>
      </div>

      <!-- Role Selection Section -->
      <div class="mb-12">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">Choose Your Role</h2>
          <p class="text-gray-600">Select your role to see customized administrative guidance</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Agent Guide -->
          <div 
            class="group relative bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-500 cursor-pointer border-2 border-transparent hover:border-blue-200 transform hover:-translate-y-2"
            :class="{ 'border-blue-400 shadow-2xl scale-105': showAgentGuide }"
            @click="toggleAgentGuide"
          >
            <div class="absolute inset-0 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="relative z-10">
              <div class="flex items-center justify-between mb-6">
                <div class="flex items-center">
                  <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                  </div>
                  <div class="ml-4">
                    <h3 class="text-2xl font-bold text-gray-900">Agent Guide</h3>
                    <p class="text-blue-600 font-medium">Support Team Operations</p>
                  </div>
                </div>
                <div class="transform transition-transform duration-300" :class="{ 'rotate-180': showAgentGuide }">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </div>
              </div>
              <p class="text-gray-600 mb-4 leading-relaxed">
                Learn day-to-day operations, ticket handling, and team collaboration tools for support agents.
              </p>
              <div class="flex flex-wrap gap-2">
                <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">Ticket Management</span>
                <span class="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium">Customer Communication</span>
                <span class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">Team Workflow</span>
              </div>
            </div>
          </div>

          <!-- Management Guide -->
          <div 
            class="group relative bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-500 cursor-pointer border-2 border-transparent hover:border-green-200 transform hover:-translate-y-2"
            :class="{ 'border-green-400 shadow-2xl scale-105': showManagementGuide }"
            @click="toggleManagementGuide"
          >
            <div class="absolute inset-0 bg-gradient-to-br from-green-50 to-emerald-50 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="relative z-10">
              <div class="flex items-center justify-between mb-6">
                <div class="flex items-center">
                  <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                    </svg>
                  </div>
                  <div class="ml-4">
                    <h3 class="text-2xl font-bold text-gray-900">Management Guide</h3>
                    <p class="text-green-600 font-medium">Strategic Administration</p>
                  </div>
                </div>
                <div class="transform transition-transform duration-300" :class="{ 'rotate-180': showManagementGuide }">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </div>
              </div>
              <p class="text-gray-600 mb-4 leading-relaxed">
                Master system configuration, user management, analytics, and strategic helpdesk optimization.
              </p>
              <div class="flex flex-wrap gap-2">
                <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">System Configuration</span>
                <span class="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-sm font-medium">User Management</span>
                <span class="px-3 py-1 bg-teal-100 text-teal-800 rounded-full text-sm font-medium">Analytics & Reports</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Agent Guide Content -->
      <Transition 
        enter-active-class="transition-all duration-500 ease-out"
        enter-from-class="opacity-0 -translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-300 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-4"
      >
        <div v-if="showAgentGuide" class="mb-12">
          <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-3xl p-8 border border-blue-100 shadow-lg">
            <div class="flex items-center mb-8">
              <div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-2xl font-bold text-gray-900">Agent Operations Guide</h3>
                <p class="text-blue-600 font-medium">Day-to-day support operations</p>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
                <div class="flex items-center mb-4">
                  <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"></path>
                    </svg>
                  </div>
                  <h4 class="text-lg font-semibold text-gray-900 ml-3">Ticket Management</h4>
                </div>
                <ul class="space-y-2 text-gray-600">
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                    Create and assign tickets
                  </li>
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                    Update ticket status and priority
                  </li>
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                    Use canned responses effectively
                  </li>
                </ul>
              </div>
              
              <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
                <div class="flex items-center mb-4">
                  <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                    <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                    </svg>
                  </div>
                  <h4 class="text-lg font-semibold text-gray-900 ml-3">Customer Communication</h4>
                </div>
                <ul class="space-y-2 text-gray-600">
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-indigo-400 rounded-full mr-2"></span>
                    Professional email responses
                  </li>
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-indigo-400 rounded-full mr-2"></span>
                    Handle escalations properly
                  </li>
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-indigo-400 rounded-full mr-2"></span>
                    Maintain customer satisfaction
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Management Guide Content -->
      <Transition 
        enter-active-class="transition-all duration-500 ease-out"
        enter-from-class="opacity-0 -translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-300 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-4"
      >
        <div v-if="showManagementGuide" class="mb-12">
          <div class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-3xl p-8 border border-green-100 shadow-lg">
            <div class="flex items-center mb-8">
              <div class="w-14 h-14 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center shadow-lg">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-2xl font-bold text-gray-900">Management Dashboard</h3>
                <p class="text-green-600 font-medium">Strategic system administration</p>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
                <div class="flex items-center mb-4">
                  <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                    <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                    </svg>
                  </div>
                  <h4 class="text-lg font-semibold text-gray-900 ml-3">User Management</h4>
                </div>
                <ul class="space-y-2 text-gray-600">
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                    Create agent accounts
                  </li>
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                    Set permissions and roles
                  </li>
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                    Team assignments
                  </li>
                </ul>
              </div>
              
              <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
                <div class="flex items-center mb-4">
                  <div class="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
                    <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                  </div>
                  <h4 class="text-lg font-semibold text-gray-900 ml-3">System Configuration</h4>
                </div>
                <ul class="space-y-2 text-gray-600">
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-emerald-400 rounded-full mr-2"></span>
                    Email settings
                  </li>
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-emerald-400 rounded-full mr-2"></span>
                    Automation rules
                  </li>
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-emerald-400 rounded-full mr-2"></span>
                    Knowledge base setup
                  </li>
                </ul>
              </div>
              
              <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
                <div class="flex items-center mb-4">
                  <div class="w-10 h-10 bg-teal-100 rounded-lg flex items-center justify-center">
                    <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                    </svg>
                  </div>
                  <h4 class="text-lg font-semibold text-gray-900 ml-3">Analytics & Reports</h4>
                </div>
                <ul class="space-y-2 text-gray-600">
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-teal-400 rounded-full mr-2"></span>
                    Performance metrics
                  </li>
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-teal-400 rounded-full mr-2"></span>
                    Team productivity
                  </li>
                  <li class="flex items-center">
                    <span class="w-2 h-2 bg-teal-400 rounded-full mr-2"></span>
                    Customer satisfaction
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Quick Start Section -->
      <div class="relative mb-12">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 transform -skew-y-1 shadow-xl rounded-3xl"></div>
        <div class="relative bg-white rounded-2xl p-8 m-4 shadow-lg border border-gray-100">
          <div class="flex items-center mb-6">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-xl flex items-center justify-center shadow-md">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h2 class="text-2xl font-bold text-gray-900">Quick Start Guide</h2>
              <p class="text-gray-600">Get your helpdesk system running in 5 easy steps</p>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="flex items-start space-x-3">
              <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <span class="text-blue-600 font-semibold text-sm">1</span>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">Email Setup</h3>
                <p class="text-sm text-gray-600">Configure email accounts for ticket management</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <div class="flex-shrink-0 w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <span class="text-green-600 font-semibold text-sm">2</span>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">User Management</h3>
                <p class="text-sm text-gray-600">Set up agent accounts and teams</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <div class="flex-shrink-0 w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                <span class="text-purple-600 font-semibold text-sm">3</span>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">Ticket Config</h3>
                <p class="text-sm text-gray-600">Create ticket types and priorities</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <div class="flex-shrink-0 w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
                <span class="text-orange-600 font-semibold text-sm">4</span>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">Automation</h3>
                <p class="text-sm text-gray-600">Configure automation rules</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <div class="flex-shrink-0 w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center">
                <span class="text-indigo-600 font-semibold text-sm">5</span>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">Knowledge Base</h3>
                <p class="text-sm text-gray-600">Set up knowledge base categories</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tutorial Sections -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <!-- User Management -->
        <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-green-200 hover:-translate-y-1">
          <div class="flex items-center mb-6">
            <div class="w-14 h-14 bg-gradient-to-br from-green-400 to-green-600 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-xl font-bold text-gray-900">User Management</h3>
              <p class="text-green-600 font-medium">Teams & Permissions</p>
            </div>
          </div>
          <p class="text-gray-600 mb-6 leading-relaxed">
            Manage agents, teams, and customer access with advanced role-based controls.
          </p>
          <div class="space-y-3">
            <div class="flex items-center">
              <div class="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Create and manage agent accounts</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Set up teams and assign agents</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Configure role-based permissions</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Manage customer portal access</span>
            </div>
          </div>
        </div>

        <!-- Email Configuration -->
        <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-blue-200 hover:-translate-y-1">
          <div class="flex items-center mb-6">
            <div class="w-14 h-14 bg-gradient-to-br from-blue-400 to-blue-600 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-xl font-bold text-gray-900">Email Integration</h3>
              <p class="text-blue-600 font-medium">Automated Workflow</p>
            </div>
          </div>
          <p class="text-gray-600 mb-6 leading-relaxed">
            Set up seamless email integration for automated ticket creation and smart responses.
          </p>
          <div class="space-y-3">
            <div class="flex items-center">
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Configure incoming email accounts</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Set up outgoing email settings</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Configure email templates</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Set up smart notifications</span>
            </div>
          </div>
        </div>

        <!-- Ticket Configuration -->
        <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-purple-200 hover:-translate-y-1">
          <div class="flex items-center mb-6">
            <div class="w-14 h-14 bg-gradient-to-br from-purple-400 to-purple-600 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-xl font-bold text-gray-900">Ticket System</h3>
              <p class="text-purple-600 font-medium">Advanced Configuration</p>
            </div>
          </div>
          <p class="text-gray-600 mb-6 leading-relaxed">
            Configure comprehensive ticket management with custom types, priorities, and SLA policies.
          </p>
          <div class="space-y-3">
            <div class="flex items-center">
              <div class="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Create custom ticket types</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Set up priority levels</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Configure SLA policies</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Create ticket templates</span>
            </div>
          </div>
        </div>

        <!-- Automation & Reports -->
        <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-orange-200 hover:-translate-y-1">
          <div class="flex items-center mb-6">
            <div class="w-14 h-14 bg-gradient-to-br from-orange-400 to-orange-600 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-xl font-bold text-gray-900">Smart Automation</h3>
              <p class="text-orange-600 font-medium">Analytics & Reports</p>
            </div>
          </div>
          <p class="text-gray-600 mb-6 leading-relaxed">
            Implement intelligent automation rules and monitor performance with detailed analytics.
          </p>
          <div class="space-y-3">
            <div class="flex items-center">
              <div class="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Create assignment rules</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Set up escalation rules</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Configure smart notifications</span>
            </div>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
              <span class="text-gray-700">Monitor advanced analytics</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Best Practices Section -->
      <div class="bg-gradient-to-r from-gray-50 to-blue-50 rounded-3xl p-8 mb-12 border border-gray-100">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-2xl mb-4 shadow-lg">
            <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 mb-2">Expert Best Practices</h2>
          <p class="text-gray-600">Pro tips from helpdesk administrators worldwide</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
            <div class="flex items-center mb-4">
              <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
              <h3 class="font-semibold text-gray-900 ml-3">Security & Access</h3>
            </div>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex items-center">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Regular permission audits
              </li>
              <li class="flex items-center">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Two-factor authentication
              </li>
              <li class="flex items-center">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Access log monitoring
              </li>
            </ul>
          </div>
          
          <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
            <div class="flex items-center mb-4">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
              </div>
              <h3 class="font-semibold text-gray-900 ml-3">Performance</h3>
            </div>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex items-center">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Monitor response times
              </li>
              <li class="flex items-center">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Archive old tickets
              </li>
              <li class="flex items-center">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Update knowledge base
              </li>
            </ul>
          </div>
          
          <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300 md:col-span-2 lg:col-span-1">
            <div class="flex items-center mb-4">
              <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <h3 class="font-semibold text-gray-900 ml-3">Quality</h3>
            </div>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex items-center">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Regular team training
              </li>
              <li class="flex items-center">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Customer feedback tracking
              </li>
              <li class="flex items-center">
                <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Process optimization
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Call to Action Section -->
      <div class="relative overflow-hidden bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 rounded-3xl p-8 text-white shadow-2xl">
        <div class="absolute inset-0 bg-black opacity-10"></div>
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-white opacity-10 rounded-full"></div>
        <div class="absolute -bottom-10 -left-10 w-32 h-32 bg-white opacity-10 rounded-full"></div>
        <div class="relative z-10 text-center">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-white bg-opacity-20 rounded-2xl mb-6">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <h2 class="text-3xl font-bold mb-4">Ready to Transform Your Helpdesk?</h2>
          <p class="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
            Take control of your support operations with advanced administrative tools and proven best practices.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/helpdesk" class="inline-flex items-center px-8 py-4 bg-white text-blue-600 rounded-xl font-semibold hover:bg-gray-100 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
              Open Admin Workspace
            </a>
            <router-link to="/dashboard" class="inline-flex items-center px-8 py-4 bg-white bg-opacity-20 text-white rounded-xl font-semibold hover:bg-opacity-30 transition-all duration-300 backdrop-blur-sm border border-white border-opacity-30 hover:border-opacity-50 transform hover:-translate-y-0.5">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
              View Analytics Dashboard
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { Breadcrumbs } from "frappe-ui";
import LayoutHeader from "@/components/LayoutHeader.vue";

const showAgentGuide = ref(false);
const showManagementGuide = ref(false);

const toggleAgentGuide = () => {
  showAgentGuide.value = !showAgentGuide.value;
  if (showAgentGuide.value) {
    showManagementGuide.value = false;
  }
};

const toggleManagementGuide = () => {
  showManagementGuide.value = !showManagementGuide.value;
  if (showManagementGuide.value) {
    showAgentGuide.value = false;
  }
};

const breadcrumbs = computed(() => [
  {
    label: "Tutorials",
    route: { name: "AdminTutorial" },
  },
  {
    label: "Admin Management",
    route: { name: "AdminTutorial" },
  },
]);
</script>