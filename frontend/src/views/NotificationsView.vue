<template>
  <section>
    <PageHeader eyebrow="通知" title="紧急通知" description="发布面向家属、员工或全体人员的重要信息。" />

    <article class="panel">
      <h3>发布通知</h3>
      <NotificationForm :model="form" @submit="saveNotification" />
      <p v-if="message" class="message">{{ message }}</p>
    </article>

    <article class="panel">
      <h3>通知列表</h3>
      <div class="filter-bar">
        <label>
          级别
          <select v-model="filterLevel" @change="loadNotifications">
            <option value="">全部级别</option>
            <option value="critical">紧急</option>
            <option value="warning">重要</option>
            <option value="info">普通</option>
          </select>
        </label>
        <label>
          受众
          <select v-model="filterTarget" @change="loadNotifications">
            <option value="">全部受众</option>
            <option value="all">全部</option>
            <option value="families">家属</option>
            <option value="staff">员工</option>
          </select>
        </label>
      </div>
      <EmptyState v-if="notifications.length === 0 && !isFiltering" />
      <div v-else-if="notifications.length === 0 && isFiltering" class="empty-state">
        <strong>未找到匹配的通知</strong>
        <span>当前筛选条件下没有匹配的通知，请调整筛选条件后重试。</span>
      </div>
      <div v-else class="notice-grid">
        <div v-for="item in notifications" :key="item.id" :class="['notice-card', { pinned: item.level === 'critical' }]">
          <div class="notice-title">
            <div class="title-left">
              <span v-if="item.level === 'critical'" class="pin-badge">置顶</span>
              <strong>{{ item.title }}</strong>
            </div>
            <span :class="['badge', item.level]">{{ levelText[item.level] }}</span>
          </div>
          <p>{{ item.content }}</p>
          <footer>
            <span>{{ targetText[item.target_group] }}</span>
            <span>{{ item.is_active ? '有效' : '已停用' }}</span>
            <span>{{ formatTime(item.published_at) }}</span>
          </footer>
        </div>
      </div>
    </article>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import EmptyState from '../components/EmptyState.vue'
import NotificationForm from '../components/NotificationForm.vue'
import PageHeader from '../components/PageHeader.vue'
import { notificationsApi } from '../services/notifications'

const notifications = ref([])
const message = ref('')
const filterLevel = ref('')
const filterTarget = ref('')
const levelText = { info: '普通', warning: '重要', critical: '紧急' }
const targetText = { all: '全部', families: '家属', staff: '员工' }
const initialForm = {
  title: '',
  content: '',
  level: 'warning',
  target_group: 'families',
  is_active: true
}
const form = reactive({ ...initialForm })
const isFiltering = computed(() => !!filterLevel.value || !!filterTarget.value)

onMounted(loadNotifications)

async function loadNotifications() {
  const params = {}
  if (filterLevel.value) params.level = filterLevel.value
  if (filterTarget.value) params.target_group = filterTarget.value
  notifications.value = (await notificationsApi.list(params)).results
}

async function saveNotification() {
  await notificationsApi.create(form)
  Object.assign(form, initialForm)
  message.value = '通知已发布'
  await loadNotifications()
}

function formatTime(value) {
  return value ? new Date(value).toLocaleString('zh-CN') : ''
}
</script>
