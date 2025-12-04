import { useEffect, useState } from 'react'
import { generateContent, listItems, getItem, publishVersion, getVersionHtmlUrl, getVersionPdfUrl, getItemExportUrl, importContent } from './api'

function GenerateForm({ onGenerated }) {
  const [title, setTitle] = useState('')
  const [topic, setTopic] = useState('')
  const [readingLevel, setReadingLevel] = useState('Grade 5')
  const [grade, setGrade] = useState('')
  const [genre, setGenre] = useState('')
  const [loading, setLoading] = useState(false)

  async function onSubmit(e) {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await generateContent({ title, topic, reading_level: readingLevel, grade: grade || undefined, genre: genre || undefined })
      onGenerated(res)
      setTitle('')
      setTopic('')
      setGrade('')
      setGenre('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={onSubmit} style={{ display: 'grid', gap: 8, maxWidth: 520 }}>
      <h2>Generate Content</h2>
      <input placeholder="Title (optional; uses Topic if blank)" value={title} onChange={e => setTitle(e.target.value)} />
      <input placeholder="Topic" value={topic} onChange={e => setTopic(e.target.value)} required />
      <input placeholder="Reading level (e.g., Grade 5)" value={readingLevel} onChange={e => setReadingLevel(e.target.value)} required />
      <input placeholder="Grade (optional)" value={grade} onChange={e => setGrade(e.target.value)} />
      <input placeholder="Genre (optional)" value={genre} onChange={e => setGenre(e.target.value)} />
      <button disabled={loading}>{loading ? 'Generating…' : 'Generate'}</button>
    </form>
  )
}

function ItemList({ selectedId, onSelect, refreshKey }) {
  const [items, setItems] = useState([])
  useEffect(() => {
    listItems().then(setItems).catch(console.error)
  }, [refreshKey])

  return (
    <div>
      <h2>Content Items</h2>
      <ul>
        {items.map(i => (
          <li key={i.id}>
            <button onClick={() => onSelect(i.id)} style={{ fontWeight: i.id === selectedId ? 'bold' : 'normal' }}>
              {i.title} {i.latest_version ? `(v${i.latest_version.version} ${i.latest_version.status})` : ''}
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

function ItemDetail({ itemId, onPublish }) {
  const [item, setItem] = useState(null)
  useEffect(() => {
    if (!itemId) return
    getItem(itemId).then(setItem).catch(console.error)
  }, [itemId])

  if (!itemId) return <div />
  if (!item) return <div>Loading…</div>
  return (
    <div>
      <h2>{item.title}</h2>
      <div style={{ marginBottom: 12 }}>
        <a href={getItemExportUrl(item.id)} target="_blank" rel="noreferrer">Export Item (JSON)</a>
        <span> | </span>
        <label style={{ cursor: 'pointer' }}>
          Import JSON
          <input type="file" accept="application/json" style={{ display: 'none' }} onChange={async e => {
            const file = e.target.files?.[0]
            if (!file) return
            const text = await file.text()
            const json = JSON.parse(text)
            await importContent(json)
            onPublish()
            e.target.value = ''
          }} />
        </label>
      </div>
      <table>
        <thead>
          <tr><th>Version</th><th>Status</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {item.versions.map(v => (
            <tr key={v.id}>
              <td>v{v.version}</td>
              <td>{v.status}</td>
              <td>
                <a href={getVersionHtmlUrl(item.id, v.id)} target="_blank" rel="noreferrer">View HTML</a>
                {' | '}
                <a href={getVersionPdfUrl(item.id, v.id)} target="_blank" rel="noreferrer">Download PDF</a>
                {' | '}
                {v.status !== 'published' && (
                  <button onClick={async () => { await publishVersion(item.id, v.id); onPublish(); }}>Publish</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function App() {
  const [selectedId, setSelectedId] = useState(null)
  const [refreshKey, setRefreshKey] = useState(0)

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, padding: 24 }}>
      <GenerateForm onGenerated={() => setRefreshKey(x => x + 1)} />
      <ItemList selectedId={selectedId} onSelect={setSelectedId} refreshKey={refreshKey} />
      <div style={{ gridColumn: '1 / span 2' }}>
        <ItemDetail itemId={selectedId} onPublish={() => setRefreshKey(x => x + 1)} />
      </div>
    </div>
  )
}
