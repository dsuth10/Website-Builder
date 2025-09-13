const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8004'

export async function generateContent({ title, topic, reading_level, grade, genre }) {
  const res = await fetch(`${API_BASE}/api/content/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, topic, reading_level, grade, genre }),
  })
  if (!res.ok) throw new Error('Failed to generate content')
  return res.json()
}

export async function listItems() {
  const res = await fetch(`${API_BASE}/api/content`)
  if (!res.ok) throw new Error('Failed to list items')
  return res.json()
}

export async function getItem(itemId) {
  const res = await fetch(`${API_BASE}/api/content/${itemId}`)
  if (!res.ok) throw new Error('Failed to get item')
  return res.json()
}

export async function publishVersion(itemId, versionId) {
  const res = await fetch(`${API_BASE}/api/content/${itemId}/versions/${versionId}/publish`, {
    method: 'POST'
  })
  if (!res.ok) throw new Error('Failed to publish')
  return res.json()
}

export function getVersionHtmlUrl(itemId, versionId) {
  return `${API_BASE}/api/content/${itemId}/versions/${versionId}/html`
}

export function getVersionPdfUrl(itemId, versionId) {
  return `${API_BASE}/api/content/${itemId}/versions/${versionId}/pdf`
}

export function getItemExportUrl(itemId) {
  return `${API_BASE}/api/content/${itemId}/export`
}

export async function importContent(payload) {
  const res = await fetch(`${API_BASE}/api/content/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('Failed to import content')
  return res.json()
}
