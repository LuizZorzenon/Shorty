import UrlRow from './Urlrow.js'
import UrlCard from './Urlcard.js'

type Url = {
    id: number
    original_url: string
    short_key: string
    clicks: number
    is_active: boolean
}

type UrlTableProps = {
    urls: Url[],
    onDelete: (shortKey: string) => void
    onUpdate: (shortKey: string, newUrl: string, isActive: boolean) => Promise<void>
}

function UrlTable({ urls, onDelete, onUpdate }: UrlTableProps) {
    return (
        <>
            {/* Desktop */}
            <div className="hidden md:block rounded-xl overflow-hidden"
                style={{ border: '1px solid var(--border)' }}>
                <table className="w-full text-sm">
                    <thead style={{ backgroundColor: 'var(--surface)', color: 'var(--muted)' }}
                        className="uppercase text-xs">
                        <tr>
                            <th className="px-4 py-3 text-left">URL Original</th>
                            <th className="px-4 py-3 text-left">Link Curto</th>
                            <th className="px-4 py-3 text-center">Cliques</th>
                            <th className="px-4 py-3 text-center">Ativo</th>
                            <th className="px-4 py-3 text-center">Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {urls.map((url, index) => (
                            <UrlRow
                                key={url.short_key}
                                url={url}
                                index={index}
                                onDelete={onDelete}
                                onUpdate={onUpdate}
                            />
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Mobile */}
            <div className="flex flex-col gap-4 md:hidden">
                {urls.map((url) => (
                    <UrlCard
                        key={url.short_key}
                        url={url}
                        onDelete={onDelete}
                        onUpdate={onUpdate}
                    />
                ))}
            </div>
        </>
    )
}

export default UrlTable