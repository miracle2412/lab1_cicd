import { useEffect, useState } from 'react'
import './App.css'

const API_URL = '/api/items'

function App() {
  const [items, setItems] = useState([])
  const [name, setName] = useState('')
  const [price, setPrice] = useState('')
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState('')

  // Получение всех элементов с backend
  const loadItems = async () => {
    try {
      const response = await fetch(API_URL)

      if (!response.ok) {
        throw new Error('Failed to load items')
      }

      const data = await response.json()

      // Backend возвращает объект:
      // {
      //   "1": {"name": "Laptop", "price": 1200},
      //   "2": {"name": "Mouse", "price": 25}
      // }
      //
      // Преобразуем его в массив для React.
      const itemsArray = Object.entries(data).map(([id, item]) => ({
        id: Number(id),
        ...item,
      }))

      setItems(itemsArray)
      setError('')
    } catch (err) {
      console.error(err)
      setError('Cannot connect to backend')
    }
  }

  // Загружаем данные при открытии страницы
  useEffect(() => {
    loadItems()
  }, [])

  // Создание или редактирование элемента
  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!name.trim() || price === '') {
      setError('Enter item name and price')
      return
    }

    const item = {
      name: name.trim(),
      price: Number(price),
    }

    try {
      const url =
        editingId === null
          ? API_URL
          : `${API_URL}/${editingId}`

      const method = editingId === null ? 'POST' : 'PUT'

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(item),
      })

      if (!response.ok) {
        throw new Error('Request failed')
      }

      setName('')
      setPrice('')
      setEditingId(null)
      setError('')

      await loadItems()
    } catch (err) {
      console.error(err)
      setError('Failed to save item')
    }
  }

  // Подготовка элемента к редактированию
  const handleEdit = (item) => {
    setEditingId(item.id)
    setName(item.name)
    setPrice(item.price)
    setError('')
  }

  // Удаление элемента
  const handleDelete = async (id) => {
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: 'DELETE',
      })

      if (!response.ok) {
        throw new Error('Delete failed')
      }

      if (editingId === id) {
        setEditingId(null)
        setName('')
        setPrice('')
      }

      await loadItems()
    } catch (err) {
      console.error(err)
      setError('Failed to delete item')
    }
  }

  // Отмена редактирования
  const handleCancel = () => {
    setEditingId(null)
    setName('')
    setPrice('')
    setError('')
  }

  return (
    <div className="container">
      <h1>Item Manager</h1>

      <p className="subtitle">
        FastAPI + React
      </p>

      <form onSubmit={handleSubmit} className="item-form">
        <input
          type="text"
          placeholder="Item name"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />

        <input
          type="number"
          step="0.01"
          min="0"
          placeholder="Price"
          value={price}
          onChange={(event) => setPrice(event.target.value)}
        />

        <button type="submit">
          {editingId === null ? 'Add item' : 'Save'}
        </button>

        {editingId !== null && (
          <button
            type="button"
            className="cancel"
            onClick={handleCancel}
          >
            Cancel
          </button>
        )}
      </form>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      <div className="items">
        <h2>Items</h2>

        {items.length === 0 ? (
          <p className="empty">No items found</p>
        ) : (
          items.map((item) => (
            <div className="item" key={item.id}>
              <div>
                <strong>{item.name}</strong>
                <span>
                  ${Number(item.price).toFixed(2)}
                </span>
              </div>

              <div className="actions">
                <button
                  type="button"
                  onClick={() => handleEdit(item)}
                >
                  Edit
                </button>

                <button
                  type="button"
                  className="delete"
                  onClick={() => handleDelete(item.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default App