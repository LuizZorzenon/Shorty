const API_URL = import.meta.env.VITE_API_URL

export type Url = {
    id: number
    original_url: string
    short_key: string
    clicks: number
    is_active: boolean
}

function getAuthHeader() {
    const token = localStorage.getItem('access_token')
    return { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
}

function handleResponse<T>(response: Response): Promise<T> {
    if (response.status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        throw new Error
    }

    if (!response.ok) throw new Error('Erro na requisição')

    return response.json()
}

export async function login(email: string, password: string) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    })

    if (!response.ok) throw new Error('Credenciais inválidas')

    return response.json()
}

export async function register(email: string, username: string, password: string) {
    const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, username, password }),
    })

    if (!response.ok) throw new Error('Erro ao cadastrar')

    return response.json()
}

export async function getUrls(): Promise<Url[]> {
    const response = await fetch(`${API_URL}/urls/`, {
        headers: getAuthHeader(),
    })
    return handleResponse<Url[]>(response)
}

export async function createUrl(original_url: string): Promise<Url> {
    const response = await fetch(`${API_URL}/urls/`, {
        method: 'POST',
        headers: getAuthHeader(),
        body: JSON.stringify({ original_url }),
    })
    return handleResponse<Url>(response)
}

export async function deleteUrl(shortkey: string): Promise<void> {
    const response = await fetch(`${API_URL}/urls/${shortkey}`, {
        method: 'DELETE',
        headers: getAuthHeader(),
    })
    return handleResponse<void>(response)
}

export async function updateUrl(shortkey: string, original_url: string, is_active: boolean): Promise<Url> {
    const response = await fetch(`${API_URL}/urls/${shortkey}`, {
        method: 'PATCH',
        headers: getAuthHeader(),
        body: JSON.stringify({ original_url, is_active }),
    })
    return handleResponse<Url>(response)
}