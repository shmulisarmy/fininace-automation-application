import { createSignal } from "solid-js";


const API_URL = "http://localhost:8000"

export function Login(){
  const [username, setUsername] = createSignal("");
  const [password, setPassword] = createSignal("");
  const [loginError, setLoginError] = createSignal("");
  const [server_res, setServerRes] = createSignal("");

  const handleLogin = (e: SubmitEvent) => {
    e.preventDefault();
    // Add your login logic here
    console.log("Username:", username());
    console.log("Password:", password());
    fetch(`${API_URL}/auth/login?username=${username()}&password=${password()}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      
    })
    .then((response) => response.json())
    .then((data) => {
      console.log("Login successful:", data);
      setServerRes(data);
    })
    .catch((error) => {
        console.error("Login failed:", error);
        setServerRes(error);

    });
  };

  return (
    <div class="login-card">
    <h2>Login</h2>
    <form onSubmit={handleLogin} class="login-form">
    <div class="form-group">
        <label>Username</label>
        <input type="text" value={username()} onInput={(e) => setUsername(e.target.value)} required />
    </div>
    <div class="form-group">
        <label>Password</label>
        <input type="password" value={password()} onInput={(e) => setPassword(e.target.value)} required />
    </div>
    {loginError() && <p class="error-text">{loginError()}</p>}
    <button type="submit" class="btn btn-success">Login</button>
    </form>
    <p>{server_res()}</p>
</div>
)
}