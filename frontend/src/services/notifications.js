import { api } from './api'

export const notificationsApi = {
  list: (params = {}) => {
    const query = new URLSearchParams()
    if (params.level) query.set('level', params.level)
    if (params.target_group) query.set('target_group', params.target_group)
    const qs = query.toString()
    return api.get(`/notifications/${qs ? '?' + qs : ''}`)
  },
  create: (payload) => api.post('/notifications/', payload),
  update: (id, payload) => api.put(`/notifications/${id}/`, payload),
  remove: (id) => api.delete(`/notifications/${id}/`)
}
