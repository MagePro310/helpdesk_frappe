<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" class="-ml-0.5" />
      </template>
    </LayoutHeader>
    <div class="px-4 sm:px-6 lg:px-8 py-8 max-w-7xl mx-auto">
      <!-- Hero Header Section -->
      <div class="text-center mb-12">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-green-500 to-blue-600 rounded-full mb-6 shadow-lg">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
          </svg>
        </div>
        <h1 class="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-gray-900 via-green-800 to-blue-600 bg-clip-text text-transparent mb-4">
          User Guide Center
        </h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
          Everything you need to know about using the helpdesk system effectively, whether you're an agent or customer
        </p>
        <div class="flex flex-wrap justify-center gap-3 mt-6">
          <span class="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
            </svg>
            Easy to Follow
          </span>
          <span class="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
            </svg>
            Step by Step
          </span>
          <span class="inline-flex items-center px-4 py-2 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
            </svg>
            Best Practices
          </span>
        </div>
      </div>

      <!-- Interactive Role Selection -->
      <div class="mb-12">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">Choose Your Learning Path</h2>
          <p class="text-gray-600">Select your role to see customized guidance and tips</p>
        </div>
        <div :class="isCustomerPortal ? 'flex justify-center' : 'grid grid-cols-1 lg:grid-cols-2 gap-8'">
          <!-- Agent Path -->
          <div 
            v-if="!isCustomerPortal"
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
                    <h3 class="text-2xl font-bold text-gray-900">I'm an Agent</h3>
                    <p class="text-blue-600 font-medium">Support Team Member</p>
                  </div>
                </div>
                <div class="transform transition-transform duration-300" :class="{ 'rotate-180': showAgentGuide }">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </div>
              </div>
              <p class="text-gray-600 mb-4 leading-relaxed">
                Master ticket management, customer communication, and team collaboration tools.
              </p>
              <div class="flex flex-wrap gap-2">
                <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">Ticket Management</span>
                <span class="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium">Customer Service</span>
                <span class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">Team Collaboration</span>
              </div>
            </div>
          </div>

          <!-- Customer Path -->
          <div 
            class="group relative bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-500 cursor-pointer border-2 border-transparent hover:border-green-200 transform hover:-translate-y-2"
            :class="[
              { 'border-green-400 shadow-2xl scale-105': showCustomerGuide },
              isCustomerPortal ? 'max-w-lg w-full' : ''
            ]"
            @click="toggleCustomerGuide"
          >
            <div class="absolute inset-0 bg-gradient-to-br from-green-50 to-emerald-50 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="relative z-10">
              <div class="flex items-center justify-between mb-6">
                <div class="flex items-center">
                  <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V5a2 2 0 012-2h4a2 2 0 012 2v2m-6 4h4"></path>
                    </svg>
                  </div>
                  <div class="ml-4">
                    <h3 class="text-2xl font-bold text-gray-900">I'm a Customer</h3>
                    <p class="text-green-600 font-medium">Seeking Support</p>
                  </div>
                </div>
                <div class="transform transition-transform duration-300" :class="{ 'rotate-180': showCustomerGuide }">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </div>
              </div>
              <p class="text-gray-600 mb-4 leading-relaxed">
                Learn how to create tickets, track progress, and find answers quickly.
              </p>
              <div class="flex flex-wrap gap-2">
                <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">Create Tickets</span>
                <span class="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-sm font-medium">Track Progress</span>
                <span class="px-3 py-1 bg-teal-100 text-teal-800 rounded-full text-sm font-medium">Self-Service</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Guide Content -->
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
                <h3 class="text-2xl font-bold text-gray-900">Agent Mastery Guide</h3>
                <p class="text-blue-600 font-medium">Professional Support Excellence</p>
              </div>
            </div>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <!-- Ticket Management -->
              <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
                <div class="flex items-center mb-4">
                  <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                    <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"></path>
                    </svg>
                  </div>
                  <h4 class="font-bold text-gray-900 ml-3">Ticket Management Pro</h4>
                </div>
                <div class="space-y-3">
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Advanced filtering and search capabilities</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Priority-based response management</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Status tracking and escalation workflows</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Internal notes and team collaboration</span>
                  </div>
                </div>
              </div>

              <!-- Communication Excellence -->
              <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
                <div class="flex items-center mb-4">
                  <div class="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center">
                    <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                    </svg>
                  </div>
                  <h4 class="font-bold text-gray-900 ml-3">Communication Excellence</h4>
                </div>
                <div class="space-y-3">
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-indigo-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Smart canned responses and templates</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-indigo-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Real-time collaboration with @mentions</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-indigo-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Escalation and handoff procedures</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-indigo-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Customer satisfaction tracking</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Agent Best Practices -->
            <div class="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl p-6 text-white">
              <h4 class="font-bold text-xl mb-4 flex items-center">
                <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"></path>
                </svg>
                Pro Agent Tips
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="flex items-center">
                  <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-sm">Respond within SLA timeframes</span>
                </div>
                <div class="flex items-center">
                  <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-sm">Use clear, professional language</span>
                </div>
                <div class="flex items-center">
                  <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-sm">Provide regular progress updates</span>
                </div>
                <div class="flex items-center">
                  <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-sm">Document solutions for knowledge base</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <Transition 
        enter-active-class="transition-all duration-500 ease-out"
        enter-from-class="opacity-0 -translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-300 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-4"
      >
        <div v-if="showCustomerGuide" class="mb-12">
          <div class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-3xl p-8 border border-green-100 shadow-lg">
            <div class="flex items-center mb-8">
              <div class="w-14 h-14 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center shadow-lg">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V5a2 2 0 012-2h4a2 2 0 012 2v2m-6 4h4"></path>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-2xl font-bold text-gray-900">Customer Success Guide</h3>
                <p class="text-green-600 font-medium">Get Help Fast & Effectively</p>
              </div>
            </div>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <!-- Creating Tickets -->
              <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
                <div class="flex items-center mb-4">
                  <div class="w-10 h-10 bg-green-100 rounded-xl flex items-center justify-center">
                    <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                    </svg>
                  </div>
                  <h4 class="font-bold text-gray-900 ml-3">Smart Ticket Creation</h4>
                </div>
                <div class="space-y-3">
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-green-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Click "New Ticket" for immediate assistance</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-green-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Include detailed problem descriptions</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-green-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Select appropriate priority levels</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-green-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Attach screenshots and relevant files</span>
                  </div>
                </div>
              </div>

              <!-- Tracking & Communication -->
              <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
                <div class="flex items-center mb-4">
                  <div class="w-10 h-10 bg-emerald-100 rounded-xl flex items-center justify-center">
                    <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                    </svg>
                  </div>
                  <h4 class="font-bold text-gray-900 ml-3">Progress Tracking</h4>
                </div>
                <div class="space-y-3">
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-emerald-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Monitor real-time status updates</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-emerald-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Receive instant email notifications</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-emerald-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Respond to agent questions quickly</span>
                  </div>
                  <div class="flex items-start">
                    <div class="w-2 h-2 bg-emerald-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span class="text-gray-700">Rate your support experience</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Customer Success Tips -->
            <div class="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl p-6 text-white">
              <h4 class="font-bold text-xl mb-4 flex items-center">
                <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Success Tips
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="flex items-center">
                  <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-sm">Search knowledge base first</span>
                </div>
                <div class="flex items-center">
                  <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-sm">Provide detailed problem descriptions</span>
                </div>
                <div class="flex items-center">
                  <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-sm">Check email regularly for updates</span>
                </div>
                <div class="flex items-center">
                  <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-sm">Rate experience to help us improve</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Knowledge Base Section -->
      <div class="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          Using the Knowledge Base
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="text-center">
            <div class="bg-blue-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <h3 class="font-medium text-gray-900 mb-2">Search Articles</h3>
            <p class="text-sm text-gray-600">Find answers to common questions quickly using our search feature.</p>
          </div>
          <div class="text-center">
            <div class="bg-green-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
              </svg>
            </div>
            <h3 class="font-medium text-gray-900 mb-2">Browse Categories</h3>
            <p class="text-sm text-gray-600">Explore articles organized by topic and product category.</p>
          </div>
          <div class="text-center">
            <div class="bg-purple-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
            </div>
            <h3 class="font-medium text-gray-900 mb-2">Step-by-step Guides</h3>
            <p class="text-sm text-gray-600">Follow detailed tutorials for complex procedures and setup tasks.</p>
          </div>
        </div>
      </div>

      <!-- Quick Action Section -->
      <div class="relative overflow-hidden bg-gradient-to-r from-blue-600 via-green-600 to-teal-600 rounded-3xl p-8 text-white shadow-2xl">
        <div class="absolute inset-0 bg-black opacity-10"></div>
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-white opacity-10 rounded-full"></div>
        <div class="absolute -bottom-10 -left-10 w-32 h-32 bg-white opacity-10 rounded-full"></div>
        <div class="relative z-10 text-center">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-white bg-opacity-20 rounded-2xl mb-6">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <h2 class="text-3xl font-bold mb-4">Ready to Get Started?</h2>
          <p class="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
            Jump right in and start using the helpdesk system with confidence
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link to="/my-tickets/new" class="inline-flex items-center px-8 py-4 bg-white text-blue-600 rounded-xl font-semibold hover:bg-gray-100 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              Create New Ticket
            </router-link>
            <router-link to="/my-tickets" class="inline-flex items-center px-8 py-4 bg-white bg-opacity-20 text-white rounded-xl font-semibold hover:bg-opacity-30 transition-all duration-300 backdrop-blur-sm border border-white border-opacity-30 hover:border-opacity-50 transform hover:-translate-y-0.5">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
              View My Tickets
            </router-link>
            <router-link to="/kb-public" class="inline-flex items-center px-8 py-4 bg-white bg-opacity-20 text-white rounded-xl font-semibold hover:bg-opacity-30 transition-all duration-300 backdrop-blur-sm border border-white border-opacity-30 hover:border-opacity-50 transform hover:-translate-y-0.5">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
              Browse Knowledge Base
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
import { isCustomerPortal } from "@/utils";

const showAgentGuide = ref(false);
const showCustomerGuide = ref(false);

const toggleAgentGuide = () => {
  showAgentGuide.value = !showAgentGuide.value;
  if (showAgentGuide.value) {
    showCustomerGuide.value = false;
  }
};

const toggleCustomerGuide = () => {
  showCustomerGuide.value = !showCustomerGuide.value;
  if (showCustomerGuide.value) {
    showAgentGuide.value = false;
  }
};

const breadcrumbs = computed(() => [
  {
    label: "Tutorials",
    route: { name: "UserTutorial" },
  },
  {
    label: "User Guide",
    route: { name: "UserTutorial" },
  },
]);
</script>