import { useState } from 'react'

type UrlFormProps = {
    onCreate: (Url: string) => void
}

function UrlForm({ onCreate }: UrlFormProps) {
    const [newUrl, setNewUrl] = useState<string>('')

    async function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
        e.preventDefault()
        await onCreate(newUrl)
        setNewUrl('')
    }

    return (
        <form onSubmit={handleSubmit} className="flex gap-2 mb-10">
            <input
                type="url"
                placeholder="Cole sua URL aqui"
                value={newUrl}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewUrl(e.target.value)}
                style={{
                    backgroundColor: 'var(--surface)',
                    border: '1px solid var(--border)',
                    color: 'var(--text)',
                }}
                className="flex-1 px-4 py-2 rounded-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
                type="submit"
                style={{ backgroundColor: 'var(--primary)' }}
                className="px-6 py-2 rounded-lg font-semibold text-white hover:opacity-90 transition"
            >
                Encurtar
            </button>
        </form>
    )
}

export default UrlForm