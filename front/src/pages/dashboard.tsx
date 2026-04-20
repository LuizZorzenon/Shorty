import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getUrls, createUrl, deleteUrl, updateUrl } from '../services/api'
import Navbar from '../components/Navbar'
import UrlForm from '../components/Urlform'
import UrlTable from '../components/Urltable'
import type { Url } from '../types/Url'


type UrlTableProps = {
    urls: Url[],
    onDelete: (shortKey: string) => void
    onUpdate: (shortKey: string, newUrl: string, isActive: boolean) => Promise<void>
}

function Dashboard() {
    const [urls, setUrls] = useState<Url[]>([])
    const [error, setError] = useState<string | null>(null)
    const navigate = useNavigate()

    useEffect(() => {
        fetchUrls()
    }, [])

    async function fetchUrls() {
        try {
            const data = await getUrls()
            setUrls(data)
        } catch (err) {
            setError('Erro ao carregar URLs')
        }
    }

    async function handleCreate(newUrl: string): Promise<void> {
        try {
            await createUrl(newUrl)
            fetchUrls()
        } catch (err) {
            setError('Erro ao criar URL')
        }
    }

    async function handleDelete(shortkey: string): Promise<void> {
        try {
            await deleteUrl(shortkey)
            fetchUrls()
        } catch (err) {
            setError('Erro ao deletar URL')
        }
    }
    async function handleUpdate(shortkey: string, newUrl: string, isActive: boolean): Promise<void> {
        try {
            await updateUrl(shortkey, newUrl, isActive)
            fetchUrls()
        } catch (err) {
            const msg = err instanceof Error ? err.message : 'Erro ao atualizar URL'
            setError(msg)
        }
    }

    function handleLogout() {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        navigate('/login')
    }

    return (
        <div className="min-h-screen" style={{ backgroundColor: 'var(--bg)', color: 'var(--text)' }}>
            <Navbar onLogout={handleLogout} />
            <div className="max-w-4xl mx-auto px-4 py-10">
                {error && <p className="mb-4 text-red-400 text-sm">{error}</p>}
                <UrlForm onCreate={handleCreate} />
                <UrlTable urls={urls} onDelete={handleDelete} onUpdate={handleUpdate} />
            </div>
        </div>
    )
}

export default Dashboard