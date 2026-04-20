import { useState } from "react"
import type { Url } from '../types/Url'

type UrlCardProps = {
    url: Url
    onDelete: (shortKey: string) => void
    onUpdate: (shortKey: string, newUrl: string, isActive: boolean) => Promise<void>
}

function UrlCard({ url, onDelete, onUpdate }: UrlCardProps) {
    const [editing, setEditing] = useState(false)
    const [editingActive, setEditingActive] = useState(url.is_active)
    const [editingUrl, setEditingUrl] = useState(url.original_url)
    const [copied, setCopied] = useState(false)

    function handleCopy() {
        navigator.clipboard.writeText(
            `${import.meta.env.VITE_API_URL}/${url.short_key}`
        )
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    async function handleSave() {
        await onUpdate(url.short_key, editingUrl, editingActive)
        setEditing(false)
    }

    return (
        <div
            className="rounded-xl p-4 flex flex-col gap-3"
            style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)' }}
        >
            <div>
                <p className="text-xs uppercase mb-1" style={{ color: 'var(--muted)' }}>
                    URL Original
                </p>

                {editing ? (
                    <input
                        value={editingUrl}
                        onChange={(e) => setEditingUrl(e.target.value)}
                        className="w-full px-2 py-1 rounded text-sm"
                    />
                ) : (
                    <p className="text-sm truncate">{url.original_url}</p>
                )}
            </div>

            <div className="flex items-center justify-between">
                <div>
                    <p className="text-xs uppercase mb-1">Link Curto</p>
                    <a
                        href={`${import.meta.env.VITE_API_URL}/${url.short_key}`}
                        target="_blank"
                        className="text-sm hover:underline"
                    >
                        {url.short_key}
                    </a>
                </div>

                <div>
                    <p className="text-xs uppercase mb-1">Cliques</p>
                    <p className="text-sm text-center">{url.clicks}</p>
                </div>

                <div>
                    <p className="text-xs uppercase mb-1">Ativo</p>
                    <input
                        type="checkbox"
                        checked={editingActive}
                        onChange={(e) => setEditingActive(e.target.checked)}
                    />
                </div>
            </div>

            <div className="flex gap-2 flex-wrap">
                {editing ? (
                    <>
                        <button onClick={handleSave}>Salvar</button>
                        <button onClick={() => setEditing(false)}>Cancelar</button>
                    </>
                ) : (
                    <>
                        <button onClick={handleCopy}>
                            {copied ? 'Copiado!' : 'Copiar'}
                        </button>

                        <button
                            onClick={() => {
                                setEditing(true)
                                setEditingUrl(url.original_url)
                                setEditingActive(url.is_active)
                            }}
                        >
                            Editar
                        </button>

                        <button onClick={() => onDelete(url.short_key)}>
                            Deletar
                        </button>
                    </>
                )}
            </div>
        </div>
    )
}

export default UrlCard