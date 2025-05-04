// App.jsx
import { createSignal, createEffect, onMount, For } from 'solid-js';
import { createStore } from 'solid-js/store';
import './App.css';
import { Login } from './login';
import { BACKEND_URL } from './settings';



function App() {
  const [expenses, setExpenses] = createStore([]);
  const [categories, setCategories] = createSignal([]);
  const [loading, setLoading] = createSignal(true);
  const [quickInput, setQuickInput] = createSignal('');
  
  // Form fields
  const [formData, setFormData] = createStore({
    date: new Date().toISOString().split('T')[0],
    amount: '',
    description: '',
    category: ''
  });
  
  // Fetch initial data
  onMount(async () => {
    try {
      const [expensesResponse, categoriesResponse] = await Promise.all([
        fetch(`${BACKEND_URL}/expenses`),
        fetch(`${BACKEND_URL}/categories`)
      ]);
      
      const expensesData = await expensesResponse.json();
      const categoriesData = await categoriesResponse.json();
      
      setExpenses(expensesData);
      setCategories(categoriesData);
    } catch (error) {
      console.error("Failed to fetch data:", error);
    } finally {
      setLoading(false);
    }
  });
  
  // Regular form submission
  const handleSubmit = async (e: SubmitEvent) => {
    e.preventDefault();
    
    try {
      const response = await fetch(`${BACKEND_URL}/expenses`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          date: formData.date,
          amount: parseFloat(formData.amount),
          description: formData.description,
          category: formData.category
        }),
        credentials: "include"
      });
      
      const newExpense = await response.json();
      setExpenses([newExpense, ...expenses]);
      
      // Reset form
      setFormData({
        date: new Date().toISOString().split('T')[0],
        amount: '',
        description: '',
        category: ''
      });
      
      // Also clear the quick input field
      setQuickInput('');
    } catch (error) {
      console.error("Failed to add expense:", error);
    }
  };
  
  // Parse quick entry and populate form fields
  const handleQuickParse = (e) => {
    e.preventDefault();
    const input = quickInput();
    
    try {
      // Parse input (e.g., "shoes for $25 #Home")
      const amountMatch = input.match(/\$(\d+(\.\d+)?)/);
      const categoryMatch = input.match(/#(\w+)/);
      
      if (!amountMatch) {
        alert("Please include an amount with $ symbol (e.g., $25)");
        return;
      }
      
      const amount = parseFloat(amountMatch[1]);
      
      // Find if the category exists in our list of categories
      let category = categoryMatch ? categoryMatch[1] : "Other";
      const categoryExists = categories().find(cat => 
        cat.toLowerCase() === category.toLowerCase()
      );
      
      // If category exists in our list, use the correctly capitalized version
      if (categoryExists) {
        category = categoryExists;
      }
      
      // Extract description (everything before # if present, otherwise everything)
      let description = input;
      if (categoryMatch) {
        description = input.substring(0, input.indexOf('#')).trim();
      }
      if (amountMatch) {
        description = description.replace(amountMatch[0], '').trim();
      }
      
      // Populate form with parsed data
      setFormData({
        date: new Date().toISOString().split('T')[0],
        amount: amount.toString(),
        description: description,
        category: category
      });
      
      // Scroll to form
      document.getElementById('regular-form').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
      console.error("Failed to parse quick entry:", error);
    }
  };

  // Get category class for tag styling
  const getCategoryClass = (category) => {
    const categoryMap = {
      'Food': 'bg-green-100 text-green-800',
      'Gifts': 'bg-purple-100 text-purple-800',
      'Health/medical': 'bg-red-100 text-red-800',
      'Home': 'bg-blue-100 text-blue-800',
      'Transportation': 'bg-yellow-100 text-yellow-800',
      'Personal': 'bg-indigo-100 text-indigo-800',
      'Pets': 'bg-pink-100 text-pink-800',
      'Utilities': 'bg-gray-100 text-gray-800',
      'Travel': 'bg-teal-100 text-teal-800',
      'Debt': 'bg-orange-100 text-orange-800',
      'Other': 'bg-gray-100 text-gray-600'
    };
    
    return categoryMap[category] || 'bg-gray-100 text-gray-600';
  };
  
  return (
    <div class="container">
      <header class="app-header">
        <h1>Expense Tracker</h1>
      </header>
      
      {/* Quick Entry Form */}
      <div class="quick-entry-card">
        <h2>Quick Entry</h2>
        <p>Format: "description $amount #category" (e.g., "shoes for $25 #Home")</p>
        <form onSubmit={handleQuickParse} class="quick-input-container">
          <input
            type="text"
            value={quickInput()}
            onInput={(e) => setQuickInput(e.target.value)}
            placeholder="shoes for $25 #Home"
            class="quick-input"
            required
          />
          <button type="submit" class="btn btn-quick">
            Parse Input
          </button>
        </form>
      </div>
      
      {/* Regular Form */}
      <div id="regular-form" class="form-card">
        <h2>Add Expense</h2>
        <form onSubmit={handleSubmit}>
          <div class="grid grid-2-col form-row">
            <div class="form-group">
              <label for="date">Date</label>
              <input
                type="date"
                id="date"
                value={formData.date}
                onInput={(e) => setFormData('date', e.target.value)}
              />
            </div>
            <div class="form-group">
              <label for="amount">Amount ($)</label>
              <input
                type="number"
                id="amount"
                step="0.01"
                value={formData.amount}
                onInput={(e) => setFormData('amount', e.target.value)}
                placeholder="10.99"
                required
              />
            </div>
          </div>
          <div class="form-group form-row">
            <label for="description">Description</label>
            <input
              type="text"
              id="description"
              value={formData.description}
              onInput={(e) => setFormData('description', e.target.value)}
              placeholder="Groceries"
              required
            />
          </div>
          <div class="form-group form-row">
            <label for="category">Category</label>
            <select
              id="category"
              value={formData.category}
              onInput={(e) => setFormData('category', e.target.value)}
              required
            >
              <option value="" disabled>Select a category</option>
              <For each={categories()}>
                {(category) => <option value={category}>{category}</option>}
              </For>
            </select>
          </div>
          <div class="form-row">
            <button type="submit" class="btn btn-success">
              Save Expense
            </button>
          </div>
        </form>
      </div>
      
      {/* Expenses List */}
      <div class="expenses-card">
        <h2>Recent Expenses</h2>
        {loading() ? (
          <div class="loading">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
          </div>
        ) : expenses.length === 0 ? (
          <div class="empty-state">
            <p>No expenses yet. Add your first one above!</p>
          </div>
        ) : (
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Description</th>
                  <th>Category</th>
                  <th style="text-align: right">Amount</th>
                </tr>
              </thead>
              <tbody>
                <For each={expenses}>
                  {(expense) => (
                    <tr>
                      <td class="expense-date">{new Date(expense.date).toLocaleDateString()}</td>
                      <td class="expense-description">{expense.description}</td>
                      <td>
                        <span class={`category-tag ${getCategoryClass(expense.category)}`}>
                          {expense.category}
                        </span>
                      </td>
                      <td class="expense-amount" style="text-align: right">
                        ${expense.amount.toFixed(2)}
                      </td>
                    </tr>
                  )}
                </For>
              </tbody>
            </table>
          </div>
        )}
      </div>
      <Login/>
      {fetch(`${BACKEND_URL}/auth/me`, {credentials: "include"}).then(res => res.json()).then(data => console.log("from auth/me", data))}
    </div>
  );
}

export default App;


