import { useState } from 'react'
import type { Url } from '../types/Url.js'


type UrlRowProps = {
    url: Url
    index: number
    onDelete: (shortKey: string) => void
    onUpdate: (shortKey: string, newUrl: string, isActive: boolean) => Promise<void>
}

function UrlRow({ url, index, onDelete, onUpdate }: UrlRowProps) {
    const [editing, setEditing] = useState(false)
    const [editingActive, setEditingActive] = useState(url.is_active)
    const [editingUrl, setEditingUrl] = useState(url.original_url)
    const [copied, setCopied] = useState(false)

    function handleCopy() {
        navigator.clipboard.writeText(`${import.meta.env.VITE_API_URL}/${url.short_key}`)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    async function handleSave() {
        await onUpdate(url.short_key, editingUrl, editingActive)
        setEditing(false)
    }

    return (
        <tr style={{ backgroundColor: index % 2 === 0 ? 'var(--surface)' : 'var(--bg)' }}>
            {/* ... o resto do seu código permanece igual ... */}
            <td className="px-4 py-3 max-w-xs truncate" style={{ color: 'var(--text)' }}>
                {editing ? (
                    <input
                        value={editingUrl}
                        onChange={(e) => setEditingUrl(e.target.value)}
                        style={{
                            backgroundColor: 'var(--bg)',
                            border: '1px solid var(--border)',
                            color: 'var(--text)',
                        }}
                        className="w-full px-2 py-1 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                ) : (
                    url.original_url
                )}
            </td>
            <td className="px-4 py-3">
                <a
                    href={`${import.meta.env.VITE_API_URL}/${url.short_key}`}
                    target="_blank"
                    rel="noreferrer" // Adicionei isso por segurança
                    style={{ color: 'var(--primary)' }}
                    className="hover:underline"
                >
                    {url.short_key}
                </a>
            </td>
            <td className="px-4 py-3 text-center" style={{ color: 'var(--text)' }}>{url.clicks}</td>
            <td className="px-4 py-3 text-center">
                {editing ? (
                    <label className="flex items-center gap-2 text-sm justify-center cursor-pointer" style={{ color: 'var(--text)' }}>
                        <input
                            type="checkbox"
                            checked={editingActive}
                            onChange={(e) => setEditingActive(e.target.checked)}
                        />
                        {editingActive ? 'Ativo' : 'Inativo'}
                    </label>
                ) : (
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${url.is_active ? 'bg-blue-900 text-blue-400' : 'bg-red-900 text-red-400'}`}>
                        {url.is_active ? 'Sim' : 'Não'}
                    </span>
                )}
            </td>
            <td className="px-4 py-3 text-center">
                <div className="flex gap-2 justify-center">
                    {editing ? (
                        <>
                            <button
                                onClick={handleSave}
                                className="px-3 py-1 bg-green-700 hover:bg-green-600 rounded text-xs transition text-white"
                            >
                                Salvar
                            </button>
                            <button
                                onClick={() => setEditing(false)}
                                className="px-3 py-1 rounded text-xs transition text-white"
                                style={{ backgroundColor: 'var(--border)' }}
                            >
                                Cancelar
                            </button>
                        </>
                    ) : (
                        <>
                            <button
                                onClick={handleCopy}
                                className="px-3 py-1 rounded text-xs transition text-white"
                                style={{ backgroundColor: copied ? '#16a34a' : '#1e40af' }}
                            >
                                {copied ? 'Copiado!' : 'Copiar'}
                            </button>
                            <button
                                onClick={() => { setEditing(true); setEditingUrl(url.original_url); setEditingActive(url.is_active) }}
                                style={{ backgroundColor: 'var(--primary)' }}
                                className="px-3 py-1 rounded text-xs transition text-white hover:opacity-90"
                            >
                                Editar
                            </button>
                            <button
                                onClick={() => onDelete(url.short_key)}
                                className="px-3 py-1 bg-red-800 hover:bg-red-700 rounded text-xs transition text-white"
                            >
                                Deletar
                            </button>
                        </>
                    )}
                </div>
            </td>
        </tr>
    )
}

export default UrlRow