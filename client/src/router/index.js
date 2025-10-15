import DutyScheduleView from '@/views/DutyScheduleView.vue'
import RepairRequestsView from '@/views/RepairRequestsView.vue'
import RoomsView from '@/views/RoomsView.vue'
import StaffView from '@/views/StaffView.vue'
import StudentsView from '@/views/StudentsView.vue'
import LoginView from '@/views/LoginView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "StudentsView",
      component: StudentsView
    },
    {
      path: "/rooms",
      name: "RoomsView",
      component: RoomsView
    },
    {
      path: "/dutySchedule",
      name: "DutyScheduleView",
      component: DutyScheduleView
    },
    {
      path: "/staff",
      name: "StaffView",
      component: StaffView
    },
    {
      path: "/repairRequests",
      name: "RepairRequestsView",
      component: RepairRequestsView
    },
    {
      path: "/login",
      name: "LoginView",
      component: LoginView
    },
  ]
})

export default router
