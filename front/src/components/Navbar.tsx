type NavbarProps = {
    onLogout: () => void
}

function Navbar({ onLogout }: NavbarProps) {
    return (
        <div
            style={{ backgroundColor: 'var(--surface)', borderBottom: '1px solid var(--border)' }}
            className="flex items-center justify-between px-8 py-4"
        >
            <div className="flex items-center gap-2">
                <span
                    style={{ color: 'var(--primary)' }}
                    className="text-2xl font-bold tracking-tight"
                >
                    ✂ Shorty
                </span>
            </div>

            <button
                onClick={onLogout}
                style={{ color: 'var(--muted)' }}
                className="text-sm hover:text-white transition"
            >
                Sair
            </button>
        </div>
    )
}

export default Navbar