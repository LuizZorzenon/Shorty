import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { login } from '../services/api'

function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()

    async function handleSubmit(e: React.SyntheticEvent<HTMLFormElement>): Promise<void> {
        e.preventDefault()
        try {
            const data = await login(email, password)
            localStorage.setItem('access_token', data.access_token)
            localStorage.setItem('refresh_token', data.refresh_token)
            navigate('/dashboard')
        } catch (err) {
            setError('Email ou senha inválidos')
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center px-4"
            style={{ backgroundColor: 'var(--bg)' }}>
            <div className="w-full max-w-md p-8 rounded-2xl"
                style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)' }}>
                <h1 className="text-3xl font-bold mb-1" style={{ color: 'var(--primary)' }}>✂ Shorty</h1>
                <p className="mb-8 text-sm" style={{ color: 'var(--muted)' }}>Encurte seus links com facilidade</p>

                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        style={{
                            backgroundColor: 'var(--bg)',
                            border: '1px solid var(--border)',
                            color: 'var(--text)',
                        }}
                        className="px-4 py-2 rounded-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <input
                        type="password"
                        placeholder="Senha"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{
                            backgroundColor: 'var(--bg)',
                            border: '1px solid var(--border)',
                            color: 'var(--text)',
                        }}
                        className="px-4 py-2 rounded-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    {error && <p className="text-red-400 text-sm">{error}</p>}
                    <button
                        type="submit"
                        style={{ backgroundColor: 'var(--primary)' }}
                        className="py-2 rounded-lg font-semibold text-white hover:opacity-90 transition"
                    >
                        Entrar
                    </button>
                </form>

                <p className="text-sm mt-6 text-center" style={{ color: 'var(--muted)' }}>
                    Não tem conta?{' '}
                    <Link to="/register" style={{ color: 'var(--primary)' }} className="hover:underline">
                        Cadastre-se
                    </Link>
                </p>
            </div>
        </div>
    )
}

export default Login