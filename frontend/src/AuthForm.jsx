import React, { useState } from "react";
import { registerUser, loginUser, setAuthToken } from "./api";

const AuthForm = ({ onAuthSuccess }) => {
    const [isRegistering, setIsRegistering] = useState(false);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage("");
        setLoading(true);

        try {
            if (isRegistering) {
                await registerUser(username, password);
                setMessage("✅ Registration successful! Please log in.");
                setIsRegistering(false);
            } else {
                const response = await loginUser(username, password);
                const token = response.data.access_token;
                setAuthToken(token);
                onAuthSuccess();
            }
            setPassword("");
        } catch (error) {
            console.error("Auth error:", error);
            const errorMessage =
                error.response?.data?.detail ||
                (isRegistering ? "Registration failed." : "Login failed.");
            setMessage(`❌ ${errorMessage}`);
        } finally {
            setLoading(false);
        }
    };

    const toggleMode = () => {
        setIsRegistering(!isRegistering);
        setMessage("");
        setUsername("");
        setPassword("");
    };

    return (
        <div className="auth-container">
            <h2>{isRegistering ? "Register" : "Login"}</h2>

            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button type="submit" disabled={loading}>
                    {loading
                        ? "Please wait..."
                        : isRegistering
                            ? "Register"
                            : "Login"}
                </button>
            </form>

            {message && <p className="message">{message}</p>}

            <button type="button" className="toggle-button" onClick={toggleMode}>
                {isRegistering
                    ? "Already have an account? Login"
                    : "Need an account? Register"}
            </button>
        </div>
    );
};

export default AuthForm;
